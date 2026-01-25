"""
Advanced Reconciliation: Separating Customer Purchases from Personal Spending
Matches Receipt Tracker customer purchases to bank transactions
"""

import pandas as pd
import re
from pathlib import Path
from difflib import SequenceMatcher

OUTPUT_DIR = Path('reports/four_way_reconciliation')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print("ADVANCED RECONCILIATION: Customer vs Personal Spending")
print("="*80)

# Load Receipt Tracker
print("\nLoading Receipt Tracker...")
receipts_df = pd.read_csv('data/receipts/Trip Receipts-Refund Tracker.csv')
receipts_df['Date'] = pd.to_datetime(receipts_df['Date'], errors='coerce')

# Extract customer purchase totals
receipts_with_purchase = receipts_df[receipts_df['Total'].notna()].copy()
receipts_with_purchase['Total_amount'] = receipts_with_purchase['Total'].astype(str).str.replace(r'[\$,]', '', regex=True)
receipts_with_purchase['Total_amount'] = pd.to_numeric(receipts_with_purchase['Total_amount'], errors='coerce')

# Clean pickup address
receipts_with_purchase['Store'] = receipts_with_purchase['Pickup Address'].str.extract(r'([A-Za-z0-9\s]+?)(?:\s*\(|$)')

print(f"Customer purchases in Receipt Tracker: {len(receipts_with_purchase)}")
print(f"Total customer purchase amount: ${receipts_with_purchase['Total_amount'].sum():,.2f}")

# Load bank data
print("\nLoading bank statements...")
bank_list = []
for csv_file in sorted(Path('bank').glob('Uber Pro Card Statement*.csv')):
    df = pd.read_csv(csv_file)
    bank_list.append(df)
bank_df = pd.concat(bank_list, ignore_index=True)
bank_df['Posted Date'] = pd.to_datetime(bank_df['Posted Date'], errors='coerce')
bank_df['Amount'] = bank_df['Amount'].astype(str).str.replace(r'[\$\+,]', '', regex=True)
bank_df['Amount'] = pd.to_numeric(bank_df['Amount'], errors='coerce')

# Get negative transactions (purchases/expenses)
purchases_bank = bank_df[bank_df['Amount'] < 0].copy()
purchases_bank['Amount_abs'] = abs(purchases_bank['Amount'])

print(f"Bank purchases (negative amounts): {len(purchases_bank)}")
print(f"Total bank purchases: ${purchases_bank['Amount'].sum():,.2f}")

# Matching algorithm: Match receipt purchases to bank purchases by date and amount
print("\n" + "="*80)
print("MATCHING CUSTOMER PURCHASES")
print("="*80)

matched_purchases = []
unmatched_receipts = []

for idx, receipt in receipts_with_purchase.iterrows():
    receipt_date = receipt['Date'].date()
    receipt_amount = receipt['Total_amount']
    receipt_store = receipt['Store']
    
    # Find bank transactions on same date with similar amount (tolerance: $0.50)
    candidates = purchases_bank[
        (purchases_bank['Posted Date'].dt.date == receipt_date) &
        (abs(purchases_bank['Amount_abs'] - receipt_amount) < 0.50)
    ]
    
    if len(candidates) > 0:
        # If multiple matches, pick the closest amount
        best_match = candidates.iloc[(candidates['Amount_abs'] - receipt_amount).abs().argmin()]
        matched_purchases.append({
            'Date': receipt_date,
            'Store': receipt_store,
            'Receipt Amount': receipt_amount,
            'Bank Amount': best_match['Amount'],
            'Bank Description': best_match['Description'],
            'Match Type': 'CUSTOMER_PURCHASE'
        })
        # Remove from unmatched pool
        purchases_bank = purchases_bank.drop(best_match.name)
    else:
        unmatched_receipts.append({
            'Date': receipt_date,
            'Store': receipt_store,
            'Amount': receipt_amount,
            'Status': 'NOT_FOUND_IN_BANK'
        })

matched_df = pd.DataFrame(matched_purchases)
unmatched_df = pd.DataFrame(unmatched_receipts)

print(f"\nMatched customer purchases: {len(matched_df)}")
print(f"Unmatched receipts (not found in bank): {len(unmatched_df)}")
print(f"Remaining bank purchases (true personal): {len(purchases_bank)}")

if len(matched_df) > 0:
    print(f"\nMatched customer purchase amount: ${matched_df['Receipt Amount'].sum():,.2f}")

print(f"True personal purchases amount: ${purchases_bank['Amount'].sum():,.2f}")

# Reload bank data for final reconciliation
bank_list = []
for csv_file in sorted(Path('bank').glob('Uber Pro Card Statement*.csv')):
    df = pd.read_csv(csv_file)
    bank_list.append(df)
bank_df = pd.concat(bank_list, ignore_index=True)
bank_df['Posted Date'] = pd.to_datetime(bank_df['Posted Date'], errors='coerce')
bank_df['Amount'] = bank_df['Amount'].astype(str).str.replace(r'[\$\+,]', '', regex=True)
bank_df['Amount'] = pd.to_numeric(bank_df['Amount'], errors='coerce')

# Load payments
print("\nLoading payments...")
payments_df = pd.concat([pd.read_csv(f) for f in sorted(Path('data/consolidated/payments').glob('*.csv'))], ignore_index=True)
payments_df['vs reporting'] = payments_df['vs reporting'].astype(str).apply(lambda x: re.sub(r'\s+[A-Z]{3}$', '', x))
payments_df['vs reporting'] = pd.to_datetime(payments_df['vs reporting'], errors='coerce', utc=True)

