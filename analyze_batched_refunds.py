"""
Quick Batch Analysis - Check if bank payments are batched refunds
"""
import pandas as pd
from pathlib import Path
from datetime import timedelta

# Load all payments
payments = []
for f in Path('data/consolidated/payments').glob('*.csv'):
    payments.append(pd.read_csv(f))
df_pay = pd.concat(payments, ignore_index=True)

# Parse dates and get refunds
df_pay['Date'] = pd.to_datetime(df_pay['vs reporting'].str.split(' -').str[0], errors='coerce')
refund_col = 'Paid to you:Trip balance:Refunds:Order Value'
toll_col = 'Paid to you:Trip balance:Refunds:Toll'

refunds = df_pay[(df_pay[refund_col] > 0) | (df_pay[toll_col] > 0)].copy()
refunds['Amount'] = refunds[refund_col].fillna(0) + refunds[toll_col].fillna(0)
refunds = refunds[refunds['Date'].notna()].sort_values('Date')

# Load bank
bank = []
for f in Path('data/bank').glob('*Statement*.csv'):
    bank.append(pd.read_csv(f))
df_bank = pd.concat(bank, ignore_index=True)
df_bank['Posted Date'] = pd.to_datetime(df_bank['Posted Date'], errors='coerce')
df_bank['Amount'] = pd.to_numeric(df_bank['Amount'].astype(str).str.replace('[\$,]', '', regex=True), errors='coerce')

# Only Uber deposits
uber_bank = df_bank[
    (df_bank['Amount'] > 0) & 
    (df_bank['Description'].str.contains('UBER|Eats', case=False, na=False))
].sort_values('Posted Date')

print("=" * 80)
print("BATCH REFUND ANALYSIS")
print("=" * 80)
print()
print(f"Uber Refunds in Payments: {len(refunds)} transactions, ${refunds['Amount'].sum():,.2f}")
print(f"Uber Deposits in Bank: {len(uber_bank)} deposits, ${uber_bank['Amount'].sum():,.2f}")
print(f"Difference: ${uber_bank['Amount'].sum() - refunds['Amount'].sum():,.2f}")
print()

# Group refunds by month
print("=" * 80)
print("MONTHLY COMPARISON")
print("=" * 80)
for month in sorted(refunds['Date'].dt.to_period('M').unique()):
    month_refunds = refunds[refunds['Date'].dt.to_period('M') == month]
    month_bank = uber_bank[uber_bank['Posted Date'].dt.to_period('M') == month]
    
    refund_sum = month_refunds['Amount'].sum()
    bank_sum = month_bank['Amount'].sum()
    
    print(f"\n{month}:")
    print(f"  Refunds: {len(month_refunds):3} transactions = ${refund_sum:8,.2f}")
    print(f"  Bank:    {len(month_bank):3} deposits     = ${bank_sum:8,.2f}")
    print(f"  Diff:    ${bank_sum - refund_sum:8,.2f}")
    
    # Check for possible batches
    if len(month_bank) < len(month_refunds):
        print(f"  ⚠ Possible batching: {len(month_refunds)} refunds → {len(month_bank)} deposits")
        
        # Try to find batch matches
        for _, deposit in month_bank.iterrows():
            # Find refunds within ±7 days
            date_min = deposit['Posted Date'] - timedelta(days=7)
            date_max = deposit['Posted Date'] + timedelta(days=7)
            nearby = month_refunds[
                (month_refunds['Date'] >= date_min) & 
                (month_refunds['Date'] <= date_max)
            ]
            
            if len(nearby) > 1:
                # Check if any combination sums to deposit
                nearby_sum = nearby['Amount'].sum()
                if abs(nearby_sum - deposit['Amount']) < 1.0:
                    print(f"    BATCH FOUND: {len(nearby)} refunds (${nearby_sum:.2f}) → 1 deposit (${deposit['Amount']:.2f})")
                    print(f"      Date: {deposit['Posted Date'].strftime('%Y-%m-%d')}")

print()
print("=" * 80)
print("DETAILED REFUNDS vs BANK DEPOSITS")
print("=" * 80)

# Show side-by-side
for month in sorted(refunds['Date'].dt.to_period('M').unique()):
    month_refunds = refunds[refunds['Date'].dt.to_period('M') == month]
    month_bank = uber_bank[uber_bank['Posted Date'].dt.to_period('M') == month]
    
    print(f"\n{month}:")
    print(f"\n  REFUNDS ({len(month_refunds)} transactions):")
    for _, r in month_refunds.head(10).iterrows():
        print(f"    {r['Date'].strftime('%m/%d')} | ${r['Amount']:6.2f} | {r['Description'][:50]}")
    if len(month_refunds) > 10:
        print(f"    ... and {len(month_refunds) - 10} more")
    
    print(f"\n  BANK DEPOSITS ({len(month_bank)} deposits):")
    for _, b in month_bank.iterrows():
        print(f"    {b['Posted Date'].strftime('%m/%d')} | ${b['Amount']:8.2f} | {b['Description'][:50]}")

print()
print("✓ Analysis complete")
