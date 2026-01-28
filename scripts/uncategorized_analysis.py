"""
Uncategorized Expense Analysis
Correlates uncategorized expenses with restaurant pickups to identify:
1. Hidden business expenses in uncategorized category
2. Spending patterns coinciding with restaurant pickup locations
3. Time-based spending correlations
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import re

# Load all expense data
def load_uncategorized_expenses():
    """Load the full expense report and filter uncategorized"""
    reports_dir = Path('c:/Users/dj-dev/Documents/courier/reports')
    csv_files = list(reports_dir.glob('expense_report_*.csv'))
    
    if not csv_files:
        print("ERROR: No expense report found")
        return None
    
    df = pd.read_csv(csv_files[0])
    uncategorized = df[df['Category'] == 'Uncategorized'].copy()
    
    print(f"Loaded {len(uncategorized)} uncategorized transactions from {len(df)} total")
    print(f"Uncategorized total: ${uncategorized['Amount'].sum():.2f}\n")
    
    return uncategorized

# Load trip data
def load_trip_data():
    """Load and consolidate all trip activity data"""
    trips_dir = Path('c:/Users/dj-dev/Documents/courier/data/consolidated/trips')
    
    dfs = []
    for csv_file in sorted(trips_dir.glob('*.csv')):
        try:
            df = pd.read_csv(csv_file)
            dfs.append(df)
            print(f"Loaded {len(df)} trips from {csv_file.name}")
        except Exception as e:
            print(f"ERROR loading {csv_file.name}: {e}")
    
    if not dfs:
        print("ERROR: No trip data found")
        return None
    
    trips = pd.concat(dfs, ignore_index=True)
    print(f"\nTotal trips loaded: {len(trips)}\n")
    return trips

# Analyze uncategorized transactions
def analyze_uncategorized(uncategorized):
    """Analyze uncategorized transactions for patterns"""
    
    print("=" * 80)
    print("UNCATEGORIZED EXPENSE ANALYSIS")
    print("=" * 80)
    print(f"\nTotal Uncategorized: {len(uncategorized)} transactions, ${uncategorized['Amount'].sum():.2f}\n")
    
    # Sort by amount to find highest spending
    top_expenses = uncategorized.nlargest(20, 'Amount')[['Date', 'Merchant', 'Amount']]
    print("TOP 20 UNCATEGORIZED EXPENSES:")
    print(top_expenses.to_string(index=False))
    
    # Look for merchant patterns
    print("\n" + "=" * 80)
    print("MERCHANT ANALYSIS:")
    print("=" * 80)
    
    merchant_summary = uncategorized.groupby('Merchant').agg({
        'Amount': ['sum', 'count', 'mean']
    }).sort_values(('Amount', 'sum'), ascending=False).head(30)
    merchant_summary.columns = ['Total ($)', 'Count', 'Avg ($)']
    print(merchant_summary)
    
    # Extract keywords to identify business expenses
    print("\n" + "=" * 80)
    print("POTENTIAL BUSINESS EXPENSE PATTERNS:")
    print("=" * 80)
    
    # Keywords indicating business expenses
    business_keywords = [
        'uber', 'doordash', 'grubhub', 'dashpass', 'eats', 'delivery', 
        'restaurant', 'cafe', 'supply', 'office', 'stationery', 'printing',
        'stripe', 'square', 'paypal', 'bank', 'fee', 'tax',
        'software', 'app', 'subscription', 'membership',
        'phone', 'internet', 'storage', 'cloud',
        'amazon business', 'staples', 'lowes', 'home depot'
    ]
    
    potential_business = []
    for idx, row in uncategorized.iterrows():
        merchant = str(row['Merchant']).lower()
        for keyword in business_keywords:
            if keyword in merchant:
                potential_business.append(row)
                break
    
    if potential_business:
        potential_df = pd.DataFrame(potential_business)
        print(f"\nFound {len(potential_df)} potential business expenses:\n")
        print(potential_df[['Date', 'Merchant', 'Amount']].sort_values('Amount', ascending=False).to_string(index=False))
        print(f"\nPotential Business Subtotal: ${potential_df['Amount'].sum():.2f}")
    else:
        print("\nNo business-pattern keywords found in merchant names")

# Analyze restaurant patterns
def analyze_restaurant_timing(uncategorized, trips):
    """Find correlation between uncategorized spending and restaurant pickups"""
    
    print("\n" + "=" * 80)
    print("SPENDING vs. RESTAURANT PICKUP CORRELATION ANALYSIS")
    print("=" * 80)
    
    # Parse dates
    uncategorized['Date'] = pd.to_datetime(uncategorized['Date'])
    
    # Check trips data structure
    print("\nTrip data columns:")
    print(trips.columns.tolist())
    
    # Identify restaurant pickups in trip data
    restaurant_cols = [col for col in trips.columns if 'pickup' in col.lower() or 'merchant' in col.lower() or 'store' in col.lower()]
    print(f"\nPotential merchant columns in trips: {restaurant_cols}")
    
    # Try to find restaurant/store columns
    possible_store_cols = [col for col in trips.columns if any(x in col.lower() for x in ['store', 'restaurant', 'merchant', 'pickup'])]
    
    if possible_store_cols:
        trips_sample = trips[possible_store_cols].head(20)
        print("\nSample trip merchant data:")
        print(trips_sample)
    
    # Daily analysis - aggregate spending by date
    daily_spending = uncategorized.groupby(uncategorized['Date'].dt.date).agg({
        'Amount': ['sum', 'count']
    }).reset_index()
    daily_spending.columns = ['Date', 'Total_Spending', 'Transaction_Count']
    daily_spending = daily_spending.sort_values('Total_Spending', ascending=False)
    
    print("\nTOP SPENDING DAYS:")
    print(daily_spending.head(15).to_string(index=False))
    
    # Hour analysis if possible
    print("\n" + "=" * 80)
    print("HOURLY SPENDING PATTERNS:")
    print("=" * 80)
    
    if 'Date' in uncategorized.columns and len(uncategorized['Date'].astype(str).iloc[0]) > 10:
        try:
            uncategorized['Hour'] = pd.to_datetime(uncategorized['Date']).dt.hour
            hourly = uncategorized.groupby('Hour').agg({
                'Amount': ['sum', 'count', 'mean']
            }).sort_values(('Amount', 'sum'), ascending=False)
            hourly.columns = ['Total ($)', 'Count', 'Avg ($)']
            print(hourly)
        except:
            print("Could not parse hours from date column")
    
    # Day of week analysis
    print("\n" + "=" * 80)
    print("SPENDING BY DAY OF WEEK:")
    print("=" * 80)
    
    uncategorized['DayOfWeek'] = pd.to_datetime(uncategorized['Date']).dt.day_name()
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    dow_spending = uncategorized.groupby('DayOfWeek').agg({
        'Amount': ['sum', 'count', 'mean']
    }).reindex(dow_order)
    dow_spending.columns = ['Total ($)', 'Count', 'Avg ($)']
    print(dow_spending)

# Identify personal vs likely business
def categorize_uncategorized(uncategorized):
    """Attempt to recategorize uncategorized items"""
    
    print("\n" + "=" * 80)
    print("RECLASSIFICATION ATTEMPT:")
    print("=" * 80)
    
    # Define patterns for reclassification
    patterns = {
        'Restaurant/Dining': {
            'keywords': ['cafe', 'coffee', 'restaurant', 'burger', 'pizza', 'taco', 'chicken', 
                        'deli', 'bar', 'grill', 'bbq', 'korean', 'thai', 'chinese', 'mexican',
                        'japanese', 'vietnamese', 'italian', 'pizza', 'sandwich', 'lunch', 'dinner'],
            'reimbursable': False
        },
        'Fast Food': {
            'keywords': ['mcdonalds', 'wendys', 'taco bell', 'kfc', 'popeyes', 'chick-fil-a', 'subway'],
            'reimbursable': False
        },
        'Grocery/Convenience': {
            'keywords': ['grocery', 'walmart', 'target', 'walgreens', 'cvs', 'whataburger', 'gas', 'convenience'],
            'reimbursable': False
        },
        'Rideshare/Delivery Apps': {
            'keywords': ['uber', 'lyft', 'doordash', 'grubhub', 'instacart', 'amazon'],
            'reimbursable': True
        },
        'Utilities/Services': {
            'keywords': ['phone', 'internet', 'electric', 'water', 'utility', 'cable'],
            'reimbursable': False
        }
    }
    
    results = {'Restaurant/Dining': [], 'Fast Food': [], 'Grocery/Convenience': [], 'Rideshare/Delivery Apps': [], 'Utilities/Services': []}
    unclassified = []
    
    for idx, row in uncategorized.iterrows():
        merchant = str(row['Merchant']).lower()
        found = False
        
        for category, config in patterns.items():
            for keyword in config['keywords']:
                if keyword in merchant:
                    row_data = row.copy()
                    row_data['SubCategory'] = category
                    row_data['Reimbursable'] = config['reimbursable']
                    results[category].append(row_data)
                    found = True
                    break
            if found:
                break
        
        if not found:
            unclassified.append(row)
    
    # Print results
    for category, items in results.items():
        if items:
            df = pd.DataFrame(items)
            total = df['Amount'].sum()
            print(f"\n{category}: {len(df)} transactions, ${total:.2f}")
    
    if unclassified:
        print(f"\nUnclassified/Review Needed: {len(unclassified)} transactions")
        unclass_df = pd.DataFrame(unclassified)
        print(f"Total: ${unclass_df['Amount'].sum():.2f}")
        print("\nTop unclassified merchants:")
        print(unclass_df.groupby('Merchant')['Amount'].agg(['sum', 'count']).sort_values('sum', ascending=False).head(15))

# Main execution
if __name__ == "__main__":
    print("Starting Uncategorized Expense Analysis...\n")
    
    # Load data
    uncategorized = load_uncategorized_expenses()
    trips = load_trip_data()
    
    if uncategorized is not None and trips is not None:
        # Analyze uncategorized
        analyze_uncategorized(uncategorized)
        
        # Analyze timing correlation
        analyze_restaurant_timing(uncategorized, trips)
        
        # Reclassification attempt
        categorize_uncategorized(uncategorized)
        
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
