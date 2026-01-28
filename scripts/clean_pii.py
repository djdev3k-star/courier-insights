import pandas as pd
from pathlib import Path

# Directories
trips_dir = Path('data/consolidated/trips')
payments_dir = Path('data/consolidated/payments')

# Process trips
for csv_file in trips_dir.glob('*.csv'):
    df = pd.read_csv(csv_file)
    # Remove name columns if they exist
    columns_to_drop = ['Driver first name', 'Driver last name']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
    df.to_csv(csv_file, index=False)
    print(f"Cleaned {csv_file.name}")

# Process payments
for csv_file in payments_dir.glob('*.csv'):
    df = pd.read_csv(csv_file)
    # Remove name columns if they exist
    columns_to_drop = ['Driver first name', 'Driver last name']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
    df.to_csv(csv_file, index=False)
    print(f"Cleaned {csv_file.name}")

print("PII removal complete.")