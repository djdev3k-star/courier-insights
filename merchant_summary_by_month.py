"""
Merchant Summary Report - Group repeat merchants by month
Shows frequency and total spending per merchant for accounting purposes
"""

import pandas as pd
from pathlib import Path


def generate_merchant_summary():
    """Generate merchant summary report grouped by month"""
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    
    # Load itemized expenses
    print("Loading itemized expenses...")
    expenses_file = base_path / 'reports' / 'itemized_expenses_by_month.csv'
    df = pd.read_csv(expenses_file)
    
    # Parse dates
    df['Posted Date'] = pd.to_datetime(df['Posted Date'])
    df['Month'] = pd.to_datetime(df['Month'])
    
    print("\n" + "="*100)
    print("MERCHANT SUMMARY BY MONTH - REPEAT VISITS GROUPED")
    print("="*100)
    
    # Group by month
    for month in sorted(df['Month'].unique()):
        month_data = df[df['Month'] == month]
        
        # Group by merchant
        merchant_summary = month_data.groupby('Description').agg({
            'Amount': ['sum', 'count']
        }).reset_index()
        
        merchant_summary.columns = ['Merchant', 'Total', 'Transactions']
        merchant_summary = merchant_summary.sort_values('Total', ascending=False)
        
        month_total = month_data['Amount'].sum()
        month_str = month.strftime('%Y-%m')
        
        print(f"\n{'='*100}")
        print(f"{month_str} - {len(merchant_summary)} unique merchants - {len(month_data)} transactions - ${month_total:,.2f}")
        print(f"{'='*100}")
        print(f"{'Merchant':<65} {'Visits':>8} {'Total':>15}")
        print("-"*100)
        
        for _, row in merchant_summary.iterrows():
            merchant = str(row['Merchant'])[:63]
            visits = int(row['Transactions'])
            total = row['Total']
            
            # Add notation for repeat visits
            if visits > 1:
                visit_note = f"{visits}x"
            else:
                visit_note = "1x"
            
            print(f"{merchant:<65} {visit_note:>8} ${total:>14,.2f}")
        
        print("-"*100)
        print(f"{'MONTH TOTAL:':<65} {len(month_data):>8} ${month_total:>14,.2f}")
    
    # Grand summary - most visited merchants overall
    print(f"\n{'='*100}")
    print("OVERALL SUMMARY - MOST VISITED MERCHANTS (All Months)")
    print(f"{'='*100}")
    
    overall_summary = df.groupby('Description').agg({
        'Amount': ['sum', 'count']
    }).reset_index()
    overall_summary.columns = ['Merchant', 'Total', 'Transactions']
    overall_summary = overall_summary.sort_values('Transactions', ascending=False).head(30)
    
    print(f"{'Merchant':<65} {'Visits':>8} {'Total':>15}")
    print("-"*100)
    
    for _, row in overall_summary.iterrows():
        merchant = str(row['Merchant'])[:63]
        visits = int(row['Transactions'])
        total = row['Total']
        print(f"{merchant:<65} {visits:>8}x ${total:>14,.2f}")
    
    # Export detailed summary
    output_file = base_path / 'reports' / 'merchant_summary_by_month.csv'
    
    # Create detailed export with month grouping
    export_data = []
    for month in sorted(df['Month'].unique()):
        month_data = df[df['Month'] == month]
        merchant_summary = month_data.groupby('Description').agg({
            'Amount': ['sum', 'count']
        }).reset_index()
        merchant_summary.columns = ['Merchant', 'Total', 'Transactions']
        merchant_summary['Month'] = month.strftime('%Y-%m')
        merchant_summary = merchant_summary.sort_values('Total', ascending=False)
        export_data.append(merchant_summary)
    
    export_df = pd.concat(export_data, ignore_index=True)
    export_df = export_df[['Month', 'Merchant', 'Transactions', 'Total']]
    export_df.to_csv(output_file, index=False)
    
    print(f"\n{'='*100}")
    print(f"✓ Exported to: {output_file}")
    print(f"{'='*100}")
    
    # Summary stats
    grand_total = df['Amount'].sum()
    total_merchants = df['Description'].nunique()
    total_transactions = len(df)
    
    print(f"\nACCOUNTING SUMMARY:")
    print(f"  Total Spending: ${grand_total:,.2f}")
    print(f"  Total Transactions: {total_transactions}")
    print(f"  Unique Merchants: {total_merchants}")
    print(f"  Average Transaction: ${grand_total/total_transactions:,.2f}")
    print(f"  Average per Merchant: ${grand_total/total_merchants:,.2f}")


if __name__ == '__main__':
    generate_merchant_summary()
