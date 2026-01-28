"""
Enhanced Spending Analysis - Cross-Reference Bank Spending with Trips
Breaks down the $8,334 monthly spending into:
1. Customer reimbursements (tracked in receipts)
2. Customer purchases (in bank, matched to trips)
3. EV charging (business expense)
4. Personal spending (restaurants, stores)
"""

import pandas as pd
import re
from pathlib import Path
from datetime import datetime, timedelta


class SpendingBreakdownAnalyzer:
    """
    Cross-references bank spending with trips to identify:
    - Customer reimbursements (already tracked)
    - Customer purchases (findable via trip cross-reference)
    - EV charging (business expense)
    - Personal spending (remaining)
    """
    
    def __init__(self, base_path='c:/Users/dj-dev/Documents/courier'):
        self.base_path = Path(base_path)
        self.trips_df = None
        self.bank_df = None
        self.receipts_df = None
        
    def load_data(self):
        """Load all necessary data"""
        print("Loading data...")
        
        # Load trips
        dfs = []
        trips_dir = self.base_path / 'data' / 'consolidated' / 'trips'
        for csv_file in sorted(trips_dir.glob('*.csv')):
            df = pd.read_csv(csv_file)
            dfs.append(df)
        self.trips_df = pd.concat(dfs, ignore_index=True)
        
        # Standardize trip times
        for col in ['Pickup Time', 'Trip drop off time', 'Dropoff Time']:
            if col in self.trips_df.columns:
                self.trips_df[col] = pd.to_datetime(self.trips_df[col], errors='coerce')
        
        # Use best available time column
        if 'Dropoff Time' in self.trips_df.columns:
            self.trips_df['Trip_Time'] = self.trips_df['Dropoff Time']
        elif 'Trip drop off time' in self.trips_df.columns:
            self.trips_df['Trip_Time'] = self.trips_df['Trip drop off time']
        else:
            self.trips_df['Trip_Time'] = self.trips_df['Pickup Time']
        
        print(f"  ✓ Loaded {len(self.trips_df)} trips")
        
        # Load bank
        dfs = []
        bank_dir = self.base_path / 'bank'
        for csv_file in sorted(bank_dir.glob('Uber Pro Card Statement*.csv')):
            df = pd.read_csv(csv_file)
            dfs.append(df)
        self.bank_df = pd.concat(dfs, ignore_index=True)
        
        self.bank_df['Posted Date'] = pd.to_datetime(self.bank_df['Posted Date'], errors='coerce')
        self.bank_df['Amount'] = pd.to_numeric(
            self.bank_df['Amount'].astype(str).str.replace(r'[\$\+,]', '', regex=True),
            errors='coerce'
        )
        self.bank_df['Is_Expense'] = self.bank_df['Amount'] < 0
        self.bank_df['Is_Uber_Deposit'] = self.bank_df['Description'].str.contains(
            'Uber App Payout', case=False, na=False
        )
        
        print(f"  ✓ Loaded {len(self.bank_df)} bank transactions")
        
        # Load receipts
        receipts_path = self.base_path / 'data' / 'receipts' / 'Trip Receipts-Refund Tracker.csv'
        self.receipts_df = pd.read_csv(receipts_path)
        self.receipts_df['Date'] = pd.to_datetime(self.receipts_df['Date'], errors='coerce')
        
        for col in ['Total', 'Refund']:
            if col in self.receipts_df.columns:
                self.receipts_df[col] = pd.to_numeric(
                    self.receipts_df[col].astype(str).str.replace(r'[\$,]', '', regex=True),
                    errors='coerce'
                )
        
        print(f"  ✓ Loaded {len(self.receipts_df)} receipt entries")
        
        return self
    
    def match_bank_to_trips(self, time_window_hours=2, amount_tolerance=1.0):
        """
        Cross-reference bank expenses with trips to find customer purchases
        
        Logic: If a bank expense occurs within X hours of a trip completion,
        it's likely a customer purchase for that delivery.
        """
        print("\n" + "="*70)
        print("CROSS-REFERENCING: Bank Expenses → Trips")
        print("="*70)
        
        # Get personal expenses (not Uber deposits)
        expenses = self.bank_df[
            self.bank_df['Is_Expense'] & 
            ~self.bank_df['Is_Uber_Deposit']
        ].copy()
        
        print(f"\nTotal personal expenses: {len(expenses)} transactions")
        print(f"Total amount: ${abs(expenses['Amount'].sum()):,.2f}")
        
        # Match to trips
        expenses['Matched_Trip_UUID'] = None
        expenses['Time_Diff_Minutes'] = None
        expenses['Likely_Customer_Purchase'] = False
        
        matched_count = 0
        matched_amount = 0
        
        for idx, expense in expenses.iterrows():
            expense_time = expense['Posted Date']
            expense_amount = abs(expense['Amount'])
            
            # Find trips within time window
            time_lower = expense_time - timedelta(hours=time_window_hours)
            time_upper = expense_time + timedelta(hours=time_window_hours)
            
            nearby_trips = self.trips_df[
                (self.trips_df['Trip_Time'] >= time_lower) &
                (self.trips_df['Trip_Time'] <= time_upper)
            ]
            
            if len(nearby_trips) > 0:
                # Find closest trip
                time_diffs = abs((nearby_trips['Trip_Time'] - expense_time).dt.total_seconds() / 60)
                closest_idx = time_diffs.idxmin()
                closest_trip = nearby_trips.loc[closest_idx]
                
                expenses.at[idx, 'Matched_Trip_UUID'] = closest_trip.get('Trip UUID', None)
                expenses.at[idx, 'Time_Diff_Minutes'] = time_diffs[closest_idx]
                expenses.at[idx, 'Likely_Customer_Purchase'] = True
                
                matched_count += 1
                matched_amount += expense_amount
        
        print(f"\nMatched to trips: {matched_count} expenses (${matched_amount:,.2f})")
        print(f"Unmatched: {len(expenses) - matched_count} expenses (${abs(expenses[~expenses['Likely_Customer_Purchase']]['Amount'].sum()):,.2f})")
        
        return expenses
    
    def categorize_unmatched(self, expenses_df):
        """
        Categorize expenses that don't match trips
        - EV charging (Tesla, charging stations)
        - Personal (restaurants, stores, etc.)
        """
        print("\n" + "="*70)
        print("CATEGORIZING: Unmatched Expenses")
        print("="*70)
        
        unmatched = expenses_df[~expenses_df['Likely_Customer_Purchase']].copy()
        
        # EV Charging patterns
        ev_keywords = [
            'tesla', 'supercharger', 'evgo', 'chargepoint', 
            'electrify america', 'blink', 'charging'
        ]
        
        unmatched['Is_EV_Charging'] = unmatched['Description'].str.lower().str.contains(
            '|'.join(ev_keywords), na=False
        )
        
        # Calculate totals
        ev_charging = unmatched[unmatched['Is_EV_Charging']]
        personal = unmatched[~unmatched['Is_EV_Charging']]
        
        ev_total = abs(ev_charging['Amount'].sum())
        personal_total = abs(personal['Amount'].sum())
        
        print(f"\nEV Charging (business expense):")
        print(f"  Count: {len(ev_charging)}")
        print(f"  Total: ${ev_total:,.2f}")
        
        if len(ev_charging) > 0:
            print(f"\n  Top EV charging locations:")
            ev_merchants = ev_charging.groupby('Description')['Amount'].agg(['sum', 'count'])
            ev_merchants['sum'] = abs(ev_merchants['sum'])
            ev_merchants = ev_merchants.sort_values('sum', ascending=False).head(5)
            for merchant, row in ev_merchants.iterrows():
                print(f"    • {merchant}: ${row['sum']:,.2f} ({row['count']:.0f}x)")
        
        print(f"\nPersonal Spending (restaurants, stores, etc.):")
        print(f"  Count: {len(personal)}")
        print(f"  Total: ${personal_total:,.2f}")
        
        if len(personal) > 0:
            print(f"\n  Top personal merchants:")
            personal_merchants = personal.groupby('Description')['Amount'].agg(['sum', 'count'])
            personal_merchants['sum'] = abs(personal_merchants['sum'])
            personal_merchants = personal_merchants.sort_values('sum', ascending=False).head(10)
            for merchant, row in personal_merchants.iterrows():
                print(f"    • {merchant}: ${row['sum']:,.2f} ({row['count']:.0f}x)")
        
        return {
            'ev_charging': ev_charging,
            'personal': personal,
            'ev_total': ev_total,
            'personal_total': personal_total
        }
    
    def full_breakdown(self):
        """Generate complete spending breakdown"""
        print("\n" + "="*80)
        print("COMPLETE SPENDING BREAKDOWN ANALYSIS")
        print("="*80)
        
        # Get all expenses
        expenses = self.bank_df[
            self.bank_df['Is_Expense'] & 
            ~self.bank_df['Is_Uber_Deposit']
        ]
        total_spending = abs(expenses['Amount'].sum())
        
        print(f"\nTotal Spending on Uber Pro Card: ${total_spending:,.2f}")
        print(f"Total Transactions: {len(expenses)}")
        
        # 1. Receipts tracker (already documented)
        receipts_total = self.receipts_df['Total'].sum() if 'Total' in self.receipts_df.columns else 0
        receipts_count = len(self.receipts_df)
        
        print(f"\n1. CUSTOMER REIMBURSEMENTS (Tracked in Receipts):")
        print(f"   Amount: ${receipts_total:,.2f}")
        print(f"   Count: {receipts_count} entries")
        print(f"   % of total: {(receipts_total/total_spending*100):.1f}%")
        
        # 2. Match to trips
        matched_expenses = self.match_bank_to_trips()
        customer_purchases = matched_expenses[matched_expenses['Likely_Customer_Purchase']]
        customer_total = abs(customer_purchases['Amount'].sum())
        
        print(f"\n2. CUSTOMER PURCHASES (Matched to Trips):")
        print(f"   Amount: ${customer_total:,.2f}")
        print(f"   Count: {len(customer_purchases)} transactions")
        print(f"   % of total: {(customer_total/total_spending*100):.1f}%")
        
        # 3. Categorize unmatched
        categories = self.categorize_unmatched(matched_expenses)
        
        print(f"\n3. EV CHARGING (Business Expense):")
        print(f"   Amount: ${categories['ev_total']:,.2f}")
        print(f"   Count: {len(categories['ev_charging'])} transactions")
        print(f"   % of total: {(categories['ev_total']/total_spending*100):.1f}%")
        
        print(f"\n4. PERSONAL SPENDING (Restaurants, Stores, etc.):")
        print(f"   Amount: ${categories['personal_total']:,.2f}")
        print(f"   Count: {len(categories['personal'])} transactions")
        print(f"   % of total: {(categories['personal_total']/total_spending*100):.1f}%")
        
        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"\nTotal Spending: ${total_spending:,.2f}")
        print(f"  - Customer Reimbursements (receipts): ${receipts_total:,.2f} ({receipts_total/total_spending*100:.1f}%)")
        print(f"  - Customer Purchases (trip-matched): ${customer_total:,.2f} ({customer_total/total_spending*100:.1f}%)")
        print(f"  - EV Charging (business): ${categories['ev_total']:,.2f} ({categories['ev_total']/total_spending*100:.1f}%)")
        print(f"  - Personal Spending: ${categories['personal_total']:,.2f} ({categories['personal_total']/total_spending*100:.1f}%)")
        
        accounted = receipts_total + customer_total + categories['ev_total'] + categories['personal_total']
        print(f"\nTotal Accounted: ${accounted:,.2f}")
        print(f"Difference: ${abs(total_spending - accounted):,.2f}")
        
        # Monthly averages (5 months)
        months = 5
        print(f"\n" + "="*80)
        print(f"MONTHLY AVERAGES (over {months} months)")
        print("="*80)
        print(f"  - Total Spending: ${total_spending/months:,.2f}/month")
        print(f"  - Customer Reimbursements: ${receipts_total/months:,.2f}/month")
        print(f"  - Customer Purchases: ${customer_total/months:,.2f}/month")
        print(f"  - EV Charging: ${categories['ev_total']/months:,.2f}/month")
        print(f"  - Personal: ${categories['personal_total']/months:,.2f}/month")
        
        return {
            'total_spending': total_spending,
            'receipts': receipts_total,
            'customer_purchases': customer_total,
            'ev_charging': categories['ev_total'],
            'personal': categories['personal_total'],
            'matched_expenses': matched_expenses,
            'categories': categories
        }


if __name__ == '__main__':
    analyzer = SpendingBreakdownAnalyzer()
    analyzer.load_data()
    results = analyzer.full_breakdown()
    
    print("\n✓ Analysis complete!")
    print("\nNEXT STEPS:")
    print("1. Review customer purchases matched to trips")
    print("2. Add matched purchases to Trip Receipts tracker")
    print("3. Categorize EV charging as business expense")
    print("4. Review personal spending for optimization")
