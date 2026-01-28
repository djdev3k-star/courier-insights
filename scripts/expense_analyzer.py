"""
Courier Expense Report Generator
Separates reimbursable business expenses from personal spending
Categorizes all transactions for tax and financial tracking
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

EXPENSE_CATEGORIES = {
    # REIMBURSABLE BUSINESS EXPENSES
    'vehicle_fuel': {
        'keywords': ['shell', 'chevron', 'exxon', 'valero', 'conoco', 'speedway', 'circle k', 'pilot', 'loves', 'gas', 'fuel', 'diesel'],
        'category': 'Vehicle - Fuel',
        'reimbursable': True,
        'tax_deductible': True,
    },
    'ev_charging': {
        'keywords': ['electrify', 'chargepoint', 'tesla supercharger', 'evgo', 'blink', 'ionity', 'tesla charging', 'ev charging', 'charging station', 'supercharger'],
        'category': 'Vehicle - EV Charging',
        'reimbursable': True,
        'tax_deductible': True,
    },
    'tolls_parking': {
        'keywords': ['toll', 'parking', 'valet', 'meter', 'parkwhiz', 'spothero'],
        'category': 'Vehicle - Tolls & Parking',
        'reimbursable': True,
        'tax_deductible': True,
    },
    'vehicle_maintenance': {
        'keywords': ['oil change', 'car wash', 'carwash', 'auto service', 'mechanic', 'tire', 'maintenance', 'detailing', 'wash', 'auto spa', 'lube', 'firestone', 'goodyear'],
        'category': 'Vehicle - Maintenance & Washing',
        'reimbursable': True,
        'tax_deductible': True,
    },
    'vehicle_insurance': {
        'keywords': ['insurance', 'geico', 'statefarm', 'allstate', 'progressive', 'aaa', 'auto insurance'],
        'category': 'Vehicle - Insurance',
        'reimbursable': False,
        'tax_deductible': True,
    },
    'vehicle_registration': {
        'keywords': ['registration', 'license plate', 'dmv', 'vehicle registration', 'inspection'],
        'category': 'Vehicle - Registration & Inspection',
        'reimbursable': False,
        'tax_deductible': True,
    },
    'app_subscriptions': {
        'keywords': ['doordash', 'uber', 'lyft', 'grubhub', 'instacart', 'spotify', 'subscription', 'premium'],
        'category': 'App Subscriptions & Memberships',
        'reimbursable': True,
        'tax_deductible': True,
    },
    'phone_internet': {
        'keywords': ['verizon', 'at&t', 'tmobile', 'sprint', 'phone', 'mobile', 'internet', 'wifi', 'cellular'],
        'category': 'Phone & Internet',
        'reimbursable': True,
        'tax_deductible': True,
    },
    'office_supplies': {
        'keywords': ['staples', 'office depot', 'amazon', 'supplies', 'office', 'laptop', 'computer', 'phone', 'tablet'],
        'category': 'Office Supplies & Equipment',
        'reimbursable': True,
        'tax_deductible': True,
    },
    'bank_fees': {
        'keywords': ['bank fee', 'overdraft', 'monthly fee', 'transfer fee', 'atm fee'],
        'category': 'Bank Fees',
        'reimbursable': False,
        'tax_deductible': True,
    },
    
    # PERSONAL / NON-REIMBURSABLE
    'restaurant_dining': {
        'keywords': ['restaurant', 'pizza', 'burger', 'cafe', 'coffee', 'diner', 'bbq', 'sushi', 'steak', 'seafood', 'italian', 'mexican', 'thai', 'chinese', 'indian', 'vietnamese', 'breakfast', 'lunch', 'dinner', 'bistro', 'gastropub', 'tavern', 'bar & grill'],
        'category': 'Dining - Restaurants (Personal)',
        'reimbursable': False,
        'tax_deductible': False,
    },
    'grocery_supplies': {
        'keywords': ['kroger', 'walmart', 'target', 'whole foods', 'trader joe', 'safeway', 'publix', 'albertsons', 'costco', 'grocery', 'supermarket', 'market'],
        'category': 'Groceries & Supplies',
        'reimbursable': False,
        'tax_deductible': False,
    },
    'fast_food': {
        'keywords': ['mcdonalds', 'burger king', 'chick-fil-a', 'subway', 'taco bell', 'kfc', 'popeyes', 'arbys', 'wendys', 'in-n-out', 'five guys', 'chipotle', 'panera', 'fast food', 'quick service'],
        'category': 'Fast Food (Personal)',
        'reimbursable': False,
        'tax_deductible': False,
    },
    'convenience_store': {
        'keywords': ['7-eleven', 'circle k', 'speedway', 'convenience', 'quickmart'],
        'category': 'Convenience Store',
        'reimbursable': False,
        'tax_deductible': False,
    },
    'entertainment': {
        'keywords': ['netflix', 'hulu', 'disney', 'cinema', 'movie', 'theater', 'concert', 'ticket', 'games', 'gaming'],
        'category': 'Entertainment (Personal)',
        'reimbursable': False,
        'tax_deductible': False,
    },
    'clothing': {
        'keywords': ['nike', 'adidas', 'clothing', 'apparel', 'fashion', 'mall', 'retail', 'boutique', 'shoes', 'pants', 'shirt'],
        'category': 'Clothing & Fashion',
        'reimbursable': False,
        'tax_deductible': False,
    },
    'health_wellness': {
        'keywords': ['gym', 'fitness', 'yoga', 'pharmacy', 'cvs', 'walgreens', 'health', 'doctor', 'hospital', 'clinic', 'medical'],
        'category': 'Health & Wellness',
        'reimbursable': False,
        'tax_deductible': False,
    },
}

DATA_DIR = Path("bank")
REPORTS_DIR = Path("reports")

# ============================================================================
# DATA LOADING
# ============================================================================

def load_bank_statements():
    """Load all Uber Pro Card statements"""
    dfs = []
    for file in sorted(DATA_DIR.glob("Uber Pro Card Statement*.csv")):
        try:
            df = pd.read_csv(file)
            dfs.append(df)
            print(f"✓ Loaded {file.name}")
        except Exception as e:
            print(f"✗ Error loading {file.name}: {e}")
    
    if not dfs:
        return None
    
    combined = pd.concat(dfs, ignore_index=True)
    return combined

# ============================================================================
# CATEGORIZATION
# ============================================================================

def categorize_transaction(merchant, amount, description=""):
    """Categorize a single transaction"""
    search_text = f"{merchant} {description}".lower()
    
    for category_key, details in EXPENSE_CATEGORIES.items():
        for keyword in details['keywords']:
            if keyword.lower() in search_text:
                return {
                    'category': details['category'],
                    'reimbursable': details['reimbursable'],
                    'tax_deductible': details['tax_deductible'],
                    'type': category_key,
                }
    
    return {
        'category': 'Uncategorized',
        'reimbursable': False,
        'tax_deductible': False,
        'type': 'uncategorized',
    }

def analyze_expenses(df):
    """Analyze and categorize all expenses"""
    if df is None or len(df) == 0:
        return None
    
    df = df.copy()
    
    # Standardize column names
    df.columns = df.columns.str.strip()
    
    # Parse date
    if 'Posted Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Posted Date'], errors='coerce')
    
    # Rename columns for clarity
    if 'Description' in df.columns:
        df['Merchant'] = df['Description']
    
    if 'Amount' in df.columns:
        # Extract numeric value and handle +/- signs
        df['Amount'] = df['Amount'].str.replace('$', '').str.replace('+', '')
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').abs()
    
    # Filter out payouts and credits
    df = df[~df['Merchant'].str.contains('Payout|Credit', case=False, na=False)]
    
    if 'Amount' not in df.columns or 'Merchant' not in df.columns:
        print("Could not find required columns")
        return None
    
    # Remove zero amounts
    df = df[df['Amount'] > 0]
    
    # Categorize each transaction
    df['Category'] = df.apply(
        lambda row: categorize_transaction(row['Merchant'], row['Amount'])['category'],
        axis=1
    )
    df['Reimbursable'] = df.apply(
        lambda row: categorize_transaction(row['Merchant'], row['Amount'])['reimbursable'],
        axis=1
    )
    df['TaxDeductible'] = df.apply(
        lambda row: categorize_transaction(row['Merchant'], row['Amount'])['tax_deductible'],
        axis=1
    )
    
    return df[['Date', 'Merchant', 'Amount', 'Category', 'Reimbursable', 'TaxDeductible']].dropna(subset=['Amount', 'Date']).sort_values('Date')

# ============================================================================
# REPORTING
# ============================================================================

def generate_expense_report(df):
    """Generate comprehensive expense report"""
    
    print("\n" + "="*80)
    print("COURIER EXPENSE REPORT")
    print("="*80)
    
    # Summary statistics
    print("\n📊 EXPENSE SUMMARY")
    print("-" * 80)
    total_expenses = df['Amount'].sum()
    reimbursable_total = df[df['Reimbursable']]['Amount'].sum()
    personal_total = df[~df['Reimbursable']]['Amount'].sum()
    
    print(f"Total Expenses:         ${total_expenses:,.2f}")
    print(f"Reimbursable Expenses:  ${reimbursable_total:,.2f} ({(reimbursable_total/total_expenses)*100:.1f}%)")
    print(f"Personal Expenses:      ${personal_total:,.2f} ({(personal_total/total_expenses)*100:.1f}%)")
    print(f"Tax Deductible:         ${df[df['TaxDeductible']]['Amount'].sum():,.2f}")
    
    # By category
    print("\n📋 EXPENSES BY CATEGORY")
    print("-" * 80)
    by_category = df.groupby('Category').agg({
        'Amount': ['sum', 'count', 'mean']
    }).round(2)
    by_category.columns = ['Total', 'Count', 'Average']
    by_category = by_category.sort_values('Total', ascending=False)
    
    print(by_category.to_string())
    
    # Reimbursable vs Personal
    print("\n💰 REIMBURSABLE vs PERSONAL")
    print("-" * 80)
    reimbursable_by_cat = df[df['Reimbursable']].groupby('Category')['Amount'].sum().sort_values(ascending=False)
    personal_by_cat = df[~df['Reimbursable']].groupby('Category')['Amount'].sum().sort_values(ascending=False)
    
    print("\nREIMBURSABLE BUSINESS EXPENSES:")
    for cat, amt in reimbursable_by_cat.items():
        count = len(df[(df['Category'] == cat) & (df['Reimbursable'])])
        print(f"  {cat:40} ${amt:>10,.2f}  ({count} transactions)")
    
    print("\nPERSONAL / NON-REIMBURSABLE EXPENSES:")
    for cat, amt in personal_by_cat.items():
        count = len(df[(df['Category'] == cat) & (~df['Reimbursable'])])
        print(f"  {cat:40} ${amt:>10,.2f}  ({count} transactions)")
    
    # Restaurant breakdown
    print("\n🍴 PERSONAL DINING EXPENSES (Non-Reimbursable)")
    print("-" * 80)
    restaurants = df[(df['Category'].str.contains('Dining - Restaurants|Fast Food', na=False)) & (~df['Reimbursable'])]
    if len(restaurants) > 0:
        print(f"Total Dining Spent:     ${restaurants['Amount'].sum():,.2f}")
        print(f"Number of Visits:       {len(restaurants)}")
        print(f"Average per Visit:      ${restaurants['Amount'].mean():,.2f}")
        print(f"Highest Single Visit:   ${restaurants['Amount'].max():,.2f}")
        print(f"Lowest Single Visit:    ${restaurants['Amount'].min():,.2f}")
        
        print("\nTop Restaurant Merchants:")
        top_merchants = restaurants.groupby('Merchant')['Amount'].agg(['sum', 'count']).sort_values('sum', ascending=False).head(10)
        for merchant, row in top_merchants.iterrows():
            print(f"  {merchant:40} ${row['sum']:>10,.2f}  ({int(row['count'])} visits)")
    
    # Vehicle expenses
    print("\n🚗 VEHICLE-RELATED EXPENSES (Reimbursable)")
    print("-" * 80)
    vehicle = df[(df['Category'].str.contains('Vehicle', na=False)) & (df['Reimbursable'])]
    if len(vehicle) > 0:
        print(f"Total Vehicle Expenses: ${vehicle['Amount'].sum():,.2f}")
        vehicle_by_type = vehicle.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        for cat, amt in vehicle_by_type.items():
            count = len(vehicle[vehicle['Category'] == cat])
            print(f"  {cat:40} ${amt:>10,.2f}  ({count} transactions)")

def export_to_csv(df):
    """Export detailed expense report to CSV"""
    REPORTS_DIR.mkdir(exist_ok=True)
    
    # Full expense report
    full_export = df.sort_values('Date')
    full_path = REPORTS_DIR / f"expense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    full_export.to_csv(full_path, index=False)
    print(f"\n✓ Full expense report saved to: {full_path.name}")
    
    # Reimbursable expenses only
    reimbursable = df[df['Reimbursable']].sort_values('Date')
    reimburse_path = REPORTS_DIR / f"reimbursable_expenses_{datetime.now().strftime('%Y%m%d')}.csv"
    reimbursable.to_csv(reimburse_path, index=False)
    print(f"✓ Reimbursable expenses saved to: {reimburse_path.name}")
    
    # Personal expenses only
    personal = df[~df['Reimbursable']].sort_values('Date')
    personal_path = REPORTS_DIR / f"personal_expenses_{datetime.now().strftime('%Y%m%d')}.csv"
    personal.to_csv(personal_path, index=False)
    print(f"✓ Personal expenses saved to: {personal_path.name}")
    
    return full_path, reimburse_path, personal_path

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("🔍 COURIER EXPENSE ANALYZER - LOADING DATA...")
    print("="*80 + "\n")
    
    # Load bank data
    print("📂 Loading Bank Statements:")
    df = load_bank_statements()
    
    if df is None or len(df) == 0:
        print("❌ No bank data found.")
        return
    
    # Analyze expenses
    print(f"\n📊 Analyzing {len(df)} transactions...")
    analyzed = analyze_expenses(df)
    
    if analyzed is None or len(analyzed) == 0:
        print("❌ Could not analyze transactions.")
        return
    
    # Generate report
    generate_expense_report(analyzed)
    
    # Export to CSV
    print("\n" + "="*80)
    print("💾 EXPORTING REPORTS")
    print("="*80)
    export_to_csv(analyzed)
    
    print("\n" + "="*80)
    print("✅ Expense Analysis Complete!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
