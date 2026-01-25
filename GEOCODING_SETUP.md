# Pre-Geocoding Setup

## Overview
The app uses pre-geocoded addresses for instant loading. Address coordinates are static and geocoded once, then cached permanently in `data/geocoded_addresses.csv`.

## Initial Setup (One-Time)

### Step 1: Run the pre-geocoding script
```bash
python pre_geocode_addresses.py
```

This will:
- Scan all transaction CSV files in `reports/monthly_comprehensive/`
- Extract all unique pickup addresses
- Geocode each address using Nominatim (free service)
- Save coordinates to `data/geocoded_addresses.csv`
- **Duration**: ~5-10 minutes depending on address count (rate-limited to 0.5s per request)

### Step 2: Start the app
```bash
streamlit run courier_insights.py
```

The app will instantly load all location data with zero geocoding overhead.

## Notes
- ✅ Run pre-geocoding **once** when setting up the project
- ✅ Add `data/geocoded_addresses.csv` to version control (it's static data)
- ✅ App loads instantly - no runtime geocoding delays
- ✅ If new addresses appear in reports, re-run the script
- ⚠️ Nominatim is rate-limited (~1 request/second) - don't run multiple scripts simultaneously

## Troubleshooting

### Script fails with "No addresses found"
- Check that `reports/monthly_comprehensive/*.csv` exists
- Verify the CSV has a `Pickup address` column

### Some addresses fail to geocode
- Nominatim may timeout for invalid/incomplete addresses
- Failed addresses are noted in the output
- The app will display available coordinates and skip missing ones

### Add new addresses
- Simply add new CSV files to `reports/monthly_comprehensive/`
- Re-run `python pre_geocode_addresses.py` to update `data/geocoded_addresses.csv`
- The script automatically avoids re-geocoding addresses already in the cache
