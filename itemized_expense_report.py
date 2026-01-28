"""
Simple Itemized Expense Report - All Bank Expenditures by Month
No analysis, no categorization - just the raw data
"""

import pandas as pd
from pathlib import Path


def generate_itemized_report():
    """Generate itemized expense report by month from bank statements"""
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    
    # Load all bank statements
    print("Loading bank statements...")
    dfs = []
    bank_dir = base_path / 'bank'
    
    for csv_file in sorted(bank_dir.glob('Uber Pro Card Statement*.csv')):
        df = pd.read_csv(csv_file)
        dfs.append(df)
    
    bank_df = pd.concat(dfs, ignore_index=True)
    
    # Parse dates and amounts
    bank_df['Posted Date'] = pd.to_datetime(bank_df['Posted Date'], errors='coerce')
    bank_df['Amount'] = pd.to_numeric(
        bank_df['Amount'].astype(str).str.replace(r'[\$\+,]', '', regex=True),
        errors='coerce'
    )
    
    # Filter to expenses only (negative amounts, excluding Uber deposits)
    expenses = bank_df[bank_df['Amount'] < 0].copy()
    
    # Add month column
    expenses['Month'] = expenses['Posted Date'].dt.to_period('M')
    
    # Sort by date
    expenses = expenses.sort_values('Posted Date')
    
    print("\n" + "="*100)
    print("ITEMIZED EXPENSE REPORT - ALL BANK EXPENDITURES")
    print("="*100)
    
    # Group by month and display
    for month in sorted(expenses['Month'].dropna().unique()):
        month_expenses = expenses[expenses['Month'] == month]
        month_total = abs(month_expenses['Amount'].sum())
        
        print(f"\n{'='*100}")
        print(f"{month} - {len(month_expenses)} transactions - Total: ${month_total:,.2f}")
        print(f"{'='*100}")
        print(f"{'Date':<12} {'Description':<60} {'Amount':>15}")
        print("-"*100)
        
        for _, row in month_expenses.iterrows():
            date_str = row['Posted Date'].strftime('%Y-%m-%d')
            desc = str(row['Description'])[:58]
            amount = f"${abs(row['Amount']):,.2f}"
            print(f"{date_str:<12} {desc:<60} {amount:>15}")
        
        print("-"*100)
        print(f"{'MONTH TOTAL:':<72} ${month_total:>15,.2f}")
    
    # Grand total
    grand_total = abs(expenses['Amount'].sum())
    print(f"\n{'='*100}")
    print(f"{'GRAND TOTAL (ALL MONTHS):':<72} ${grand_total:>15,.2f}")
    print(f"{'TOTAL TRANSACTIONS:':<72} {len(expenses):>15,}")
    print(f"{'='*100}")
    
    # Export to CSV
    output_file = base_path / 'reports' / 'itemized_expenses_by_month.csv'
    output_file.parent.mkdir(exist_ok=True)
    
    export_df = expenses[['Posted Date', 'Description', 'Amount', 'Month']].copy()
    export_df['Amount'] = abs(export_df['Amount'])
    export_df = export_df.sort_values('Posted Date')
    export_df.to_csv(output_file, index=False)
    
    print(f"\n✓ Exported to: {output_file}")
    
    return expenses


if __name__ == '__main__':
    generate_itemized_report()
