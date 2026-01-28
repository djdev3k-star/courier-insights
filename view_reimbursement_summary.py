import pandas as pd

df = pd.read_csv('reimbursement_reconciliation.csv')

print('=' * 80)
print('REIMBURSEMENT RECONCILIATION SUMMARY')
print('=' * 80)
print()

print(f'Total Transactions: {len(df)}')
print()
print(f'Uber Claims: ${df["Uber_Amount"].sum():,.2f}')
bank_received = df[df["Bank_Match"] == "Yes"]["Bank_Amount"].sum()
print(f'Bank Received: ${bank_received:,.2f}')
print(f'Difference: ${bank_received - df["Uber_Amount"].sum():,.2f}')
print()

receipt_matches = len(df[df["Receipt_Match"] == "Yes"])
bank_matches = len(df[df["Bank_Match"] == "Yes"])

print(f'Receipt Tracker Matches: {receipt_matches}/{len(df)} ({receipt_matches/len(df)*100:.1f}%)')
print(f'Bank Payment Matches: {bank_matches}/{len(df)} ({bank_matches/len(df)*100:.1f}%)')
print()

print('=' * 80)
print('TOP 10 REIMBURSEMENTS')
print('=' * 80)
print()

top10 = df.nlargest(10, 'Uber_Amount')[['Date', 'Description', 'Uber_Amount', 'Receipt_Match', 'Bank_Match', 'Bank_Amount']]
for _, row in top10.iterrows():
    date = pd.to_datetime(row['Date']).strftime('%Y-%m-%d')
    desc = row['Description'][:40]
    uber_amt = row['Uber_Amount']
    receipt = '✓' if row['Receipt_Match'] == 'Yes' else '✗'
    bank = '✓' if row['Bank_Match'] == 'Yes' else '✗'
    bank_amt = row['Bank_Amount'] if pd.notna(row['Bank_Amount']) else 0
    
    print(f'{date} | ${uber_amt:6.2f} → ${bank_amt:6.2f} | Receipt:{receipt} Bank:{bank} | {desc}')

print()
print('=' * 80)
print('MONTHLY BREAKDOWN')
print('=' * 80)
print()

for month in sorted(df['Month'].unique()):
    month_data = df[df['Month'] == month]
    month_label = pd.to_datetime(month + '-01').strftime('%B %Y')
    
    uber_total = month_data['Uber_Amount'].sum()
    bank_total = month_data[month_data['Bank_Match'] == 'Yes']['Bank_Amount'].sum()
    receipt_pct = len(month_data[month_data['Receipt_Match'] == 'Yes']) / len(month_data) * 100
    
    print(f'{month_label:15} | {len(month_data):2} txns | Uber: ${uber_total:7.2f} | Bank: ${bank_total:7.2f} | Receipt Match: {receipt_pct:5.1f}%')
