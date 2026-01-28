"""
Merchant Summary by First 7 Characters - Grouped by Month
Consolidates similar merchants (chains, brands) by prefix matching
"""

import pandas as pd
from pathlib import Path


def generate_merchant_prefix_summary():
    """Group merchants by first 7 characters and summarize by month"""
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    expenses_file = base_path / 'reports' / 'itemized_expenses_by_month.csv'
    
    # Load itemized expenses
    df = pd.read_csv(expenses_file)
    df['Posted Date'] = pd.to_datetime(df['Posted Date'])
    df['Month'] = pd.to_datetime(df['Month'])
    
    # Extract first 7 characters of merchant description
    df['Merchant_Prefix'] = df['Description'].str[:7].str.strip()
    
    print("="*80)
    print("MERCHANT SUMMARY BY PREFIX (First 7 Characters) - GROUPED BY MONTH")
    print("="*80)
    print()
    
    # Summary by month
    monthly_summary = []
    
    for month in sorted(df['Month'].unique()):
        month_data = df[df['Month'] == month]
        month_str = month.strftime('%Y-%m')
        
        # Group by prefix
        grouped = month_data.groupby('Merchant_Prefix').agg({
            'Amount': ['sum', 'count'],
            'Description': 'first'  # Get one example
        }).reset_index()
        
        grouped.columns = ['Prefix', 'Total', 'Transactions', 'Example']
        grouped = grouped.sort_values('Total', ascending=False)
        
        print(f"\n{month.strftime('%B %Y')} - {len(grouped)} unique prefixes - {len(month_data)} transactions - ${month_data['Amount'].sum():,.2f}")
        print(f"{'Prefix':<10} {'Example Merchant':<45} {'Visits':<8} {'Total':<10}")
        print("-" * 80)
        
        for _, row in grouped.head(30).iterrows():  # Top 30 per month
            prefix = row['Prefix']
            example = str(row['Example'])[:45]
            visits = int(row['Transactions'])
            total = row['Total']
            
            print(f"{prefix:<10} {example:<45} {visits}x{' '*(6-len(str(visits)))} ${total:>8,.2f}")
            
            # Add to monthly summary
            monthly_summary.append({
                'Month': month_str,
                'Prefix': prefix,
                'Example_Merchant': row['Example'],
                'Transactions': visits,
                'Total': total
            })
    
    # Overall summary - most visited prefixes
    print("\n" + "="*80)
    print("OVERALL SUMMARY - MOST VISITED MERCHANT PREFIXES (All Months)")
    print("="*80)
    
    overall = df.groupby('Merchant_Prefix').agg({
        'Amount': ['sum', 'count'],
        'Description': 'first'
    }).reset_index()
    
    overall.columns = ['Prefix', 'Total', 'Transactions', 'Example']
    overall = overall.sort_values('Transactions', ascending=False).head(30)
    
    print(f"\n{'Prefix':<10} {'Example Merchant':<45} {'Visits':<8} {'Total':<10}")
    print("-" * 80)
    
    for _, row in overall.iterrows():
        prefix = row['Prefix']
        example = str(row['Example'])[:45]
        visits = int(row['Transactions'])
        total = row['Total']
        
        print(f"{prefix:<10} {example:<45} {visits}x{' '*(6-len(str(visits)))} ${total:>8,.2f}")
    
    # Export to CSV
    summary_df = pd.DataFrame(monthly_summary)
    output_file = base_path / 'reports' / 'merchant_by_prefix_monthly.csv'
    summary_df.to_csv(output_file, index=False)
    
    print("\n" + "="*80)
    print("ACCOUNTING SUMMARY")
    print("="*80)
    print(f"Total Spending: ${df['Amount'].sum():,.2f}")
    print(f"Total Transactions: {len(df)}")
    print(f"Unique Prefixes: {df['Merchant_Prefix'].nunique()}")
    print(f"Average per Prefix: ${df.groupby('Merchant_Prefix')['Amount'].sum().mean():,.2f}")
    print()
    print(f"✓ Exported to: {output_file}")
    print()
    
    return summary_df


if __name__ == '__main__':
    generate_merchant_prefix_summary()
