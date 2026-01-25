"""
Pre-geocode all addresses from transaction data
Run this once to build the complete geocoded address cache
"""
import pandas as pd
from pathlib import Path
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

def geocode_address(address):
    """Geocode a single address using geopy"""
    if pd.isna(address) or address == '':
        return None, None
    
    try:
        parts = str(address).split(',')
        if len(parts) >= 3:
            clean_addr = ','.join(parts[-4:-1]).strip()
        else:
            clean_addr = address
        
        geolocator = Nominatim(user_agent="courier_geocoding_v1", timeout=10)
        location = geolocator.geocode(clean_addr)
        if location:
            return float(location.latitude), float(location.longitude)
    except (GeocoderTimedOut, GeocoderServiceError):
        return None, None
    except Exception:
        pass
    
    return None, None

def main():
    """Extract all addresses from transaction files and geocode them"""
    
    print("🔍 Collecting addresses from transaction files...")
    addresses = set()
    
    # Find all transaction CSV files
    reports_dir = Path('reports/monthly_comprehensive')
    if reports_dir.exists():
        for csv_file in reports_dir.glob('*.csv'):
            try:
                df = pd.read_csv(csv_file)
                if 'Pickup address' in df.columns:
                    file_addresses = df['Pickup address'].dropna().unique()
                    addresses.update(file_addresses)
                    print(f"  ✓ {csv_file.name}: {len(file_addresses)} addresses")
            except Exception as e:
                print(f"  ✗ Error reading {csv_file.name}: {e}")
    
    addresses = sorted(list(addresses))
    print(f"\n📍 Total unique addresses to geocode: {len(addresses)}")
    
    if len(addresses) == 0:
        print("❌ No addresses found. Check that reports/monthly_comprehensive/*.csv exist")
        return
    
    # Geocode all addresses
    print("\n🌍 Geocoding addresses (this may take a few minutes)...\n")
    
    geocoded_data = []
    failed = []
    
    for idx, addr in enumerate(addresses):
        print(f"  [{idx+1}/{len(addresses)}] {addr[:60]}...", end='', flush=True)
        
        lat, lon = geocode_address(addr)
        
        if lat and lon:
            geocoded_data.append({
                'address': addr,
                'latitude': lat,
                'longitude': lon
            })
            print(f" ✓ ({lat:.4f}, {lon:.4f})")
        else:
            failed.append(addr)
            print(f" ✗ (no coordinates)")
        
        # Be nice to Nominatim - don't hammer it
        time.sleep(0.5)
    
    # Save to CSV
    print(f"\n💾 Saving {len(geocoded_data)} geocoded addresses...", end='', flush=True)
    
    output_dir = Path('data')
    output_dir.mkdir(exist_ok=True)
    
    df_geocoded = pd.DataFrame(geocoded_data)
    df_geocoded.to_csv('data/geocoded_addresses.csv', index=False)
    
    print(f" ✓\n")
    
    # Summary
    print(f"""
📊 GEOCODING COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Successfully geocoded: {len(geocoded_data)}
✗ Failed to geocode:    {len(failed)}
📁 Saved to: data/geocoded_addresses.csv

The app will now load instantly with all coordinates pre-loaded!
""")
    
    if failed:
        print("Failed addresses:")
        for addr in failed[:10]:
            print(f"  - {addr}")
        if len(failed) > 10:
            print(f"  ... and {len(failed) - 10} more")

if __name__ == '__main__':
    main()
