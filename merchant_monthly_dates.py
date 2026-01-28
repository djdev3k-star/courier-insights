"""
Generate Monthly Merchant Report with Latest Charge Date
Shows merchants grouped by month with their most recent transaction date
"""

import pandas as pd
from pathlib import Path


def generate_monthly_merchant_report():
    """Generate report of merchants by month with latest charge date"""
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    expenses_file = base_path / 'reports' / 'itemized_expenses_by_month.csv'
    
    # Load expenses
    df = pd.read_csv(expenses_file)
    df['Posted Date'] = pd.to_datetime(df['Posted Date'])
    df['Month'] = pd.to_datetime(df['Month'])
    
    print("="*80)
    print("MERCHANT ACTIVITY BY MONTH - WITH LATEST CHARGE DATE")
    print("="*80)
    print()
    
    # Process by month
    monthly_data = []
    
    for month in sorted(df['Month'].unique()):
        month_data = df[df['Month'] == month]
        month_str = month.strftime('%B %Y')
        
        # Group by merchant
        merchant_groups = month_data.groupby('Description').agg({
            'Posted Date': ['max', 'count'],  # Latest date and count
            'Amount': 'sum'
        }).reset_index()
        
        merchant_groups.columns = ['Merchant', 'Latest_Date', 'Transactions', 'Total']
        merchant_groups = merchant_groups.sort_values('Total', ascending=False)
        
        print(f"\n{month_str}")
        print(f"Total: ${month_data['Amount'].sum():,.2f} | {len(month_data)} transactions | {len(merchant_groups)} unique merchants")
        print("-" * 80)
        print(f"{'Merchant':<50} {'Latest':<12} {'Visits':<8} {'Total':<10}")
        print("-" * 80)
        
        for _, row in merchant_groups.iterrows():
            merchant = str(row['Merchant'])[:48]
            latest = row['Latest_Date'].strftime('%m/%d/%Y')
            visits = int(row['Transactions'])
            total = row['Total']
            
            print(f"{merchant:<50} {latest:<12} {visits}x{' '*(6-len(str(visits)))} ${total:>8,.2f}")
            
            # Store for CSV
            monthly_data.append({
                'Month': month_str,
                'Merchant': row['Merchant'],
                'Latest_Charge_Date': latest,
                'Transactions': visits,
                'Total_Spent': total,
                'First_Charge_Date': month_data[month_data['Description'] == row['Merchant']]['Posted Date'].min().strftime('%m/%d/%Y')
            })
    
    # Export to CSV
    export_df = pd.DataFrame(monthly_data)
    output_file = base_path / 'reports' / 'merchant_by_month_with_dates.csv'
    export_df.to_csv(output_file, index=False)
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total Spending: ${df['Amount'].sum():,.2f}")
    print(f"Total Transactions: {len(df)}")
    print(f"Total Unique Merchants: {df['Description'].nunique()}")
    print(f"Months Covered: {df['Month'].nunique()}")
    print()
    print(f"✓ Exported to: {output_file}")
    print()
    
    return export_df


if __name__ == '__main__':
    generate_monthly_merchant_report()
