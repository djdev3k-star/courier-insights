"""
Four-Way Reconciliation: Trips ↔ Payments ↔ Bank ↔ Receipts Tracker
Ignores paid status, double-checks all four sources for discrepancies
"""

import pandas as pd
from pathlib import Path
from datetime import timedelta
import re

OUTPUT_DIR = Path('reports/four_way_reconciliation')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("FOUR-WAY RECONCILIATION ANALYSIS")
print("Trips <> Payments <> Bank <> Receipts Tracker")
print("=" * 80)

# Load all four data sources
print("\nLoading data sources...")
trips_df = pd.concat([pd.read_csv(f) for f in sorted(Path('data/consolidated/trips').glob('*.csv'))], ignore_index=True)
trips_df['Trip drop off time'] = pd.to_datetime(trips_df['Trip drop off time'], errors='coerce')
trips_df = trips_df[trips_df['Trip status'] == 'completed'].copy()

payments_df = pd.concat([pd.read_csv(f) for f in sorted(Path('data/consolidated/payments').glob('*.csv'))], ignore_index=True)
# Fix date parsing: Remove timezone abbreviation (CDT, CST, etc.) that pandas can't parse
import re
payments_df['vs reporting'] = payments_df['vs reporting'].astype(str).apply(lambda x: re.sub(r'\s+[A-Z]{3}$', '', x))
payments_df['vs reporting'] = pd.to_datetime(payments_df['vs reporting'], errors='coerce', utc=True)

# Parse payment columns for Net Earnings calculation (include ALL payment types)
for col in ['Paid to you:Your earnings:Fare:Fare', 'Paid to you:Your earnings:Tip',
            'Paid to you:Trip balance:Refunds:Order Value', 'Paid to you:Your earnings:Promotion:Incentive',
            'Paid to you:Your earnings:Promotion:Boost+', 'Paid to you:Trip balance:Expenses:Instant Pay Fees',
            'Paid to you:Trip balance:Refunds:Toll', 'Paid to you:Your earnings:Fare:Return Trip Fare',
            'Paid to you:Your earnings:Other earnings:Delivery Adjustment', 'Paid to you:Your earnings:Other earnings:Adjustment',
            'Paid to you:Your earnings:Promotion:Quest']:
    if col in payments_df.columns:
        payments_df[col] = pd.to_numeric(payments_df[col], errors='coerce').fillna(0)

# Calculate Net Earnings per transaction (include ALL payment types)
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
# Filter to ONLY Uber deposits for reconciliation (ignore personal purchases/spending on the shared card)
bank_df = bank_df[bank_df['Description'].str.contains('Uber App Payout', case=False, na=False)].copy()

receipts_df = pd.read_csv('data/receipts/Trip Receipts-Refund Tracker.csv')
receipts_df['Date'] = pd.to_datetime(receipts_df['Date'], errors='coerce')
receipts_df['Refund'] = receipts_df['Refund'].astype(str).str.replace(r'[\$,]', '', regex=True)
receipts_df['Refund'] = pd.to_numeric(receipts_df['Refund'], errors='coerce')

# Extract Trip UUID from Uber Link when present
def extract_trip_uuid(link: str):
    if pd.isna(link):
        return None
    match = re.search(r'/trips/([0-9a-fA-F-]{8,})', str(link))
    return match.group(1) if match else None

receipts_df['Trip UUID'] = receipts_df.get('Uber Link', '').apply(extract_trip_uuid)

print(f"  Trips: {len(trips_df):,}")
print(f"  Payments: {len(payments_df):,}")
print(f"  Bank Transactions: {len(bank_df):,}")
print(f"  Receipts Tracker: {len(receipts_df):,}")

# === 1. Trips ↔ Receipts Tracker ===
print("\n" + "=" * 80)
print("1. TRIPS vs RECEIPTS TRACKER")
print("=" * 80)

receipts_with_trip_data = receipts_df.dropna(subset=['Date']).copy()
print(f"\nReceipts with dates: {len(receipts_with_trip_data)}")
print(f"  - With Refund values: {receipts_with_trip_data['Refund'].notna().sum()}")
print(f"  - With Fare values: {receipts_with_trip_data['Fare'].notna().sum()}")
print(f"  - With Tip values: {receipts_with_trip_data['Tip'].notna().sum()}")

# Try to match by Trip UUID first, then by date
trips_by_date = trips_df.copy()
trips_by_date['Trip_date_only'] = trips_by_date['Trip drop off time'].dt.date

receipts_unmatched = []
receipt_matches = []

