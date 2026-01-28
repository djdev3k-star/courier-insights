"""
Generate Merchant Category Suggestions for Review
Creates a master list of unique merchants with proposed categories
"""

import pandas as pd
from pathlib import Path


def categorize_merchant(description):
    """Suggest category based on merchant name"""
    desc_upper = description.upper()
    
    # EV Charging / Fuel
    if any(x in desc_upper for x in ['TESLA', 'SUPERCHARGER', 'EVGO', 'XEAL EV', 'BLINK CHARGING', 'EV CHARGING', 'HYPERFUEL', 'NYX*SILVER', 'CHARGING']):
        return 'EV Charging'
    
    # Fast Food / Restaurants
    if any(x in desc_upper for x in ['RAISING CANES', 'MCDONALD', 'WHATABURGER', 'TACO BELL', 'BURGER KING', 'JACK IN THE BOX', 'SONIC DRIVE', 'WENDYS', 'CHIPOTLE', 'POPEYES', 'PANDA EXPRESS', 'LITTLE CAESAR', 'JOLLIBEE', 'BRAUMS']):
        return 'Fast Food'
    
    if any(x in desc_upper for x in ['CAFE', 'DELI', 'ITALIAN', 'BURGER', 'PIZZA', 'ZALAT', 'PEACH COBBLER', 'GRIFFS', 'BAWARCHI']):
        return 'Restaurant'
    
    # Coffee / Drinks
    if any(x in desc_upper for x in ['STARBUCKS', 'DUTCH BROS', 'COFFEE', 'DONUTS', 'DUNKIN']):
        return 'Coffee & Beverages'
    
    # Groceries / Convenience
    if any(x in desc_upper for x in ['KROGER', 'TOM THUMB', 'ALDI', 'ALBERTSONS', 'WAL-MART', 'WINCO', 'WM SUPERCENTER']):
        return 'Groceries'
    
    if any(x in desc_upper for x in ['DOLLAR TREE', 'DOLLAR GENERAL', 'FIVE BELOW', 'OLLIES', '7-ELEVEN', 'QT ', 'RACETRAC', 'BUC-EE']):
        return 'Convenience Store'
    
    # Pharmacy / Health
    if any(x in desc_upper for x in ['CVS', 'WALGREENS', 'PHARMACY']):
        return 'Pharmacy/Health'
    
    # Retail
    if any(x in desc_upper for x in ['TARGET', 'HOME DEPOT', 'TRACTOR SUPPLY', 'OLD NAVY', 'FAMOUS FOOTWEAR', 'UNIFORM FACTORY']):
        return 'Retail Shopping'
    
    if any(x in desc_upper for x in ['BEAUTY SUPPLY']):
        return 'Personal Care'
    
    # Transfers / Fees / Financial
    if any(x in desc_upper for x in ['INSTANT TRANSFER', 'ACH DEBIT', 'ACCOUNT UNLOAD', 'ATM WITHDRAWAL', 'FEE FOR', 'OUT-OF-NETWORK', 'AFFIRM', 'CREDIT ONE']):
        return 'Financial/Transfers'
    
    # Utilities / Services
    if any(x in desc_upper for x in ['TMOBILE', 'T-MOBILE']):
        return 'Phone/Utilities'
    
    if any(x in desc_upper for x in ['CSC SERVICEWORKS', 'LAUNDRY']):
        return 'Laundry/Services'
    
    # Gas Stations (non-EV)
    if any(x in desc_upper for x in ['SHELL', 'EXXON', 'CHEVRON', 'FUEL CITY', 'COTTON GIN']):
        return 'Gas Station'
    
    # Alcohol
    if any(x in desc_upper for x in ['BEER', 'WINE', 'LIQUOR', 'MONTICELLO']):
        return 'Alcohol'
    
    # Default
    return 'Uncategorized'


def generate_merchant_categories():
    """Generate merchant category suggestions"""
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    expenses_file = base_path / 'reports' / 'itemized_expenses_by_month.csv'
    
    # Load expenses
    df = pd.read_csv(expenses_file)
    
    # Get unique merchants with total spending and visit counts
    merchant_summary = df.groupby('Description').agg({
        'Amount': ['sum', 'count']
    }).reset_index()
    
    merchant_summary.columns = ['Merchant', 'Total_Spent', 'Visit_Count']
    merchant_summary = merchant_summary.sort_values('Total_Spent', ascending=False)
    
    # Add suggested categories
    merchant_summary['Suggested_Category'] = merchant_summary['Merchant'].apply(categorize_merchant)
    merchant_summary['Approved_Category'] = ''  # For user to fill in
    merchant_summary['Notes'] = ''  # For user comments
    
    # Display summary by category
    print("="*80)
    print("MERCHANT CATEGORIZATION SUMMARY")
    print("="*80)
    print()
    
    category_summary = merchant_summary.groupby('Suggested_Category').agg({
        'Total_Spent': 'sum',
        'Visit_Count': 'sum',
        'Merchant': 'count'
    }).reset_index()
    
    category_summary.columns = ['Category', 'Total_Spent', 'Total_Visits', 'Unique_Merchants']
    category_summary = category_summary.sort_values('Total_Spent', ascending=False)
    
    print(f"{'Category':<25} {'Merchants':<12} {'Visits':<8} {'Total':<12}")
    print("-" * 80)
    
    for _, row in category_summary.iterrows():
        print(f"{row['Category']:<25} {row['Unique_Merchants']:<12} {row['Total_Visits']:<8} ${row['Total_Spent']:>10,.2f}")
    
    print("-" * 80)
    print(f"{'TOTAL':<25} {merchant_summary['Merchant'].count():<12} {merchant_summary['Visit_Count'].sum():<8} ${merchant_summary['Total_Spent'].sum():>10,.2f}")
    
    # Show top merchants by category
    print("\n" + "="*80)
    print("TOP MERCHANTS BY CATEGORY (For Review)")
    print("="*80)
    
    for category in category_summary['Category']:
        cat_merchants = merchant_summary[merchant_summary['Suggested_Category'] == category].head(10)
        if len(cat_merchants) > 0:
            print(f"\n{category}:")
            for _, row in cat_merchants.iterrows():
                merchant = row['Merchant'][:50]
                print(f"  • {merchant:<50} {row['Visit_Count']}x  ${row['Total_Spent']:>8,.2f}")
    
    # Export for review
    output_file = base_path / 'reports' / 'merchant_category_master.csv'
    
    # Reorder columns for easier review
    export_df = merchant_summary[['Merchant', 'Suggested_Category', 'Approved_Category', 'Visit_Count', 'Total_Spent', 'Notes']]
    export_df.to_csv(output_file, index=False)
    
    print("\n" + "="*80)
    print("INSTRUCTIONS FOR REVIEW")
    print("="*80)
    print(f"\n1. Open: {output_file}")
    print("2. Review the 'Suggested_Category' column")
    print("3. Fill in 'Approved_Category' column with your final category")
    print("4. Add any notes if needed")
    print("5. Save the file")
    print("6. Run the categorization script to generate spending by category report")
    print()
    print(f"✓ Exported to: {output_file}")
    print(f"  Total Unique Merchants: {len(merchant_summary)}")
    print(f"  Categories Suggested: {len(category_summary)}")
    print()


if __name__ == '__main__':
    generate_merchant_categories()
