"""
Pre-geocode all addresses from transaction data
Run this once to build the complete geocoded address cache

Falls back to city-level geocoding if Nominatim is unavailable
"""
import pandas as pd
from pathlib import Path
import time

# City coordinates for Dallas DFW area (fallback when Nominatim unavailable)
CITY_COORDINATES = {
    'Dallas': (32.7767, -96.7970),
    'Arlington': (32.7357, -97.1081),
    'Fort Worth': (32.7555, -97.3308),
    'Plano': (33.0198, -96.6989),
    'Irving': (32.8140, -96.9489),
    'Frisco': (33.1637, -96.8236),
    'McKinney': (33.1972, -96.6397),
    'Lewisville': (33.0048, -96.5248),
    'Denton': (33.2148, -97.1331),
    'Carrollton': (32.9735, -96.8899),
    'Mesquite': (32.7668, -96.5992),
    'Garland': (32.9126, -96.6389),
    'Richardson': (32.9483, -96.7299),
    'Allen': (33.1031, -96.6705),
    'Balch Springs': (32.7287, -96.6228),
    'Seagoville': (32.6390, -96.5386),
    'Forney': (32.7479, -96.4719),
}

def extract_city_from_address(address):
    """Extract city name from address string"""
    if pd.isna(address):
        return None
    
    addr_str = str(address)
    # Try to find city names in the address
    for city in CITY_COORDINATES.keys():
        if city.lower() in addr_str.lower():
            return city
    
    # Fallback: try to extract from common patterns
    parts = addr_str.split(',')
    if len(parts) >= 2:
        # Usually city is near the end
        for part in reversed(parts):
            part = part.strip()
            for city in CITY_COORDINATES.keys():
                if city.lower() in part.lower():
                    return city
    
    return None

def geocode_address_nominatim(address):
    """Try to geocode with Nominatim (requires geopy)"""
    try:
        from geopy.geocoders import Nominatim
        from geopy.exc import GeocoderTimedOut, GeocoderServiceError
        
        if pd.isna(address) or address == '':
            return None, None
        
        parts = str(address).split(',')
        if len(parts) >= 3:
            clean_addr = ','.join(parts[-4:-1]).strip()
        else:
            clean_addr = address
        
        geolocator = Nominatim(user_agent="courier_geocoding_v1", timeout=10)
        location = geolocator.geocode(clean_addr)
        if location:
            return float(location.latitude), float(location.longitude)
    except ImportError:
        return None, None
    except Exception:
        return None, None
    
    return None, None

def geocode_address_fallback(address):
    """Fallback: use city coordinates from lookup table"""
    city = extract_city_from_address(address)
    if city and city in CITY_COORDINATES:
        lat, lon = CITY_COORDINATES[city]
        # Add small random jitter to differentiate addresses in same city
        import random
        lat += random.uniform(-0.01, 0.01)
        lon += random.uniform(-0.01, 0.01)
        return lat, lon
    
    return None, None

def geocode_address(address):
    """Geocode address: try Nominatim first, fallback to city coordinates"""
    # Try Nominatim first (more accurate)
    lat, lon = geocode_address_nominatim(address)
    if lat and lon:
        return lat, lon
    
    # Fallback to city-level geocoding
    lat, lon = geocode_address_fallback(address)
    if lat and lon:
        return lat, lon
    
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
    print("\n🌍 Geocoding addresses...\n")
    
    geocoded_data = []
    failed = []
    nominatim_count = 0
    fallback_count = 0
    
    for idx, addr in enumerate(addresses):
        addr_display = addr[:50] + "..." if len(addr) > 50 else addr
        print(f"  [{idx+1}/{len(addresses)}] {addr_display}", end='', flush=True)
        
        # Try Nominatim
        lat, lon = geocode_address_nominatim(addr)
        
        if lat and lon:
            geocoded_data.append({
                'address': addr,
                'latitude': lat,
                'longitude': lon
            })
            print(f" ✓ (Nominatim: {lat:.4f}, {lon:.4f})")
            nominatim_count += 1
        else:
            # Try fallback
            lat, lon = geocode_address_fallback(addr)
            if lat and lon:
                geocoded_data.append({
                    'address': addr,
                    'latitude': lat,
                    'longitude': lon
                })
                city = extract_city_from_address(addr)
                print(f" ✓ (City: {city})")
                fallback_count += 1
            else:
                failed.append(addr)
                print(f" ✗ (no city found)")
        
        # Rate limit for Nominatim
        time.sleep(0.1)
    
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
✓ Successfully geocoded:  {len(geocoded_data)}
  ├─ Street-level (Nominatim): {nominatim_count}
  └─ City-level (Fallback):    {fallback_count}
✗ Failed to geocode:      {len(failed)}
📁 Saved to: data/geocoded_addresses.csv

The app will now load with all coordinates ready!
""")
    
    if failed:
        print("⚠️  Failed addresses (no city found):")
        for addr in failed[:5]:
            print(f"  - {addr}")
        if len(failed) > 5:
            print(f"  ... and {len(failed) - 5} more")

if __name__ == '__main__':
    main()
