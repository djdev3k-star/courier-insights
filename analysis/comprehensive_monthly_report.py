"""
Comprehensive Monthly Transaction Report
Combines trips, payments, and bank data with line-by-line details and monthly balances
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
DATA_DIR = Path('data')
TRIPS_DIR = DATA_DIR / 'consolidated' / 'trips'
PAYMENTS_DIR = DATA_DIR / 'consolidated' / 'payments'
BANK_DIR = Path('bank')
OUTPUT_DIR = Path('reports') / 'monthly_comprehensive'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_all_data():
    """Load and prepare all data sources."""
    print("Loading trips...")
    trips_df = pd.concat([pd.read_csv(f) for f in sorted(TRIPS_DIR.glob('*.csv'))], ignore_index=True)
    trips_df['Trip drop off time'] = pd.to_datetime(trips_df['Trip drop off time'], errors='coerce')
    trips_df = trips_df[trips_df['Trip status'] == 'completed'].copy()
    trips_df['Month'] = trips_df['Trip drop off time'].dt.strftime('%Y-%m')
    
    print("Loading payments...")
    payments_df = pd.concat([pd.read_csv(f) for f in sorted(PAYMENTS_DIR.glob('*.csv'))], ignore_index=True)
    # Fix date parsing: Remove timezone abbreviation (CDT, CST, etc.) that pandas can't parse
    import re
    payments_df['vs reporting'] = payments_df['vs reporting'].astype(str).apply(lambda x: re.sub(r'\s+[A-Z]{3}$', '', x))
    payments_df['vs reporting'] = pd.to_datetime(payments_df['vs reporting'], errors='coerce', utc=True)
    
    # Parse payment amounts (include ALL payment types)
    for col in ['Paid to you', 'Paid to you : Your earnings', 'Paid to you : Your earnings : Fare',
                'Paid to you:Your earnings:Fare:Fare', 'Paid to you:Your earnings:Tip',
                'Paid to you:Trip balance:Refunds:Order Value', 'Paid to you:Your earnings:Promotion:Incentive',
                'Paid to you:Your earnings:Promotion:Boost+', 'Paid to you:Trip balance:Expenses:Instant Pay Fees',
                'Paid to you:Trip balance:Refunds:Toll', 'Paid to you:Your earnings:Fare:Return Trip Fare',
                'Paid to you:Your earnings:Other earnings:Delivery Adjustment', 'Paid to you:Your earnings:Other earnings:Adjustment',
                'Paid to you:Your earnings:Promotion:Quest']:
        if col in payments_df.columns:
            payments_df[col] = pd.to_numeric(payments_df[col], errors='coerce').fillna(0)
    
    print("Loading bank statements...")
    bank_list = []
    for csv_file in sorted(BANK_DIR.glob('Uber Pro Card Statement*.csv')):
        df = pd.read_csv(csv_file)
        df['source_file'] = csv_file.name
        bank_list.append(df)
    bank_df = pd.concat(bank_list, ignore_index=True)
    bank_df['Posted Date'] = pd.to_datetime(bank_df['Posted Date'], errors='coerce')
    bank_df['Amount'] = bank_df['Amount'].astype(str).str.replace(r'[\$\+,]', '', regex=True)
    bank_df['Amount'] = pd.to_numeric(bank_df['Amount'], errors='coerce')
    bank_df['Month'] = bank_df['Posted Date'].dt.strftime('%Y-%m')
    
    return trips_df, payments_df, bank_df

def create_combined_report(trips_df, payments_df, bank_df):
    """Create comprehensive line-by-line report."""
    
    # Group payments by Trip UUID to get all payment details
    trip_payment_details = []
    
    for trip_uuid in trips_df['Trip UUID'].unique():
        trip_payments = payments_df[payments_df['Trip UUID'] == trip_uuid]
        
        if len(trip_payments) == 0:
            continue
        
        # Aggregate payment details
        total_paid = trip_payments['Paid to you'].sum()
        total_fare = trip_payments['Paid to you:Your earnings:Fare:Fare'].sum()
        total_tip = trip_payments['Paid to you:Your earnings:Tip'].sum()
        total_refund = trip_payments['Paid to you:Trip balance:Refunds:Order Value'].sum()
        total_incentive = trip_payments['Paid to you:Your earnings:Promotion:Incentive'].sum()
        total_boost = trip_payments['Paid to you:Your earnings:Promotion:Boost+'].sum()
        instant_pay_fees = trip_payments['Paid to you:Trip balance:Expenses:Instant Pay Fees'].sum()
        
        # Payment descriptions
        descriptions = trip_payments['Description'].unique().tolist()
        has_customer_purchase = any('cash collected' in str(d).lower() for d in descriptions)
        
        trip_payment_details.append({
            'Trip UUID': trip_uuid,
            'Total Paid': total_paid,
            'Fare': total_fare,
            'Tip': total_tip,
            'Refund': total_refund,
            'Incentive': total_incentive,
            'Boost': total_boost,
            'Instant Pay Fee': instant_pay_fees,
            'Customer Purchase': has_customer_purchase,
            'Payment Descriptions': '; '.join([str(d) for d in descriptions]),
            'Payment Count': len(trip_payments)
        })
    
    payment_details_df = pd.DataFrame(trip_payment_details)
    
    # Merge with trip data
    combined = trips_df.merge(payment_details_df, on='Trip UUID', how='left')
    
    # Fill missing payment data
    for col in ['Total Paid', 'Fare', 'Tip', 'Refund', 'Incentive', 'Boost', 'Instant Pay Fee']:
        combined[col] = combined[col].fillna(0)
    combined['Customer Purchase'] = combined['Customer Purchase'].fillna(False)
    
    # Add calculated fields
    combined['Net Earnings'] = combined['Total Paid'] - combined['Instant Pay Fee']
    
    # Sort by drop off time
    combined = combined.sort_values('Trip drop off time')
    
    return combined

def create_monthly_summaries(combined_df, bank_df):
    """Create monthly summary reports."""
    
    summaries = []
    
    for month in sorted(combined_df['Month'].unique()):
        month_trips = combined_df[combined_df['Month'] == month]
        month_bank = bank_df[bank_df['Month'] == month]
        
        # Trip metrics
        trip_count = len(month_trips)
        total_distance = month_trips['Trip distance'].sum()
        
        # Payment metrics
        total_paid = month_trips['Total Paid'].sum()
        total_fare = month_trips['Fare'].sum()
        total_tip = month_trips['Tip'].sum()
        total_refund = month_trips['Refund'].sum()
        total_incentive = month_trips['Incentive'].sum()
        total_boost = month_trips['Boost'].sum()
        total_fees = month_trips['Instant Pay Fee'].sum()
        net_earnings = month_trips['Net Earnings'].sum()
        
        # Customer purchases
        customer_purchase_count = month_trips['Customer Purchase'].sum()
        
        # Bank metrics
        bank_deposits = month_bank[month_bank['Amount'] > 0]['Amount'].sum()
        bank_charges = month_bank[month_bank['Amount'] < 0]['Amount'].sum()
        bank_net = bank_deposits + bank_charges
        
        summaries.append({
            'Month': month,
            'Trips': trip_count,
            'Distance (mi)': total_distance,
            'Total Paid': total_paid,
            'Fare': total_fare,
            'Tip': total_tip,
            'Refunds': total_refund,
            'Incentives': total_incentive,
            'Boost': total_boost,
            'Instant Pay Fees': total_fees,
            'Net Earnings': net_earnings,
            'Customer Purchases': int(customer_purchase_count),
            'Bank Deposits': bank_deposits,
            'Bank Charges': bank_charges,
            'Bank Net': bank_net,
            'Difference (Paid - Bank)': total_paid - bank_deposits
        })
    
    return pd.DataFrame(summaries)

def main():
    print("="*70)
    print("COMPREHENSIVE MONTHLY TRANSACTION REPORT")
    print("="*70)
    
    # Load data
    trips_df, payments_df, bank_df = load_all_data()
    print(f"\n✓ Loaded: {len(trips_df):,} trips, {len(payments_df):,} payments, {len(bank_df):,} bank transactions\n")
    
    # Create combined report
    print("Creating combined transaction report...")
    combined_df = create_combined_report(trips_df, payments_df, bank_df)
    
    # Select output columns
    output_columns = [
        'Trip drop off time', 'Month', 'Trip UUID',
        'Pickup address', 'Drop off address', 'Trip distance',
        'Service type', 'Product Type', 'Payment Type',
        'Total Paid', 'Fare', 'Tip', 'Refund', 'Incentive', 'Boost',
        'Instant Pay Fee', 'Net Earnings', 'Customer Purchase',
        'Payment Count', 'Payment Descriptions'
    ]
    
    detail_report = combined_df[output_columns].copy()
    detail_report.to_csv(OUTPUT_DIR / 'all_transactions_detailed.csv', index=False)
    print(f"✓ Saved detailed transactions: all_transactions_detailed.csv\n")
    
    # Create monthly summaries
    print("Creating monthly summaries...")
    monthly_summary = create_monthly_summaries(combined_df, bank_df)
    monthly_summary.to_csv(OUTPUT_DIR / 'monthly_summary.csv', index=False)
    print(f"✓ Saved monthly summary: monthly_summary.csv\n")
    
    # Print summary
    print("="*70)
    print("MONTHLY SUMMARY")
    print("="*70)
    print(monthly_summary.to_string(index=False))
    
    # Create individual month reports
    print("\n" + "="*70)
    print("CREATING INDIVIDUAL MONTH REPORTS")
    print("="*70)
    
    for month in sorted(combined_df['Month'].unique()):
        month_data = combined_df[combined_df['Month'] == month][output_columns].copy()
        
        # Add running balance
        month_data = month_data.sort_values('Trip drop off time')
        month_data['Running Balance'] = month_data['Net Earnings'].cumsum()
        
        filename = f'{month}_detailed_transactions.csv'
        month_data.to_csv(OUTPUT_DIR / filename, index=False)
        print(f"  ✓ {month}: {len(month_data)} trips, ${month_data['Net Earnings'].sum():,.2f}")
    
    # Grand totals
    print("\n" + "="*70)
    print("GRAND TOTALS")
    print("="*70)
    print(f"Total Trips: {len(combined_df):,}")
    print(f"Total Distance: {combined_df['Trip distance'].sum():,.2f} mi")
    print(f"Total Paid: ${combined_df['Total Paid'].sum():,.2f}")
    print(f"  Fare: ${combined_df['Fare'].sum():,.2f}")
    print(f"  Tip: ${combined_df['Tip'].sum():,.2f}")
    print(f"  Incentives: ${combined_df['Incentive'].sum():,.2f}")
    print(f"  Boost: ${combined_df['Boost'].sum():,.2f}")
    print(f"  Refunds: ${combined_df['Refund'].sum():,.2f}")
    print(f"Instant Pay Fees: ${combined_df['Instant Pay Fee'].sum():,.2f}")
    print(f"Net Earnings: ${combined_df['Net Earnings'].sum():,.2f}")
    print(f"Customer Purchases: {int(combined_df['Customer Purchase'].sum())}")
    
    bank_total_deposits = bank_df[bank_df['Amount'] > 0]['Amount'].sum()
    bank_total_charges = bank_df[bank_df['Amount'] < 0]['Amount'].sum()
    print(f"\nBank Deposits: ${bank_total_deposits:,.2f}")
    print(f"Bank Charges: ${bank_total_charges:,.2f}")
    print(f"Bank Net: ${bank_total_deposits + bank_total_charges:,.2f}")
    
    print(f"\n✓ All reports saved to: {OUTPUT_DIR.absolute()}")
    print("="*70)

if __name__ == '__main__':
    main()
