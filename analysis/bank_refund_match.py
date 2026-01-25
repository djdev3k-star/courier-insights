"""
Enrich bank/refund_status.csv with Trip UUID and trip drop-off time.
Matching strategy:
- Primary: Date + Refund Amount + normalized Pickup Address (exact)
- Secondary: Date + Refund Amount (exact)
- Tertiary: Date + Refund Amount within tolerance (± TOLERANCE)
- Fallback: date-only to attach a representative trip UUID/time
Outputs:
- bank/bank_refund_status_enriched.csv (with match_level)
- bank/bank_refund_unmatched.csv (items with no UUID after all passes)
"""
import pandas as pd
from pathlib import Path
import re

TOLERANCE = 0.50  # dollars for amount tolerance matching

# Paths
bank_refund_path = Path('bank/refund_status.csv')
receipts_path = Path('data/receipts/Trip Receipts-Refund Tracker.csv')
trips_dir = Path('data/consolidated/trips')

if not bank_refund_path.exists():
    raise SystemExit('bank/refund_status.csv not found')

bank_df = pd.read_csv(bank_refund_path)

# Normalize date and amounts
for col in ['Date']:
    if col in bank_df.columns:
        bank_df[col] = pd.to_datetime(bank_df[col], errors='coerce')
if 'Refund Amount' in bank_df.columns:
    bank_df['Refund Amount'] = pd.to_numeric(bank_df['Refund Amount'], errors='coerce').fillna(0.0)
elif 'Refund' in bank_df.columns:
    bank_df['Refund Amount'] = pd.to_numeric(bank_df['Refund'], errors='coerce').fillna(0.0)
else:
    bank_df['Refund Amount'] = 0.0

# Normalize pickup/address text for deterministic matching
def norm_addr(val):
    if pd.isna(val):
        return ''
    return str(val).strip().lower().replace("  ", " ")

bank_df['Norm Address'] = bank_df.get('Pickup Address', '').apply(norm_addr)

# Load receipts tracker (for Trip UUID via Uber Link)
if receipts_path.exists():
    receipts = pd.read_csv(receipts_path)
    receipts['Date'] = pd.to_datetime(receipts['Date'], errors='coerce')
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

    # Extract Trip UUID from Uber Link
    def extract_trip_uuid(link: str):
        if pd.isna(link):
            return None
        match = re.search(r'/trips/([0-9a-fA-F-]{8,})', str(link))
        return match.group(1) if match else None
    receipts['Trip UUID'] = receipts.get('Uber Link', '').apply(extract_trip_uuid)
    receipts['Norm Address'] = receipts.get('Pickup Address', '').apply(norm_addr)
else:
    receipts = pd.DataFrame()

# Load trips for fallback date match
trip_files = sorted(trips_dir.glob('*.csv'))
trips = pd.concat([pd.read_csv(f) for f in trip_files], ignore_index=True) if trip_files else pd.DataFrame()
if not trips.empty and 'Trip drop off time' in trips.columns:
    trips['Trip drop off time'] = pd.to_datetime(trips['Trip drop off time'], errors='coerce')
    trips['Trip_date_only'] = trips['Trip drop off time'].dt.date

# Match priority:
# 1) Date + Refund Amount + Norm Address
# 2) Date + Refund Amount
enriched = bank_df.copy()
enriched['match_level'] = 'unmatched'
if not receipts.empty:
    pri_cols = ['Date', 'Refund Amount', 'Norm Address']
    avail_pri = [c for c in pri_cols if c in receipts.columns]
    if len(avail_pri) == 3:
        enriched = enriched.merge(
            receipts[['Date', 'Refund Amount', 'Norm Address', 'Trip UUID']],
            on=['Date', 'Refund Amount', 'Norm Address'],
            how='left',
            suffixes=('', '_rcpt')
        )
        enriched.loc[enriched['Trip UUID'].notna(), 'match_level'] = 'date+amount+address'
    # Fill remaining by Date + Amount
    if 'Trip UUID' not in enriched.columns:
        enriched['Trip UUID'] = None
    missing_uuid = enriched['Trip UUID'].isna()
    if missing_uuid.any():
        merged_amt = enriched[missing_uuid].merge(
            receipts[['Date', 'Refund Amount', 'Trip UUID']],
            on=['Date', 'Refund Amount'],
            how='left',
            suffixes=('', '_rcpt2')
        )
        enriched.loc[missing_uuid, 'Trip UUID'] = merged_amt['Trip UUID'].values
        enriched.loc[missing_uuid & merged_amt['Trip UUID'].notna(), 'match_level'] = 'date+amount'
    # Tertiary: tolerance on amount
    still_missing = enriched['Trip UUID'].isna()
    if still_missing.any():
        tol_df = enriched[still_missing].copy()
        tol_df['orig_idx'] = tol_df.index
        tol_df['Date'] = pd.to_datetime(tol_df['Date'], errors='coerce')
        receipts_tol = receipts.copy()
        receipts_tol['Date'] = pd.to_datetime(receipts_tol['Date'], errors='coerce')
        # Merge by date then filter by tolerance
        merged_tol = tol_df.merge(
            receipts_tol[['Date', 'Refund Amount', 'Trip UUID']],
            on='Date',
            how='left',
            suffixes=('', '_tol')
        )
        # Apply tolerance filter
        close_amt = (merged_tol['Refund Amount_tol'] - merged_tol['Refund Amount']).abs() <= TOLERANCE
        merged_tol.loc[~close_amt, 'Trip UUID'] = None
        # Assign back using aligned index
        valid_idx = merged_tol['orig_idx']
        enriched.loc[valid_idx, 'Trip UUID'] = merged_tol['Trip UUID'].values
        enriched.loc[valid_idx[merged_tol['Trip UUID'].notna()], 'match_level'] = 'date+amount_tol'
else:
    enriched['Trip UUID'] = None

# Fallback: fill missing UUIDs by date-only from trips (attach representative time)
if not trips.empty and 'Trip UUID' in enriched.columns:
    # Map date -> first trip drop-off time for context
    date_to_time = trips.dropna(subset=['Trip drop off time']).groupby('Trip_date_only')['Trip drop off time'].first()
    # Attach trip time for all rows
    enriched['Trip drop off time'] = enriched['Date'].dt.date.map(date_to_time)
    # If still missing UUIDs, try date-only join to pick a representative UUID
    if enriched['Trip UUID'].isna().any():
        date_to_uuid = trips.dropna(subset=['Trip UUID']).groupby('Trip_date_only')['Trip UUID'].first()
        enriched['Trip UUID'] = enriched['Trip UUID'].fillna(enriched['Date'].dt.date.map(date_to_uuid))
        enriched.loc[enriched['match_level'] == 'unmatched'] = enriched.loc[enriched['match_level'] == 'unmatched'].assign(match_level='date-only')
else:
    enriched['Trip drop off time'] = pd.NaT

# Save enriched file
out_path = Path('bank/bank_refund_status_enriched.csv')
enriched.to_csv(out_path, index=False)
print(f"Enriched bank refund file written to {out_path}")
print(f"Rows: {len(enriched)}")
print(enriched[['Date', 'Refund Amount', 'Trip UUID', 'Trip drop off time']].head())

# Save unmatched
unmatched = enriched[enriched['Trip UUID'].isna()]
unmatched_path = Path('bank/bank_refund_unmatched.csv')
unmatched.to_csv(unmatched_path, index=False)
print(f"Unmatched rows written to {unmatched_path}: {len(unmatched)}")
