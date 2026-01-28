import pandas as pd

# Check trips data
print("TRIPS DATA STRUCTURE:")
print("=" * 80)
df_trips = pd.read_csv('data/consolidated/trips/202509-FULL-trip_activity-.csv')
print(f"Total trips: {len(df_trips)}")
print("\nColumns:")
for col in df_trips.columns:
    print(f"  {col}")

# Check payments data for all refund-related columns
print("\n\nPAYMENTS DATA - REFUND COLUMNS:")
print("=" * 80)
df_payments = pd.read_csv('data/consolidated/payments/202509-FULL-payments_order-.csv')
refund_cols = [col for col in df_payments.columns if 'efund' in col.lower() or 'order' in col.lower()]
print("\nRefund-related columns:")
for col in refund_cols:
    non_zero = df_payments[df_payments[col] != 0][col]
    print(f"\n{col}:")
    print(f"  Non-zero values: {len(non_zero)}")
    if len(non_zero) > 0:
        print(f"  Total: ${non_zero.sum():,.2f}")
        print(f"  Sample values: {non_zero.head(5).tolist()}")
