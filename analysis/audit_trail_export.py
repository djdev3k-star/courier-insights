"""
Complete Audit Trail Export
Links all 4 sources: Trips → Receipts → Payments → Bank Deposits
"""

import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path('reports/audit_trail')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Generating complete audit trail...")

# Load all data
trips_df = pd.concat([pd.read_csv(f) for f in sorted(Path('data/consolidated/trips').glob('*.csv'))], ignore_index=True)
trips_df['Trip drop off time'] = pd.to_datetime(trips_df['Trip drop off time'], errors='coerce')
trips_df = trips_df[trips_df['Trip status'] == 'completed'].copy()

payments_df = pd.concat([pd.read_csv(f) for f in sorted(Path('data/consolidated/payments').glob('*.csv'))], ignore_index=True)
# Fix date parsing: Remove timezone abbreviation (CDT, CST, etc.) that pandas can't parse
import re
payments_df['vs reporting'] = payments_df['vs reporting'].astype(str).apply(lambda x: re.sub(r'\s+[A-Z]{3}$', '', x))
payments_df['vs reporting'] = pd.to_datetime(payments_df['vs reporting'], errors='coerce', utc=True)

# Calculate Net Earnings - Include ALL payment types
for col in ['Paid to you:Your earnings:Fare:Fare', 'Paid to you:Your earnings:Tip',
            'Paid to you:Trip balance:Refunds:Order Value', 'Paid to you:Your earnings:Promotion:Incentive',
            'Paid to you:Your earnings:Promotion:Boost+', 'Paid to you:Trip balance:Expenses:Instant Pay Fees',
            'Paid to you:Trip balance:Refunds:Toll', 'Paid to you:Your earnings:Fare:Return Trip Fare',
            'Paid to you:Your earnings:Other earnings:Delivery Adjustment', 'Paid to you:Your earnings:Other earnings:Adjustment',
            'Paid to you:Your earnings:Promotion:Quest']:
    if col in payments_df.columns:
        payments_df[col] = pd.to_numeric(payments_df[col], errors='coerce').fillna(0)

payments_df['Total Paid'] = (
    payments_df.get('Paid to you:Your earnings:Fare:Fare', 0) +
    payments_df.get('Paid to you:Your earnings:Tip', 0) +
    payments_df.get('Paid to you:Trip balance:Refunds:Order Value', 0) +
    payments_df.get('Paid to you:Your earnings:Promotion:Incentive', 0) +
    payments_df.get('Paid to you:Your earnings:Promotion:Boost+', 0) +
    payments_df.get('Paid to you:Trip balance:Refunds:Toll', 0) +
    payments_df.get('Paid to you:Your earnings:Fare:Return Trip Fare', 0) +
    payments_df.get('Paid to you:Your earnings:Other earnings:Delivery Adjustment', 0) +
    payments_df.get('Paid to you:Your earnings:Other earnings:Adjustment', 0) +
    payments_df.get('Paid to you:Your earnings:Promotion:Quest', 0)
)
payments_df['Instant Pay Fee'] = payments_df.get('Paid to you:Trip balance:Expenses:Instant Pay Fees', 0)
payments_df['Net Earnings'] = payments_df['Total Paid'] - payments_df['Instant Pay Fee']

bank_list = []
for csv_file in sorted(Path('bank').glob('Uber Pro Card Statement*.csv')):
    df = pd.read_csv(csv_file)
    bank_list.append(df)
bank_df = pd.concat(bank_list, ignore_index=True)
bank_df['Posted Date'] = pd.to_datetime(bank_df['Posted Date'], errors='coerce')
bank_df['Amount'] = bank_df['Amount'].astype(str).str.replace(r'[\$\+,]', '', regex=True)
bank_df['Amount'] = pd.to_numeric(bank_df['Amount'], errors='coerce')

receipts_df = pd.read_csv('data/receipts/Trip Receipts-Refund Tracker.csv')
receipts_df['Date'] = pd.to_datetime(receipts_df['Date'], errors='coerce')
receipts_df['Refund'] = receipts_df['Refund'].astype(str).str.replace(r'[\$,]', '', regex=True)
receipts_df['Refund'] = pd.to_numeric(receipts_df['Refund'], errors='coerce')

# Group payments by Trip UUID
# Remove rows with invalid dates before aggregation
valid_payments = payments_df[payments_df['vs reporting'].notna()].copy()
payment_agg = valid_payments.groupby('Trip UUID').agg({
    'Net Earnings': 'sum',
    'Total Paid': 'sum',
    'Instant Pay Fee': 'sum',
    'vs reporting': 'min'
}).reset_index()
payment_agg.columns = ['Trip UUID', 'Payment Net Earnings', 'Payment Total Paid', 'Payment Instant Pay Fee', 'Payment Date']