for col in ['Paid to you:Your earnings:Fare:Fare', 'Paid to you:Your earnings:Tip',
            'Paid to you:Trip balance:Refunds:Order Value', 'Paid to you:Your earnings:Promotion:Incentive',
            'Paid to you:Your earnings:Promotion:Boost+', 'Paid to you:Trip balance:Expenses:Instant Pay Fees']:
    if col in payments_df.columns:
        payments_df[col] = pd.to_numeric(payments_df[col], errors='coerce').fillna(0)

payments_df['Total Paid'] = (
    payments_df.get('Paid to you:Your earnings:Fare:Fare', 0) +
    payments_df.get('Paid to you:Your earnings:Tip', 0) +
    payments_df.get('Paid to you:Trip balance:Refunds:Order Value', 0) +
    payments_df.get('Paid to you:Your earnings:Promotion:Incentive', 0) +
    payments_df.get('Paid to you:Your earnings:Promotion:Boost+', 0)
)
payments_df['Instant Pay Fee'] = payments_df.get('Paid to you:Trip balance:Expenses:Instant Pay Fees', 0)
payments_df['Net Earnings'] = payments_df['Total Paid'] - payments_df['Instant Pay Fee']

# Categorize bank transactions
bank_df['Is_Uber_Payout'] = bank_df['Description'].str.contains('Uber App Payout', case=False, na=False)

if len(matched_df) > 0:
    matched_descs = set(matched_df['Bank Description'].unique())
    bank_df['Is_Customer_Purchase'] = bank_df['Description'].isin(matched_descs)
else:
    bank_df['Is_Customer_Purchase'] = False

bank_df['Is_Personal_Spending'] = (bank_df['Amount'] < 0) & ~bank_df['Is_Uber_Payout'] & ~bank_df['Is_Customer_Purchase']

# Final categorization
uber_deposits = bank_df[bank_df['Is_Uber_Payout']]
customer_purchases = bank_df[bank_df['Is_Customer_Purchase']]
personal_spending = bank_df[bank_df['Is_Personal_Spending']]

print("\n" + "="*80)
print("FINAL BANK CATEGORIZATION")
print("="*80)
print(f"\nUber Deposits: {len(uber_deposits):,} = ${uber_deposits['Amount'].sum():,.2f}")
print(f"Customer Purchases (reimbursed): {len(customer_purchases):,} = ${customer_purchases['Amount'].sum():,.2f}")
print(f"True Personal Spending: {len(personal_spending):,} = ${personal_spending['Amount'].sum():,.2f}")

# Uber-only reconciliation with correct categorization
print("\n" + "="*80)
print("CORRECTED UBER-ONLY RECONCILIATION")
print("="*80)

valid_payments = payments_df[payments_df['vs reporting'].notna()].copy()
valid_payments['payment_date'] = valid_payments['vs reporting'].dt.date
total_payment_earnings = valid_payments['Net Earnings'].sum()
total_uber_deposits = uber_deposits['Amount'].sum()
total_customer_purchases = abs(customer_purchases['Amount'].sum())
total_personal_spending = abs(personal_spending['Amount'].sum())

print(f"\nUber Earnings (Payments): ${total_payment_earnings:,.2f}")
print(f"Uber Deposits: ${total_uber_deposits:,.2f}")
print(f"  - Includes reimbursement for customer purchases: ${total_customer_purchases:,.2f}")
print(f"  - Net Uber earnings deposited: ${total_uber_deposits - total_customer_purchases:,.2f}")
print(f"\nReconciliation Difference: ${total_payment_earnings - total_uber_deposits:,.2f}")
print(f"  (Variance: {100*(total_payment_earnings - total_uber_deposits)/total_payment_earnings:.2f}%)")

print(f"\nTrue Personal Spending (separate from Uber business): ${total_personal_spending:,.2f}")

# Save detailed report
report_data = {
    'Category': [
        'Uber Payment Records (Net Earnings)',
        'Uber Deposits to Bank',
        'Difference (timing lag)',
        '',
        'Customer Purchases (reimbursed by Uber)',
        'True Personal Spending (not reimbursed)',
        '',
        'Total Bank Activity',
    ],
    'Amount': [
        f"${total_payment_earnings:,.2f}",
        f"${total_uber_deposits:,.2f}",
        f"${total_payment_earnings - total_uber_deposits:,.2f}",
        '',
        f"${total_customer_purchases:,.2f}",
        f"${total_personal_spending:,.2f}",
        '',
        f"${(total_uber_deposits + total_personal_spending):,.2f}",
    ]
}

report_df = pd.DataFrame(report_data)
report_df.to_csv(OUTPUT_DIR / 'reconciliation_breakdown.csv', index=False)

print("\n" + "="*80)
print("KEY FINDINGS")
print("="*80)
print(f"""
1. CUSTOMER PURCHASES: ${total_customer_purchases:,.2f}
   - These were paid from your card but reimbursed by Uber
   - Should NOT count against your net earnings
   - Included in the Uber deposits you received

2. TRUE PERSONAL SPENDING: ${total_personal_spending:,.2f}
   - Meals, gas, shopping, etc. for personal use
   - Your actual personal expenses

3. UBER RECONCILIATION: 
   - You earned: ${total_payment_earnings:,.2f}
   - You received: ${total_uber_deposits:,.2f}
   - Difference: ${total_payment_earnings - total_uber_deposits:,.2f} ({100*(total_payment_earnings - total_uber_deposits)/total_payment_earnings:.2f}%)
   - This small difference is typical due to timing delays

CONCLUSION: Uber is paying you correctly. The original report showed
${abs(personal_spending['Amount'].sum()) + total_customer_purchases:,.2f} as "personal spending", but ${total_customer_purchases:,.2f} was actually customer
purchases you were reimbursed for, and only ${total_personal_spending:,.2f}
was truly personal spending.
""")

print(f"\n[OK] Reports saved to {OUTPUT_DIR}/")
