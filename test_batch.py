import pandas as pd
from pathlib import Path

print("Starting batch reconciliation...")

# Load refunds
payments_path = Path('data/consolidated/payments')
all_payments = []

for csv_file in sorted(payments_path.glob('*.csv')):
    df = pd.read_csv(csv_file)
    all_payments.append(df)

combined = pd.concat(all_payments, ignore_index=True)
print(f"Loaded {len(combined)} payment records")

# Parse dates
combined['Date'] = combined['vs reporting'].str.split(' -').str[0]
combined['Date'] = pd.to_datetime(combined['Date'], errors='coerce')

# Get refunds
refund_order_col = 'Paid to you:Trip balance:Refunds:Order Value'
refund_toll_col = 'Paid to you:Trip balance:Refunds:Toll'

refunds = combined[
    (combined[refund_order_col] > 0) | (combined[refund_toll_col] > 0)
].copy()

refunds['Refund_Amount'] = (
    refunds[refund_order_col].fillna(0) + 
    refunds[refund_toll_col].fillna(0)
)

refunds = refunds[refunds['Date'].notna()]

print(f"Found {len(refunds)} refund transactions")
print(f"Total refunds: ${refunds['Refund_Amount'].sum():,.2f}")

# Load bank
bank_path = Path('data/bank')
all_statements = []

for csv_file in sorted(bank_path.glob('*.csv')):
    if 'Statement' in csv_file.name:
        df = pd.read_csv(csv_file)
        all_statements.append(df)

bank = pd.concat(all_statements, ignore_index=True)
bank['Posted Date'] = pd.to_datetime(bank['Posted Date'], errors='coerce')
bank['Amount'] = pd.to_numeric(
    bank['Amount'].astype(str).str.replace('$', '').str.replace(',', ''), 
    errors='coerce'
)

deposits = bank[bank['Amount'] > 0]
print(f"Found {len(deposits)} bank deposits")

# Find Uber deposits
uber_keywords = ['uber', 'eats', 'technologies']
uber_deposits = deposits[
    deposits['Description'].astype(str).str.lower().str.contains('|'.join(uber_keywords), na=False)
]

print(f"Uber-related deposits: {len(uber_deposits)}")
print(f"Total Uber deposit amount: ${uber_deposits['Amount'].sum():,.2f}")

print("\nDone!")
