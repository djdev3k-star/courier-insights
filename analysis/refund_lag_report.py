"""
Refund Lag Report
- Shows receipt vs payout months for refunds
- Highlights lags (receipt date to payout date) and cross-month batching
"""
import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path('reports/refund_lag')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("REFUND LAG REPORT")
print("Receipt month vs payout month for refunds")
print("=" * 80)

# Load receipts tracker (prefer detailed tracker, fallback to bank/refund_status)
receipts_paths = [
    Path('data/receipts/Trip Receipts-Refund Tracker.csv'),
    Path('bank/refund_status.csv')
]
receipts_path = next((p for p in receipts_paths if p.exists()), None)
if receipts_path is None:
    raise SystemExit("No receipts tracker found at data/receipts/ or bank/refund_status.csv")

print(f"Loading receipts from: {receipts_path}")
receipts = pd.read_csv(receipts_path)

# Normalize columns
for col in ['Date', 'Date Paid']:
    if col in receipts.columns:
        receipts[col] = pd.to_datetime(receipts[col], errors='coerce')
    else:
        receipts[col] = pd.NaT

# Refund amount
if 'Refund Amount' in receipts.columns:
    receipts['Refund Amount'] = pd.to_numeric(receipts['Refund Amount'], errors='coerce').fillna(0.0)
elif 'Refund' in receipts.columns:
    receipts['Refund Amount'] = (
        receipts['Refund']
        .astype(str)
        .str.replace(r'[\$,]', '', regex=True)
    )
    receipts['Refund Amount'] = pd.to_numeric(receipts['Refund Amount'], errors='coerce').fillna(0.0)
else:
    receipts['Refund Amount'] = 0.0

# Payout date preference: Date Paid column; fallback to receipt Date when missing (for monthly alignment)
receipts['Payout Date'] = receipts['Date Paid']
receipts.loc[receipts['Payout Date'].isna(), 'Payout Date'] = receipts['Date']

# Months
receipts['Receipt Month'] = receipts['Date'].dt.to_period('M')
receipts['Payout Month'] = receipts['Payout Date'].dt.to_period('M')

# Monthly totals by receipt vs payout
receipt_month_totals = receipts.groupby('Receipt Month')['Refund Amount'].sum().reset_index()
payout_month_totals = receipts.groupby('Payout Month')['Refund Amount'].sum().reset_index()

# Cross-month matrix
matrix = receipts.pivot_table(
    index='Receipt Month',
    columns='Payout Month',
    values='Refund Amount',
    aggfunc='sum',
    fill_value=0.0
).reset_index()

# Lag calculations (only where both dates exist)
lag_df = receipts.dropna(subset=['Date', 'Payout Date']).copy()
lag_df['Lag Days'] = (lag_df['Payout Date'] - lag_df['Date']).dt.days

lag_buckets = pd.DataFrame({
    'Lag Bucket': ['0-7 days', '8-30 days', '31+ days', 'Missing payout date'],
    'Count': [
        ((lag_df['Lag Days'] >= 0) & (lag_df['Lag Days'] <= 7)).sum(),
        ((lag_df['Lag Days'] >= 8) & (lag_df['Lag Days'] <= 30)).sum(),
        (lag_df['Lag Days'] >= 31).sum(),
        receipts['Payout Date'].isna().sum()
    ]
})

# Summary headline
print("\nRefund totals by receipt month:")
print(receipt_month_totals.to_string(index=False))

print("\nRefund totals by payout month:")
print(payout_month_totals.to_string(index=False))

if not lag_df.empty:
    print("\nLag stats (days):")
    print(lag_df['Lag Days'].describe().to_string())

# Save outputs
receipt_month_totals.to_csv(OUTPUT_DIR / 'refunds_by_receipt_month.csv', index=False)
payout_month_totals.to_csv(OUTPUT_DIR / 'refunds_by_payout_month.csv', index=False)
matrix.to_csv(OUTPUT_DIR / 'receipt_vs_payout_matrix.csv', index=False)
lag_buckets.to_csv(OUTPUT_DIR / 'refund_lag_buckets.csv', index=False)
lag_df[['Date', 'Payout Date', 'Refund Amount', 'Lag Days']].to_csv(OUTPUT_DIR / 'refund_lag_detail.csv', index=False)

print("\nReports saved to reports/refund_lag/")
print(" - refunds_by_receipt_month.csv")
print(" - refunds_by_payout_month.csv")
print(" - receipt_vs_payout_matrix.csv")
print(" - refund_lag_buckets.csv")
print(" - refund_lag_detail.csv")
