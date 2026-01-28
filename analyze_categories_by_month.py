"""
Category Spending Analysis by Month
Shows how spending in each category varied across months
"""

import pandas as pd
from pathlib import Path


def analyze_categories_by_month():
    """Analyze category spending by month"""
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    categorized_file = base_path / 'reports' / 'categorized_spending.csv'
    
    # Load categorized spending
    df = pd.read_csv(categorized_file)
    df['Posted Date'] = pd.to_datetime(df['Posted Date'])
    df['Month'] = df['Posted Date'].dt.to_period('M').astype(str)
    
    print("="*80)
    print("CATEGORY SPENDING BY MONTH")
    print("="*80)
    print()
    
    # Monthly breakdown by category
    monthly_data = []
    
    for month in sorted(df['Month'].unique()):
        month_df = df[df['Month'] == month]
        
        print(f"\n{month}:")
        print("-" * 80)
        print(f"{'Category':<45} {'Transactions':<15} {'Total':<12}")
        print("-" * 80)
        
        category_summary = month_df.groupby('Category').agg({
            'Amount': 'sum',
            'Description': 'count'
        }).reset_index()
        category_summary.columns = ['Category', 'Total', 'Transactions']
        category_summary = category_summary.sort_values('Total', ascending=False)
        
        for _, row in category_summary.iterrows():
            category = row['Category']
            txns = int(row['Transactions'])
            total = row['Total']
            
            print(f"{category:<45} {txns:<15} ${total:>10,.2f}")
            
            monthly_data.append({
                'Month': month,
                'Category': category,
                'Transactions': txns,
                'Total': total
            })
        
        # Month total
        month_total = month_df['Amount'].sum()
        print("-" * 80)
        print(f"{'MONTH TOTAL':<45} {len(month_df):<15} ${month_total:>10,.2f}")
    
    # Category totals across all months
    print("\n" + "="*80)
    print("CATEGORY TOTALS (All Months)")
    print("="*80)
    
    category_totals = df.groupby('Category').agg({
        'Amount': 'sum',
        'Description': 'count'
    }).reset_index()
    category_totals.columns = ['Category', 'Total', 'Transactions']
    category_totals = category_totals.sort_values('Total', ascending=False)
    
    print(f"\n{'Category':<45} {'Transactions':<15} {'Total':<12}")
    print("-" * 80)
    
    for _, row in category_totals.iterrows():
        print(f"{row['Category']:<45} {int(row['Transactions']):<15} ${row['Total']:>10,.2f}")
    
    print("-" * 80)
    print(f"{'GRAND TOTAL':<45} {len(df):<15} ${df['Amount'].sum():>10,.2f}")
    
    # Export to CSV
    monthly_df = pd.DataFrame(monthly_data)
    output_file = base_path / 'reports' / 'category_spending_by_month.csv'
    monthly_df.to_csv(output_file, index=False)
    
    print("\n" + "="*80)
    print(f"✓ Exported to: {output_file}")
    print()
    
    return monthly_df


if __name__ == '__main__':
    analyze_categories_by_month()
