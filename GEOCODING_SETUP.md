# Pre-Geocoding Setup

## Overview
The app uses pre-geocoded addresses for instant loading. Address coordinates are static and geocoded once, then cached permanently in `data/geocoded_addresses.csv`.

## How It Works
The script uses a **two-tier geocoding strategy**:

1. **Primary**: Street-level geocoding via Nominatim (accurate to address level) - requires geopy
2. **Fallback**: City-level geocoding from a lookup table (accurate to city) - always works

If Nominatim is unavailable (network issues, service limits, or geopy not installed), the script automatically falls back to city-level coordinates extracted from address text.

## Initial Setup (One-Time)

### Step 1: Run the pre-geocoding script
```bash
python pre_geocode_addresses.py
```

This will:
- Scan all transaction CSV files in `reports/monthly_comprehensive/`
- Extract all unique pickup addresses
- Geocode each address (street-level via Nominatim if available, city-level fallback always works)
- Save coordinates to `data/geocoded_addresses.csv`
- **Duration**: ~2-3 minutes for typical dataset

### Step 2: Start the app
```bash
streamlit run courier_insights.py
```

The app will instantly load all location data with zero geocoding overhead.

## Geocoding Methods

### Method 1: Street-Level (Nominatim)
- **Accuracy**: Individual address
- **Requires**: `pip install geopy`
- **Works when**: Network accessible, Nominatim service online
- **Coverage**: Complete for valid addresses

### Method 2: City-Level (Fallback)
- **Accuracy**: City block (jittered to avoid perfect overlap)
- **Requires**: Nothing (always available)
- **Works when**: Address contains recognizable city name
- **Coverage**: All Dallas DFW cities automatically included

## Supported Cities (Fallback)
Pre-loaded coordinates available for:
- Dallas, Arlington, Fort Worth, Plano, Irving, Frisco
- McKinney, Lewisville, Denton, Carrollton, Mesquite
- Garland, Richardson, Allen, Balch Springs, Seagoville, Forney

## Notes
- ✅ Run pre-geocoding **once** when setting up the project
- ✅ Add `data/geocoded_addresses.csv` to version control (it's static data)
- ✅ App loads instantly - no runtime geocoding delays
- ✅ Works offline once geocoding is complete
- ✅ If new addresses appear in reports, re-run the script
- ℹ️ Fallback ensures 100% geocoding coverage for Dallas DFW area
- ⚠️ Nominatim is rate-limited (~1 request/second) - don't run multiple scripts simultaneously

## Troubleshooting

### Script completes but shows only city-level geocoding
- This is normal if geopy isn't installed or Nominatim is unavailable
- City-level accuracy is sufficient for regional analysis
- To get street-level: `pip install geopy`

### Some addresses fail to geocode
- Check that address contains a recognized city name
- Add missing cities to the `CITY_COORDINATES` dictionary in the script

### Script fails with "No addresses found"
- Check that `reports/monthly_comprehensive/*.csv` exists
- Verify the CSV has a `Pickup address` column

### Add new addresses
- Simply add new CSV files to `reports/monthly_comprehensive/`
- Re-run `python pre_geocode_addresses.py` to update `data/geocoded_addresses.csv`
- The script automatically avoids re-geocoding addresses already in the cache