for idx, receipt in receipts_with_trip_data.iterrows():
    receipt_date = receipt['Date'].date()
    trip_uuid = receipt.get('Trip UUID')

    matched_row = None
    # UUID match
    if pd.notna(trip_uuid):
        uuid_match = trips_df[trips_df['Trip UUID'] == trip_uuid]
        if not uuid_match.empty:
            matched_row = uuid_match.iloc[0]

    # Date match fallback
    if matched_row is None:
        matching_trips = trips_by_date[trips_by_date['Trip_date_only'] == receipt_date]
        if len(matching_trips) > 0:
            matched_row = matching_trips.iloc[0]

    if matched_row is not None:
        receipt_matches.append({
            'Receipt Index': idx,
            'Trip UUID': matched_row['Trip UUID'],
            'Trip drop off time': matched_row['Trip drop off time'],
            'Receipt Date': receipt['Date']
        })
    else:
        receipts_unmatched.append({
            'Receipt Date': receipt['Date'],
            'Refund': receipt['Refund'],
            'Pickup Address': receipt['Pickup Address'][:50] if pd.notna(receipt['Pickup Address']) else '',
            'Status': 'NO_TRIP_FOUND_ON_DATE_OR_UUID'
        })

if receipts_unmatched:
    unmatched_df = pd.DataFrame(receipts_unmatched)
    unmatched_df.to_csv(OUTPUT_DIR / 'receipts_without_matching_trips.csv', index=False)
    print(f"\nWARNING: {len(unmatched_df)} receipts have no matching trip on same date")
else:
    print("\nOK: All receipts have matching trips on the same date")

# === 2. Receipts Tracker ↔ Payments ===
print("\n" + "=" * 80)
print("2. RECEIPTS TRACKER vs PAYMENTS")
print("=" * 80)

refund_from_payments = payments_df[
    (payments_df['Description'].str.contains('refund', case=False, na=False)) |
    (payments_df['Description'].str.contains('Refund', case=False, na=False))
].copy()

receipts_refunds = receipts_with_trip_data[receipts_with_trip_data['Refund'].notna()].copy()
print(f"\nRefunds in Receipts Tracker: {len(receipts_refunds)}")
print(f"  Total Refund Amount: ${receipts_refunds['Refund'].sum():,.2f}")

print(f"\nRefund transactions in Payments: {len(refund_from_payments)}")

refund_total_from_payments = 0
for col in payments_df.columns:
    if 'refund' in col.lower() or 'Refund' in col:
        refund_total_from_payments += payments_df[col].sum()
print(f"  Total Refund Amount: ${refund_total_from_payments:,.2f}")

# === 3. Payments ↔ Bank ===
print("\n" + "=" * 80)
print("3. PAYMENTS vs BANK DEPOSITS")
print("=" * 80)

# Group by payment date
payments_df['payment_date'] = payments_df['vs reporting'].dt.date
payment_totals_by_day = payments_df.groupby('payment_date')['Net Earnings'].sum()
bank_totals_by_day = bank_df.groupby(bank_df['Posted Date'].dt.date)['Amount'].sum()

print(f"\nPayment days: {len(payment_totals_by_day)}")
print(f"Bank deposit days: {len(bank_totals_by_day)}")

total_payments = payments_df['Net Earnings'].sum()
total_bank = bank_df['Amount'].sum()

print(f"\nPayments (Net Earnings) Total: ${total_payments:,.2f}")
print(f"Bank Total: ${total_bank:,.2f}")
print(f"Difference: ${(total_payments - total_bank):,.2f}")

# === 4. Daily Reconciliation (3-way) ===
print("\n" + "=" * 80)
print("4. DAILY RECONCILIATION (Trips to Payments to Bank)")
print("=" * 80)

daily_reconcile = []
for date_val in sorted(set(list(payment_totals_by_day.index) + list(bank_totals_by_day.index))):
    trip_count = len(trips_by_date[trips_by_date['Trip_date_only'] == date_val])
    payment_total = payment_totals_by_day.get(date_val, 0)
    bank_total = bank_totals_by_day.get(date_val, 0)
    difference = payment_total - bank_total
    
    daily_reconcile.append({
        'Date': date_val,
        'Trips': trip_count,
        'Payment Total (Net)': round(payment_total, 2),
        'Bank Total': round(bank_total, 2),
        'Difference': round(difference, 2),
        'Status': 'MATCH' if abs(difference) < 0.01 else 'MISMATCH'
    })

daily_df = pd.DataFrame(daily_reconcile)
daily_df.to_csv(OUTPUT_DIR / 'daily_reconciliation_3way.csv', index=False)

