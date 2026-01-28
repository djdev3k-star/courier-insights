"""
Analyze Uber Miscellaneous Payments (likely refunds) vs Uber Refund Claims
"""
import pandas as pd
from pathlib import Path

print("=" * 80)
print("UBER MISCELLANEOUS PAYMENTS ANALYSIS")
print("=" * 80)
print()

# Load bank statements
bank_files = list(Path('data/bank').glob('*Statement*.csv'))
all_bank = []
for f in sorted(bank_files):
    df = pd.read_csv(f)
    all_bank.append(df)

bank = pd.concat(all_bank, ignore_index=True)
bank['Posted Date'] = pd.to_datetime(bank['Posted Date'], errors='coerce')
bank['Amount'] = bank['Amount'].astype(str).str.replace('$', '').str.replace('+', '').str.replace(',', '')
bank['Amount'] = pd.to_numeric(bank['Amount'], errors='coerce')

# Filter for Uber payouts
uber_misc = bank[
    (bank['Description'].str.contains('Uber App Payout; Miscellaneous', na=False)) &
    (bank['Amount'] > 0)
].copy()

uber_delivery = bank[
    (bank['Description'].str.contains('Uber App Payout; Delivery', na=False)) &
    (bank['Amount'] > 0)
].copy()

print(f"Uber Delivery Payouts: {len(uber_delivery)} (${uber_delivery['Amount'].sum():,.2f})")
print(f"Uber Miscellaneous Payouts: {len(uber_misc)} (${uber_misc['Amount'].sum():,.2f})")
print()

# Load Uber refund claims from payments
payments_files = list(Path('data/consolidated/payments').glob('*.csv'))
all_payments = []
for f in sorted(payments_files):
    df = pd.read_csv(f)
    all_payments.append(df)

payments = pd.concat(all_payments, ignore_index=True)
payments['Date'] = payments['vs reporting'].str.split(' -').str[0]
payments['Date'] = pd.to_datetime(payments['Date'], errors='coerce')

refund_col = 'Paid to you:Trip balance:Refunds:Order Value'
toll_col = 'Paid to you:Trip balance:Refunds:Toll'

refunds = payments[
    (payments[refund_col] > 0) | (payments[toll_col] > 0)
].copy()

refunds['Refund_Amount'] = refunds[refund_col].fillna(0) + refunds[toll_col].fillna(0)
refunds = refunds[refunds['Date'].notna()]

print(f"Uber Refund Claims: {len(refunds)} (${refunds['Refund_Amount'].sum():,.2f})")
print()

# Compare by month
print("=" * 80)
print("MONTHLY COMPARISON")
print("=" * 80)
print()

for month in sorted(refunds['Date'].dt.to_period('M').unique()):
    month_label = month.strftime('%B %Y')
    
    month_refunds = refunds[refunds['Date'].dt.to_period('M') == month]
    month_misc = uber_misc[uber_misc['Posted Date'].dt.to_period('M') == month]
    
    refund_sum = month_refunds['Refund_Amount'].sum()
    misc_sum = month_misc['Amount'].sum()
    
    print(f"{month_label}:")
    print(f"  Uber Claims (Refunds):      {len(month_refunds):3} txns = ${refund_sum:8,.2f}")
    print(f"  Bank (Miscellaneous):       {len(month_misc):3} txns = ${misc_sum:8,.2f}")
    print(f"  Difference:                                ${misc_sum - refund_sum:8,.2f}")
    
    if abs(misc_sum - refund_sum) < 5.0:
        print(f"  ✓ MATCH - Miscellaneous payments match refund claims!")
    elif misc_sum > refund_sum:
        print(f"  ⚠ Bank received MORE than Uber claims")
    else:
        print(f"  ⚠ Bank received LESS than Uber claims")
    
    print()

# Overall comparison
print("=" * 80)
print("OVERALL SUMMARY")
print("=" * 80)
print()

total_refunds = refunds['Refund_Amount'].sum()
total_misc = uber_misc['Amount'].sum()

print(f"Total Uber Refund Claims:        ${total_refunds:,.2f}")
print(f"Total Bank Miscellaneous:        ${total_misc:,.2f}")
print(f"Difference:                      ${total_misc - total_refunds:,.2f}")
print()

if abs(total_misc - total_refunds) < 10.0:
    print("✓ SUCCESS: Bank Miscellaneous payments match Uber refund claims!")
    print("  The 'Miscellaneous' category in bank = Customer reimbursements")
else:
    print(f"⚠ Discrepancy of ${abs(total_misc - total_refunds):.2f}")

# Show sample transactions
print()
print("=" * 80)
print("SAMPLE UBER MISCELLANEOUS PAYMENTS (First 20)")
print("=" * 80)
print()

for _, row in uber_misc.head(20).iterrows():
    date = row['Posted Date'].strftime('%Y-%m-%d')
    amt = row['Amount']
    print(f"{date} | ${amt:6.2f} | Uber App Payout; Miscellaneous")

print()
print("✓ Analysis complete")
print()
print("Export data...")

# Export for verification
uber_misc.to_csv('uber_miscellaneous_payments.csv', index=False)
refunds[['Date', 'Description', 'Refund_Amount']].to_csv('uber_refund_claims.csv', index=False)

print("  ✓ uber_miscellaneous_payments.csv")
print("  ✓ uber_refund_claims.csv")
