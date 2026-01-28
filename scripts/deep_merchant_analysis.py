"""
Deep Uncategorized Merchant Analysis
- Identifies business type for each merchant
- Determines if expense is reimbursable based on business type
- Cross-references against trip pickups to verify business vs personal
- Generates detailed categorization report
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import re

# ============================================================================
# MERCHANT DATABASE - Define what each business type does
# ============================================================================

MERCHANT_DIRECTORY = {
    # DOLLAR TREE - Variety store (personal supplies, cleaning, seasonal, snacks)
    'DOLLAR TREE': {
        'business_type': 'Variety/General Merchandise Store',
        'products': ['cleaning supplies', 'seasonal items', 'party supplies', 'small tools', 'snacks', 'household items'],
        'likely_category': 'Personal/Household Supplies',
        'reimbursable': False,
        'reason': 'Personal household/convenience purchases - not business related'
    },
    
    # RAISING CANES - QSR (Fast Casual Chicken Restaurant)
    'RAISING CANES': {
        'business_type': 'Quick Service Restaurant (QSR)',
        'products': ['chicken meals', 'sandwiches', 'drinks', 'combo meals'],
        'likely_category': 'Dining - Personal',
        'reimbursable': False,
        'reason': 'Personal dining expense. Even if at restaurant location, eating is personal spending'
    },
    
    # WAL-MART / WALMART - Discount Retailer
    'WAL-MART': {
        'business_type': 'General Discount Retailer',
        'products': ['groceries', 'household goods', 'clothing', 'electronics', 'personal care'],
        'likely_category': 'Personal Shopping/Groceries',
        'reimbursable': False,
        'reason': 'Personal retail purchases - groceries and household items'
    },
    
    # ALDI - Grocery Store
    'ALDI': {
        'business_type': 'Grocery Store',
        'products': ['groceries', 'household items', 'personal care'],
        'likely_category': 'Groceries/Personal Supplies',
        'reimbursable': False,
        'reason': 'Personal grocery shopping'
    },
    
    # WINCO FOODS - Warehouse Grocery
    'WINCO FOODS': {
        'business_type': 'Warehouse Grocery Store',
        'products': ['bulk groceries', 'household items', 'personal supplies'],
        'likely_category': 'Groceries/Personal Supplies',
        'reimbursable': False,
        'reason': 'Personal grocery/bulk shopping'
    },
    
    # TOM THUMB - Grocery Store
    'TOM THUMB': {
        'business_type': 'Grocery Store',
        'products': ['groceries', 'household items'],
        'likely_category': 'Groceries/Personal Supplies',
        'reimbursable': False,
        'reason': 'Personal grocery shopping'
    },
    
    # BRAUMS - Dairy/Ice Cream Shop
    'BRAUMS': {
        'business_type': 'Dairy Store / Ice Cream Shop',
        'products': ['ice cream', 'dairy products', 'milk', 'treats'],
        'likely_category': 'Dining - Personal',
        'reimbursable': False,
        'reason': 'Personal dining/treat purchase'
    },
    
    # BUC-EE\'S - Travel Center/Convenience
    'BUC-EE': {
        'business_type': 'Travel Center / Convenience Store',
        'products': ['fuel', 'snacks', 'drinks', 'travel items', 'candy'],
        'likely_category': 'Convenience/Personal',
        'reimbursable': False,
        'reason': 'Personal snacks/convenience purchases. Fuel would be separate category'
    },
    
    # TRACTOR SUPPLY - Agricultural/Farm Supply
    'TRACTOR SUPPLY': {
        'business_type': 'Farm & Agricultural Supply Store',
        'products': ['farm equipment', 'tools', 'animal feed', 'outdoor supplies', 'fencing', 'automotive supplies'],
        'likely_category': 'Personal/Hobby Supplies',
        'reimbursable': False,
        'reason': 'Personal hobby or home maintenance supplies - not courier business related'
    },
    
    # DOLLAR GENERAL - Variety store
    'DOLLAR GENERAL': {
        'business_type': 'Variety/General Merchandise Store',
        'products': ['household items', 'cleaning supplies', 'personal care', 'snacks'],
        'likely_category': 'Personal/Household Supplies',
        'reimbursable': False,
        'reason': 'Personal household/convenience purchases'
    },
    
    # OLLIES - Discount Retailer
    'OLLIES': {
        'business_type': 'Discount Closeout Retailer',
        'products': ['closeout items', 'household goods', 'personal items', 'seasonal'],
        'likely_category': 'Personal Shopping',
        'reimbursable': False,
        'reason': 'Personal retail purchases - closeout/discount shopping'
    },
    
    # OLD NAVY - Clothing Retailer
    'OLD NAVY': {
        'business_type': 'Apparel Retailer',
        'products': ['clothing', 'accessories', 'footwear'],
        'likely_category': 'Personal Clothing',
        'reimbursable': False,
        'reason': 'Personal clothing purchase'
    },
    
    # FAMOUS FOOTWEAR - Shoe Store
    'FAMOUS FOOTWEAR': {
        'business_type': 'Shoe/Footwear Retailer',
        'products': ['shoes', 'footwear', 'athletic shoes'],
        'likely_category': 'Personal Clothing/Shoes',
        'reimbursable': False,
        'reason': 'Personal footwear purchase. Not work-specific uniform.'
    },
    
    # HOME DEPOT - Home Improvement
    'HOME DEPOT': {
        'business_type': 'Home Improvement / Hardware Store',
        'products': ['building materials', 'tools', 'supplies', 'home improvement'],
        'likely_category': 'Personal/Home Supplies',
        'reimbursable': False,
        'reason': 'Personal home improvement/maintenance - not courier business'
    },
    
    # QT / QUICKTRIP - Convenience Store
    'QT': {
        'business_type': 'Convenience Store',
        'products': ['snacks', 'drinks', 'candy', 'fuel', 'personal items'],
        'likely_category': 'Personal/Convenience',
        'reimbursable': False,
        'reason': 'Personal snacks/convenience purchases'
    },
    
    # BEAUTY SUPPLY - Beauty Store
    'BEAUTY SUPPLY': {
        'business_type': 'Beauty Supply Store',
        'products': ['hair care', 'beauty products', 'personal care'],
        'likely_category': 'Personal Care',
        'reimbursable': False,
        'reason': 'Personal beauty/grooming purchases'
    },
    
    # NYX - Energy Drink / Beverage
    'NYX': {
        'business_type': 'Energy Drink Brand / Beverage Distributor',
        'products': ['energy drinks', 'beverages'],
        'likely_category': 'Dining/Beverages - Personal',
        'reimbursable': False,
        'reason': 'Personal beverage consumption. Could be argument for business (staying alert during work) but typically personal'
    },
    
    # AFFIRM - Buy Now Pay Later Service
    'AFFIRM': {
        'business_type': 'Fintech / Payment Platform',
        'products': ['installment payments', 'financing'],
        'likely_category': 'Payment/Financing - Depends on item',
        'reimbursable': False,
        'reason': 'Financing payment - actual item category depends on what was financed. Without knowing item, mark non-reimbursable'
    },
    
    # ATM WITHDRAWAL - Cash Withdrawal
    'ATM': {
        'business_type': 'Banking',
        'products': ['cash withdrawal'],
        'likely_category': 'Cash/Personal Spending',
        'reimbursable': False,
        'reason': 'Cash withdrawal - cannot track actual spending. Likely personal.'
    },
    
    # ACH HMFUSA - Health/Fitness Equipment?
    'HMFUSA': {
        'business_type': 'Unknown - ACH Payment',
        'products': ['subscription or service'],
        'likely_category': 'Subscription/Unknown',
        'reimbursable': False,
        'reason': 'ACH payment to unknown entity - requires receipt to verify. Likely personal subscription.'
    },
    
    # BANK TRANSFER - Internal
    'BANK TRANSFER': {
        'business_type': 'Banking',
        'products': ['account transfer'],
        'likely_category': 'Internal Transfer',
        'reimbursable': False,
        'reason': 'Internal bank transfer - not an actual expense'
    },
    
    # LS MONTICELLO - Liquor Store
    'LS MONTICELLO': {
        'business_type': 'Liquor Store',
        'products': ['alcoholic beverages', 'beer', 'wine'],
        'likely_category': 'Personal Beverage/Dining',
        'reimbursable': False,
        'reason': 'Personal alcohol purchase - not business related'
    },
}

# ============================================================================
# LOAD DATA
# ============================================================================

def load_data():
    """Load uncategorized expenses and trip data"""
    reports_dir = Path('c:/Users/dj-dev/Documents/courier/reports')
    csv_file = list(reports_dir.glob('expense_report_*.csv'))[0]
    
    expenses = pd.read_csv(csv_file)
    uncategorized = expenses[expenses['Category'] == 'Uncategorized'].copy()
    
    # Load trips
    trips_dir = Path('c:/Users/dj-dev/Documents/courier/data/consolidated/trips')
    trip_dfs = []
    for csv in sorted(trips_dir.glob('*.csv')):
        trip_dfs.append(pd.read_csv(csv))
    trips = pd.concat(trip_dfs, ignore_index=True)
    
    return uncategorized, trips

# ============================================================================
# MERCHANT ANALYSIS
# ============================================================================

def analyze_merchant(merchant_name):
    """Analyze a merchant and return categorization"""
    
    merchant_upper = str(merchant_name).upper()
    
    # Check exact matches
    for key, info in MERCHANT_DIRECTORY.items():
        if key in merchant_upper:
            return info.copy()
    
    # Check partial matches
    for key, info in MERCHANT_DIRECTORY.items():
        if key in merchant_upper or merchant_upper in key:
            return info.copy()
    
    # Heuristic-based categorization
    if any(word in merchant_upper for word in ['RESTAURANT', 'CAFE', 'PIZZA', 'BURGER', 'CHICKEN', 'TACO', 'DELI', 'GRILL']):
        return {
            'business_type': 'Restaurant/Food Service',
            'products': ['prepared meals'],
            'likely_category': 'Dining - Personal',
            'reimbursable': False,
            'reason': 'Restaurant/food service - personal dining'
        }
    elif any(word in merchant_upper for word in ['GAS', 'SHELL', 'CHEVRON', 'EXXON', 'FUEL']):
        return {
            'business_type': 'Gas Station',
            'products': ['fuel'],
            'likely_category': 'Vehicle - Fuel',
            'reimbursable': True,
            'reason': 'Vehicle fuel - likely reimbursable business expense'
        }
    elif any(word in merchant_upper for word in ['UBER', 'LYFT', 'DOORDASH', 'GRUBHUB']):
        return {
            'business_type': 'Gig Service Platform',
            'products': ['app subscription', 'services'],
            'likely_category': 'Business Apps/Services',
            'reimbursable': True,
            'reason': 'Gig platform subscription - business expense'
        }
    elif any(word in merchant_upper for word in ['PHONE', 'INTERNET', 'VERIZON', 'AT&T', 'TMOBILE']):
        return {
            'business_type': 'Telecommunications',
            'products': ['phone service', 'internet'],
            'likely_category': 'Phone/Internet',
            'reimbursable': True,
            'reason': 'Communication services - business expense'
        }
    elif any(word in merchant_upper for word in ['PARKING', 'TOLL', 'VALET']):
        return {
            'business_type': 'Parking/Tolls',
            'products': ['parking fees', 'tolls'],
            'likely_category': 'Vehicle - Tolls & Parking',
            'reimbursable': True,
            'reason': 'Business travel costs - reimbursable'
        }
    elif any(word in merchant_upper for word in ['INSURANCE', 'GEICO', 'STATEFARM']):
        return {
            'business_type': 'Insurance',
            'products': ['insurance premium'],
            'likely_category': 'Vehicle - Insurance',
            'reimbursable': False,
            'reason': 'Insurance - not typically reimbursable, but tax deductible'
        }
    else:
        return {
            'business_type': 'Unknown - Requires Manual Review',
            'products': ['unknown'],
            'likely_category': 'Unknown',
            'reimbursable': False,
            'reason': 'Unknown merchant - unable to categorize without receipt'
        }

def cross_reference_with_trips(merchant_name, trips):
    """Check if this merchant appears in trip pickup addresses"""
    
    merchant_keywords = merchant_name.upper().split()
    
    # Look for trips that picked up from this merchant
    pickup_matches = []
    for keyword in merchant_keywords:
        if len(keyword) > 3:  # Only check meaningful words
            try:
                # Escape special regex characters
                escaped_keyword = re.escape(keyword)
                matches = trips[trips['Pickup address'].str.upper().str.contains(escaped_keyword, na=False, regex=True)]
                if len(matches) > 0:
                    pickup_matches.append(len(matches))
            except:
                pass
    
    if pickup_matches and sum(pickup_matches) > 0:
        return True, sum(pickup_matches)
    return False, 0

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def main():
    print("=" * 100)
    print("DEEP UNCATEGORIZED MERCHANT ANALYSIS")
    print("=" * 100)
    
    uncategorized, trips = load_data()
    
    print(f"\nAnalyzing {len(uncategorized)} uncategorized transactions...")
    print(f"Total uncategorized amount: ${uncategorized['Amount'].sum():.2f}\n")
    
    # Analyze each transaction
    results = []
    
    for idx, row in uncategorized.iterrows():
        merchant = row['Merchant']
        amount = row['Amount']
        date = row['Date']
        
        # Get merchant info
        merchant_info = analyze_merchant(merchant)
        
        # Cross-reference with trips
        is_pickup, pickup_count = cross_reference_with_trips(merchant, trips)
        
        result = {
            'Date': date,
            'Merchant': merchant,
            'Amount': amount,
            'Business Type': merchant_info['business_type'],
            'Products/Services': ', '.join(merchant_info['products']),
            'Likely Category': merchant_info['likely_category'],
            'Reimbursable?': 'YES' if merchant_info['reimbursable'] else 'NO',
            'Is Pickup Location?': 'YES' if is_pickup else 'NO',
            'Pickup Count': pickup_count,
            'Reasoning': merchant_info['reason']
        }
        
        results.append(result)
    
    results_df = pd.DataFrame(results)
    
    # ========================================================================
    # GENERATE REPORTS
    # ========================================================================
    
    print("=" * 100)
    print("CATEGORIZATION RESULTS")
    print("=" * 100)
    
    # Summary by category
    print("\n1. SUMMARY BY LIKELY CATEGORY:")
    print("-" * 100)
    
    category_summary = results_df.groupby('Likely Category').agg({
        'Amount': ['sum', 'count', 'mean']
    }).sort_values(('Amount', 'sum'), ascending=False)
    
    category_summary.columns = ['Total ($)', 'Count', 'Avg ($)']
    for cat in category_summary.index:
        total = category_summary.loc[cat, 'Total ($)']
        count = category_summary.loc[cat, 'Count']
        avg = category_summary.loc[cat, 'Avg ($)']
        print(f"  {cat:40} ${total:8.2f}  ({int(count):3} transactions, avg ${avg:6.2f})")
    
    # Summary by reimbursable status
    print("\n2. REIMBURSABLE vs PERSONAL:")
    print("-" * 100)
    
    reimbursable_summary = results_df.groupby('Reimbursable?')['Amount'].agg(['sum', 'count']).sort_values('sum', ascending=False)
    for status in reimbursable_summary.index:
        total = reimbursable_summary.loc[status, 'sum']
        count = reimbursable_summary.loc[status, 'count']
        pct = total / results_df['Amount'].sum() * 100
        print(f"  {status:10} ${total:8.2f}  ({int(count):3} transactions, {pct:5.1f}%)")
    
    # Items that are pickup locations
    print("\n3. MERCHANTS THAT ARE ALSO PICKUP LOCATIONS (Likely business-related):")
    print("-" * 100)
    
    pickup_merchants = results_df[results_df['Is Pickup Location?'] == 'YES'].sort_values('Amount', ascending=False)
    if len(pickup_merchants) > 0:
        for idx, row in pickup_merchants.iterrows():
            print(f"\n  {row['Merchant']}")
            print(f"    Amount: ${row['Amount']:.2f}")
            print(f"    Business Type: {row['Business Type']}")
            print(f"    Pickup Count: {int(row['Pickup Count'])} times")
            print(f"    Assessment: {row['Reasoning']}")
            print(f"    Reimbursable: {row['Reimbursable?']}")
    else:
        print("  No uncategorized merchants found in pickup locations")
    
    # Top uncategorized items
    print("\n4. TOP 20 UNCATEGORIZED TRANSACTIONS:")
    print("-" * 100)
    
    top_items = results_df.sort_values('Amount', ascending=False).head(20)
    for idx, row in top_items.iterrows():
        print(f"\n  ${row['Amount']:7.2f}  {row['Date']}  {row['Merchant'][:50]}")
        print(f"    Type: {row['Business Type']}")
        print(f"    Category: {row['Likely Category']}")
        print(f"    Reimbursable: {row['Reimbursable?']}")
        if row['Is Pickup Location?'] == 'YES':
            print(f"    ⚠️  PICKUP LOCATION - appeared {int(row['Pickup Count'])} times in trips!")
    
    # Export detailed report
    print("\n" + "=" * 100)
    print("EXPORTING DETAILED CATEGORIZATION...")
    print("=" * 100)
    
    reports_dir = Path('c:/Users/dj-dev/Documents/courier/reports')
    
    # Export full categorization
    export_file = reports_dir / 'uncategorized_analysis_detailed.csv'
    results_df.to_csv(export_file, index=False)
    print(f"\n✓ Full analysis exported to: uncategorized_analysis_detailed.csv")
    
    # Export potential business expenses (from pickup locations)
    business_expenses = results_df[results_df['Is Pickup Location?'] == 'YES']
    if len(business_expenses) > 0:
        business_file = reports_dir / 'uncategorized_potential_business_expenses.csv'
        business_expenses.to_csv(business_file, index=False)
        print(f"✓ Potential business expenses (pickup locations): uncategorized_potential_business_expenses.csv")
        print(f"  Total: ${business_expenses['Amount'].sum():.2f}")
    
    # Summary statistics
    print("\n" + "=" * 100)
    print("FINAL SUMMARY")
    print("=" * 100)
    
    total_amount = results_df['Amount'].sum()
    reimbursable_amount = results_df[results_df['Reimbursable?'] == 'YES']['Amount'].sum()
    personal_amount = results_df[results_df['Reimbursable?'] == 'NO']['Amount'].sum()
    pickup_amount = results_df[results_df['Is Pickup Location?'] == 'YES']['Amount'].sum()
    
    print(f"\nTotal Uncategorized: ${total_amount:.2f}")
    print(f"  - Potentially Reimbursable: ${reimbursable_amount:.2f} ({reimbursable_amount/total_amount*100:.1f}%)")
    print(f"  - Personal: ${personal_amount:.2f} ({personal_amount/total_amount*100:.1f}%)")
    print(f"  - From Pickup Locations: ${pickup_amount:.2f} ({pickup_amount/total_amount*100:.1f}%)")
    
    print("\nNote: Items marked as 'pickup locations' appeared in your trip data as food delivery")
    print("pickup addresses. Even if you picked up from a restaurant, eating there is still")
    print("personal spending (not reimbursable), but it explains the expense pattern.\n")

if __name__ == "__main__":
    main()