mismatches = daily_df[daily_df['Status'] == 'MISMATCH']
print(f"\nDays with mismatches: {len(mismatches)}/{len(daily_df)}")
if len(mismatches) > 0:
    print("\nMismatched days (top 20):")
    print(mismatches[['Date', 'Trips', 'Payment Total (Net)', 'Bank Total', 'Difference']].head(20).to_string(index=False))

# === 5. Refund Verification ===
print("\n" + "=" * 80)
print("5. REFUND VERIFICATION (Receipts to Payments)")
print("=" * 80)

receipt_refunds_with_status = receipts_with_trip_data[[
    'Date', 'Refund', 'Paid', 'Refund Verification Match', 'Pickup Address', 'Trip UUID'
]].copy()

# Attach matched trip times when available
if receipt_matches:
    matches_df = pd.DataFrame(receipt_matches)
    receipt_refunds_with_status = receipt_refunds_with_status.merge(
        matches_df[['Receipt Index', 'Trip UUID', 'Trip drop off time']],
        left_index=True,
        right_on='Receipt Index',
        how='left'
    )
    receipt_refunds_with_status.drop(columns=['Receipt Index'], inplace=True)

marked_matched = (receipt_refunds_with_status['Refund Verification Match'] == 'Match').sum()
print(f"\nRefunds marked as 'Match': {marked_matched}/{len(receipts_refunds)}")

unchecked_refunds = receipt_refunds_with_status[receipt_refunds_with_status['Paid'].isna()].copy()
print(f"Refunds NOT marked as 'checked': {len(unchecked_refunds)}")

receipt_refunds_with_status.to_csv(OUTPUT_DIR / 'refund_verification_status.csv', index=False)

# === 6. SUMMARY REPORT ===
print("\n" + "=" * 80)
print("FOUR-WAY RECONCILIATION SUMMARY")
print("=" * 80)

# Multi-account reconciliation (check if other bank deposits exist)
other_bank_list = []
for csv_file in sorted(Path('bank').glob('*.csv')):
    # Skip the Uber Pro Card, look for other accounts
    if 'Uber Pro Card' not in csv_file.name:
        try:
            df = pd.read_csv(csv_file)
            df['Posted Date'] = pd.to_datetime(df['Posted Date'], errors='coerce')
            df['Amount'] = df['Amount'].astype(str).str.replace(r'[\$\+,]', '', regex=True)
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
            # Filter to ONLY Uber deposits
            uber_only = df[df['Description'].str.contains('Uber App Payout', case=False, na=False)].copy()
            if len(uber_only) > 0:
                other_bank_list.append(uber_only)
        except:
            pass

other_account_total = 0
if other_bank_list:
    other_df = pd.concat(other_bank_list, ignore_index=True)
    other_account_total = other_df['Amount'].sum()

total_all_deposits = total_bank + other_account_total

summary_stats = {
    'Metric': [
        'Total Trips (Completed)',
        'Total Payment Records',
        'Total Bank Transactions',
        'Total Receipts Tracked',
        '',
        'Payments (Net Earnings) Total',
        'Bank Deposits (This Account)',
        'Bank Deposits (Other Accounts)',
        'Total Bank Deposits (All)',
        'Final Difference (Payments - Total)',
        '',
        'Total Refunds (Receipts)',
        'Refunds in Payments',
        'Refund Matches',
        '',
        'Days with Payment/Bank Mismatch',
        'Receipts Missing Trip Match',
        'Unchecked Refunds'
    ],
    'Value': [
        f"{len(trips_df):,}",
        f"{len(payments_df):,}",
        f"{len(bank_df):,}",
        f"{len(receipts_df):,}",
        '',
        f"${total_payments:,.2f}",
        f"${total_bank:,.2f}",
        f"${other_account_total:,.2f}",
        f"${total_all_deposits:,.2f}",
        f"${(total_payments - total_all_deposits):,.2f}",
        '',
        f"${receipts_refunds['Refund'].sum():,.2f}",
        f"${refund_total_from_payments:,.2f}",
        f"{marked_matched}/{len(receipts_refunds)}",
        '',
        f"{len(mismatches)}/{len(daily_df)}",
        f"{len(receipts_unmatched)}",
        f"{len(unchecked_refunds)}"
    ]
}

summary_df = pd.DataFrame(summary_stats)
summary_df.to_csv(OUTPUT_DIR / 'four_way_summary.csv', index=False)
print("\n" + summary_df.to_string(index=False))

print("\n" + "=" * 80)
print(f"Reports saved to: {OUTPUT_DIR}/")
print("=" * 80)
