"""
Categorize Personal Spending - Exclude Business Reimbursements
Cross-references bank statements with receipt tracker to identify personal vs business spending
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta


def load_bank_statements():
    """Load all bank statements"""
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    expenses_file = base_path / 'reports' / 'itemized_expenses_by_month.csv'
    
    # Load from pre-processed file
    df = pd.read_csv(expenses_file)
    df['Posted Date'] = pd.to_datetime(df['Posted Date'])
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    
    return df


def load_receipt_tracker():
    """Load receipt tracker with reimbursed amounts"""
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    tracker_file = base_path / 'data' / 'receipts' / 'Trip Receipts-Refund Tracker.csv'
    
    df = pd.read_csv(tracker_file)
    
    # Parse dates - handle multiple date columns
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Parse refund amounts
    if 'Refund' in df.columns:
        df['Refund'] = df['Refund'].replace(r'[\$,]', '', regex=True)
        df['Refund'] = pd.to_numeric(df['Refund'], errors='coerce')
    
    # Only rows with refund amounts
    reimbursed = df[df['Refund'].notna() & (df['Refund'] > 0)].copy()
    
    return reimbursed


def match_transactions(bank_df, receipts_df):
    """Match bank transactions with receipt tracker entries"""
    
    # Create matched list
    matched_indices = set()
    matches = []
    
    for _, receipt in receipts_df.iterrows():
        receipt_date = receipt['Date']
        receipt_amount = receipt['Refund']
        
        if pd.isna(receipt_date) or pd.isna(receipt_amount):
            continue
        
        # Look for bank transactions within +/- 3 days with matching amount
        date_min = receipt_date - timedelta(days=3)
        date_max = receipt_date + timedelta(days=3)
        
        candidates = bank_df[
            (bank_df['Posted Date'] >= date_min) &
            (bank_df['Posted Date'] <= date_max) &
            (np.abs(bank_df['Amount'] - receipt_amount) < 0.50)  # Within 50 cents
        ]
        
        for idx, transaction in candidates.iterrows():
            if idx not in matched_indices:
                matched_indices.add(idx)
                matches.append({
                    'Bank_Date': transaction['Posted Date'],
                    'Bank_Description': transaction['Description'],
                    'Bank_Amount': transaction['Amount'],
                    'Receipt_Date': receipt_date,
                    'Receipt_Merchant': receipt.get('Pickup Address', ''),
                    'Receipt_Amount': receipt_amount,
                    'Category': 'Business Reimbursement'
                })
                break  # Only match once
    
    return matched_indices, matches


def categorize_merchant(description):
    """Categorize merchant"""
    desc_upper = description.upper()
    
    # Business-only merchants
    if any(x in desc_upper for x in ['TESLA', 'SUPERCHARGER', 'EVGO', 'XEAL EV', 'BLINK CHARGING', 'EV CHARGING', 'HYPERFUEL', 'NYX*SILVER', 'CHARGING']):
        return 'Business - EV Charging'
    
    # Fast Food
    if any(x in desc_upper for x in ['RAISING CANES', 'MCDONALD', 'WHATABURGER', 'TACO BELL', 'BURGER KING', 'JACK IN THE BOX', 'SONIC DRIVE', 'WENDYS', 'CHIPOTLE', 'POPEYES', 'PANDA EXPRESS', 'LITTLE CAESAR', 'JOLLIBEE', 'BRAUMS']):
        return 'Personal - Fast Food'
    
    if any(x in desc_upper for x in ['CAFE', 'DELI', 'ITALIAN', 'BURGER', 'PIZZA', 'ZALAT', 'PEACH COBBLER', 'GRIFFS', 'BAWARCHI']):
        return 'Personal - Restaurant'
    
    # Coffee
    if any(x in desc_upper for x in ['STARBUCKS', 'DUTCH BROS', 'COFFEE', 'DONUTS', 'DUNKIN']):
        return 'Personal - Coffee & Beverages'
    
    # Groceries
    if any(x in desc_upper for x in ['KROGER', 'TOM THUMB', 'ALDI', 'ALBERTSONS', 'WAL-MART', 'WINCO', 'WM SUPERCENTER']):
        return 'Personal - Groceries'
    
    if any(x in desc_upper for x in ['DOLLAR TREE', 'DOLLAR GENERAL', 'FIVE BELOW', 'OLLIES', '7-ELEVEN', 'QT ', 'RACETRAC', 'BUC-EE']):
        return 'Personal - Convenience Store'
    
    # Pharmacy
    if any(x in desc_upper for x in ['CVS', 'WALGREENS', 'PHARMACY']):
        return 'Personal - Pharmacy/Health'
    
    # Retail
    if any(x in desc_upper for x in ['TARGET', 'HOME DEPOT', 'TRACTOR SUPPLY', 'OLD NAVY', 'FAMOUS FOOTWEAR', 'UNIFORM FACTORY', 'BEAUTY SUPPLY']):
        return 'Personal - Retail Shopping'
    
    # Financial
    if any(x in desc_upper for x in ['INSTANT TRANSFER', 'ACH DEBIT', 'ACCOUNT UNLOAD', 'ATM WITHDRAWAL', 'FEE FOR', 'OUT-OF-NETWORK', 'AFFIRM', 'CREDIT ONE']):
        return 'Financial - Transfers/Fees'
    
    # Utilities
    if any(x in desc_upper for x in ['TMOBILE', 'T-MOBILE']):
        return 'Personal - Phone/Utilities'
    
    # Gas Stations (non-EV)
    if any(x in desc_upper for x in ['SHELL', 'EXXON', 'CHEVRON', 'FUEL CITY', 'COTTON GIN']):
        return 'Personal - Gas Station'
    
    # Alcohol
    if any(x in desc_upper for x in ['BEER', 'WINE', 'LIQUOR', 'MONTICELLO']):
        return 'Personal - Alcohol'
    
    return 'Personal - Uncategorized'


def analyze_spending():
    """Analyze and categorize personal vs business spending"""
    
    print("="*80)
    print("PERSONAL SPENDING ANALYSIS - EXCLUDING BUSINESS REIMBURSEMENTS")
    print("="*80)
    print()
    
    # Load data
    print("Loading data...")
    bank_df = load_bank_statements()
    receipts_df = load_receipt_tracker()
    
    print(f"  Bank transactions: {len(bank_df)}")
    print(f"  Receipt tracker entries: {len(receipts_df)}")
    print()
    
    # Match transactions
    print("Matching bank transactions with receipt tracker...")
    matched_indices, matches = match_transactions(bank_df, receipts_df)
    print(f"  Matched transactions: {len(matches)}")
    print()
    
    # Categorize all transactions
    bank_df['Category'] = bank_df['Description'].apply(categorize_merchant)
    bank_df['Is_Matched'] = bank_df.index.isin(matched_indices)
    
    # Mark matched as business reimbursement
    bank_df.loc[bank_df['Is_Matched'], 'Category'] = 'Business - Customer Reimbursement'
    
    # Summary by category
    category_summary = bank_df.groupby('Category').agg({
        'Amount': 'sum',
        'Description': 'count'
    }).reset_index()
    category_summary.columns = ['Category', 'Total', 'Transactions']
    category_summary = category_summary.sort_values('Total', ascending=False)
    
    print("SPENDING BY CATEGORY:")
    print("-" * 80)
    print(f"{'Category':<45} {'Transactions':<15} {'Total':<12}")
    print("-" * 80)
    
    business_total = 0
    personal_total = 0
    financial_total = 0
    
    for _, row in category_summary.iterrows():
        category = row['Category']
        txns = int(row['Transactions'])
        total = row['Total']
        
        print(f"{category:<45} {txns:<15} ${total:>10,.2f}")
        
        if 'Business' in category:
            business_total += total
        elif 'Financial' in category:
            financial_total += total
        else:
            personal_total += total
    
    print("-" * 80)
    print(f"{'BUSINESS TOTAL':<45} {'':<15} ${business_total:>10,.2f}")
    print(f"{'PERSONAL TOTAL':<45} {'':<15} ${personal_total:>10,.2f}")
    print(f"{'FINANCIAL TOTAL':<45} {'':<15} ${financial_total:>10,.2f}")
    print(f"{'GRAND TOTAL':<45} {'':<15} ${bank_df['Amount'].sum():>10,.2f}")
    
    # Personal spending breakdown
    print("\n" + "="*80)
    print("PERSONAL SPENDING BREAKDOWN BY MERCHANT")
    print("="*80)
    
    personal_df = bank_df[~bank_df['Category'].str.contains('Business|Financial', case=False)]
    merchant_summary = personal_df.groupby('Description').agg({
        'Amount': 'sum',
        'Category': 'first'
    }).reset_index().sort_values('Amount', ascending=False)
    
    print(f"\n{'Merchant':<50} {'Category':<30} {'Total':<10}")
    print("-" * 80)
    
    for _, row in merchant_summary.head(50).iterrows():
        merchant = str(row['Description'])[:48]
        category = str(row['Category']).replace('Personal - ', '')[:28]
        total = row['Amount']
        print(f"{merchant:<50} {category:<30} ${total:>8,.2f}")
    
    # Export results
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    
    # Export full categorized transactions
    export_df = bank_df[['Posted Date', 'Description', 'Amount', 'Category', 'Is_Matched']].copy()
    export_df['Posted Date'] = export_df['Posted Date'].dt.strftime('%Y-%m-%d')
    export_df.to_csv(base_path / 'reports' / 'categorized_spending.csv', index=False)
    
    # Export category summary
    category_summary.to_csv(base_path / 'reports' / 'spending_by_category.csv', index=False)
    
    # Export personal merchant summary
    merchant_summary.to_csv(base_path / 'reports' / 'personal_spending_by_merchant.csv', index=False)
    
    print("\n" + "="*80)
    print("EXPORTS COMPLETE")
    print("="*80)
    print(f"✓ categorized_spending.csv - All transactions with categories")
    print(f"✓ spending_by_category.csv - Summary by category")
    print(f"✓ personal_spending_by_merchant.csv - Personal spending by merchant")
    print()


if __name__ == '__main__':
    analyze_spending()