# Merge trips with payments
audit_df = trips_df.merge(payment_agg, on='Trip UUID', how='left')

# Add individual refund amounts from enriched bank refund data
try:
    bank_refunds_enriched = pd.read_csv('bank/bank_refund_status_enriched.csv')
    bank_refunds_enriched['Trip UUID'] = bank_refunds_enriched['Trip UUID'].astype(str)
    
    # Get individual refund amounts per trip
    refund_amounts = bank_refunds_enriched.groupby('Trip UUID').agg({
        'Refund Amount': 'sum'  # Sum in case a trip has multiple refunds
    }).reset_index()
    refund_amounts.columns = ['Trip UUID', 'Receipt Refund Amount']
    
    # Merge with audit trail
    audit_df = audit_df.merge(refund_amounts, on='Trip UUID', how='left')
except FileNotFoundError:
    # Fallback: mark if trip has refund from receipts tracker (by date match only)
    audit_df['Trip date'] = audit_df['Trip drop off time'].dt.date
    receipts_df['Receipt date'] = receipts_df['Date'].dt.date
    
    # Get dates with refunds
    refund_dates = set(receipts_df['Receipt date'].dropna())
    audit_df['Receipt Refund Amount'] = audit_df['Trip date'].apply(
        lambda d: 'Has Refund' if d in refund_dates else None
    )

# Add bank deposit matching - just flag if trip's date has a bank deposit
audit_df['Trip date'] = audit_df['Trip drop off time'].dt.date
bank_dates_with_deposits = set(bank_df['Posted Date'].dt.date.dropna())

# Check if trip date or next 3 days have bank deposits
audit_df['Bank Deposit Date'] = audit_df['Trip drop off time'].dt.date.apply(
    lambda trip_date: next(
        (bank_date for bank_date in pd.date_range(trip_date, periods=4).date
         if bank_date in bank_dates_with_deposits),
        None
    ) if pd.notna(trip_date) else None
)

# Create output columns
output_cols = [
    'Trip UUID',
    'Trip drop off time',
    'Pickup address',
    'Drop off address',
    'Trip distance',
    'Service type',
    'Payment Date',
    'Payment Total Paid',
    'Payment Net Earnings',
    'Payment Instant Pay Fee',
    'Receipt Refund Amount',
    'Bank Deposit Date',
    'Reconciliation Status'
]

# Add reconciliation status
def check_status(row):
    has_payment = pd.notna(row['Payment Net Earnings']) and row['Payment Net Earnings'] != 0
    has_refund = pd.notna(row['Receipt Refund Amount']) and row['Receipt Refund Amount'] != 0
    has_bank = pd.notna(row['Bank Deposit Date'])
    
    if not has_payment:
        return 'NO_PAYMENT'
    if has_refund:
        return 'REFUND_TRACKED'
    if has_bank:
        return 'BANK_MATCHED'
    return 'OK'

audit_df['Reconciliation Status'] = audit_df.apply(check_status, axis=1)

# Select and save
output_df = audit_df[output_cols].copy()
output_df = output_df.sort_values('Trip drop off time')

output_df.to_csv(OUTPUT_DIR / 'complete_audit_trail.csv', index=False)

print(f"\n[OK] Saved: complete_audit_trail.csv ({len(output_df)} rows)")
print(f"\nStatus breakdown:")
print(output_df['Reconciliation Status'].value_counts())

# Summary by month
output_df['Month'] = pd.to_datetime(output_df['Trip drop off time']).dt.strftime('%Y-%m')
monthly_audit = output_df.groupby('Month').agg({
    'Trip UUID': 'count',
    'Payment Net Earnings': 'sum',
    'Receipt Refund Amount': lambda x: (pd.to_numeric(x, errors='coerce') > 0).sum(),
    'Bank Deposit Date': lambda x: x.notna().sum()
}).reset_index()
monthly_audit.columns = ['Month', 'Trips', 'Net Earnings', 'Trips with Refunds', 'Trips with Bank Deposits']

monthly_audit.to_csv(OUTPUT_DIR / 'audit_trail_monthly_summary.csv', index=False)

print(f"\n[OK] Saved: audit_trail_monthly_summary.csv")
print("\nMonthly Summary:")
print(monthly_audit.to_string(index=False))

print(f"\n[DONE] Reports saved to {OUTPUT_DIR}/")
