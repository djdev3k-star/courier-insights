"""
Courier Insights - Purpose-Built Analytics Dashboard
For finding outliers, optimizing earnings, and maximizing efficiency
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime, timedelta

st.set_page_config(page_title="Courier Insights", layout="wide", initial_sidebar_state="expanded")

# Mapbox configuration
px.set_mapbox_access_token('pk.eyJ1IjoibXBieDE1IiwiYSI6ImNta2Y1a3dxZzAzZ3AzZ29qNXQ1bmpiaGsifQ.tCkudl7SJNzzHCARPEzC9w')

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
  /* Color Variables */
  :root {
    --black: #000000;
    --dark-blue: #1a3a52;
    --blue: #1e5a96;
    --light-blue: #6ba3d0;
    --white: #ffffff;
    --light-gray: #f5f6f8;
    --text-primary: #000000;
    --text-secondary: #4a5568;
  }
  
  /* Main Container */
  .main {
    padding-top: 2rem !important;
    background: #ffffff;
  }
  
  /* Sidebar Logo */
  .logo-container {
    text-align: center;
    padding: 8px 0;
    margin-bottom: 20px;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .logo-container img {
    max-width: 200px;
    height: auto;
  }
  
  /* Sidebar Metrics - Clean and Minimal */
  .sidebar-metrics {
    background: #f5f6f8;
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 24px;
    border-left: 4px solid #1e5a96;
  }
  
  .metrics-header {
    font-size: 10px;
    font-weight: 800;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 12px;
    display: block;
  }
  
  .metric-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 9px;
    font-size: 13px;
  }
  
  .metric-label {
    color: #4a5568;
    font-weight: 600;
  }
  
  .metric-value {
    color: #1a3a52;
    font-weight: 700;
  }
  
  /* Navigation Section */
  .nav-section {
    margin-bottom: 8px;
  }
  
  .nav-label {
    font-size: 10px;
    font-weight: 800;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    padding: 12px 0 10px 0;
    display: block;
  }
  
  /* Modern Navigation Buttons */
  .stButton {
    padding: 0 !important;
    margin: 0 !important;
  }
  
  .stButton > button {
    background-color: transparent !important;
    background: transparent !important;
    color: #000000 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 0px !important;
    transition: all 0.2s ease !important;
    text-align: left !important;
    width: 100% !important;
    position: relative;
    box-shadow: none !important;
  }
  
  .stButton > button:hover {
    background-color: transparent !important;
    background: transparent !important;
    border-bottom-color: #1e5a96 !important;
    color: #1a3a52 !important;
    font-weight: 600 !important;
    box-shadow: none !important;
  }
  
  .stButton > button:focus {
    background-color: transparent !important;
    background: transparent !important;
    border-bottom-color: #1e5a96 !important;
    color: #1a3a52 !important;
    font-weight: 600 !important;
    box-shadow: none !important;
  }
  
  .stButton > button:active {
    background-color: transparent !important;
    background: transparent !important;
    box-shadow: none !important;
  }
  
  /* Hide radio buttons (no longer used) */
  [role="radio"] {
    display: none !important;
  }
  
  .stRadio {
    display: none !important;
  }
  
  /* Page Title */
  .page-title {
    color: #000000;
    text-align: center;
    margin-bottom: 10px;
  }
  
  /* Page Header Styling */
  h1 {
    color: #000000 !important;
    border-bottom: 2px solid #1e5a96;
    padding-bottom: 12px;
    margin-bottom: 16px;
    font-weight: 700;
  }
  
  h2 {
    color: #1a3a52 !important;
    margin-top: 24px;
    margin-bottom: 12px;
    font-weight: 700;
  }
  
  h3 {
    color: #4a5568 !important;
    margin-top: 16px;
    margin-bottom: 10px;
    font-weight: 600;
  }
  
  /* Dividers */
  hr {
    border: none;
    height: 1px;
    background: #e2e8f0;
    margin: 20px 0;
  }
  
  /* Data Tables */
  .dataframe {
    background: #f5f6f8 !important;
    border-radius: 8px !important;
    border: 1px solid #e2e8f0 !important;
  }
  
  .stDataFrame {
    margin: 16px 0;
  }
  
  /* Metric Cards */
  .metric-card {
    background: linear-gradient(135deg, #f5f6f8 0%, #ffffff 100%);
    padding: 16px;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    margin-bottom: 12px;
  }
  
  /* Plotly Charts */
  .plotly-container {
    border-radius: 8px;
    overflow: hidden;
  }
  
  /* Sidebar header text */
  .stSidebar h3 {
    color: #000000;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 12px;
    margin-top: 0;
  }
  
  .stSidebar p {
    color: #4a5568;
    font-size: 13px;
    line-height: 1.5;
  }
  
  /* Buttons */
  .stButton > button {
    background-color: #1e5a96 !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
  }
  
  .stButton > button:hover {
    background-color: #1a3a52 !important;
    box-shadow: 0 4px 12px rgba(26, 58, 82, 0.2) !important;
  }
  
  /* Subheader */
  .stSubheader {
    color: #1a3a52 !important;
    font-weight: 700 !important;
  }
  
  /* Text styling */
  .stMarkdown {
    color: #000000;
  }
  
  /* Body and Page Background */
  body {
    background-color: #ffffff !important;
    color: #000000 !important;
  }
  
  .stApp {
    background: #ffffff !important;
  }
  
  [data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
  }
  
  [data-testid="stHeader"] {
    background-color: #ffffff !important;
  }
  
  .stMetric {
    background: #f5f6f8;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
  }
  
  .stMetricLabel {
    color: #4a5568 !important;
    font-weight: 600 !important;
  }
  
  .stMetricValue {
    color: #1a3a52 !important;
    font-weight: 700 !important;
  }
  
  /* Print Mode Styles */
  @media print {
    .stSidebar {
      display: none !important;
    }
    .stAppHeader {
      display: none !important;
    }
    .stToolbar {
      display: none !important;
    }
    main {
      padding: 0 !important;
    }
    .stMarkdown h1 {
      page-break-after: avoid;
      margin-top: 0;
      border: none;
      padding-bottom: 8px;
    }
    .stMarkdown h2 {
      page-break-after: avoid;
      margin-top: 24px;
    }
    .stDataFrame {
      page-break-inside: avoid;
      margin: 12px 0;
    }
    .plotly-container {
      page-break-inside: avoid;
    }
    body {
      background: white;
      color: #000;
    }
  }
</style>
""", unsafe_allow_html=True)

def safe_read(path):
  """Safely read CSV file, return empty DataFrame if missing or error"""
  p = Path(path)
  if p.exists():
    try:
      return pd.read_csv(p)
    except Exception as e:
      st.warning(f"Could not read {path}: {e}")
  return pd.DataFrame()

def format_money(val):
  """Format value as currency"""
  return f"${val:,.2f}"

def format_percent(val):
  """Format value as percentage"""
  return f"{val:.1f}%"

def format_month_human(month_str):
  """Convert YYYY-MM to human-friendly format like 'August 2025'"""
  try:
    return pd.to_datetime(month_str + '-01').strftime('%B %Y')
  except:
    return month_str

# Restaurant logo URLs (hardcoded for reliability)
RESTAURANT_LOGOS = {
    "McDonald's": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/1200px-McDonald%27s_Golden_Arches.svg.png",
    "Taco Bell": "https://www.tacobell.com/favicon.ico",
    "CVS": "https://www.cvs.com/favicon.ico",
    "Jack in the Box": "https://www.jackinthebox.com/favicon.ico",
    "24 Seven Tacos": "https://cdn-icons-png.flaticon.com/512/2919/2919600.png",
    "Big Guys Chicken & Rice": "https://cdn-icons-png.flaticon.com/512/921/921489.png",
    "Burger King": "https://www.burgerking.com/favicon.ico",
    "Walgreens": "https://www.walgreens.com/favicon.ico",
    "Target": "https://www.target.com/favicon.ico",
    "Dollar General": "https://www.dollargeneral.com/favicon.ico",
}

def get_restaurant_logo(restaurant_name):
  """Get restaurant logo from hardcoded map"""
  return RESTAURANT_LOGOS.get(restaurant_name)

@st.cache_data
@st.cache_data
def load_geocoded_addresses():
  """Load cached geocoded addresses, create if doesn't exist"""
  geocode_file = Path('data/geocoded_addresses.csv')
  if geocode_file.exists():
    return pd.read_csv(geocode_file)
  return pd.DataFrame(columns=['address', 'latitude', 'longitude'])

def geocode_address(address):
  """Geocode a single address using geopy with fallback"""
  if pd.isna(address) or address == '':
    return None, None
  
  try:
    # Extract the cleaner part of the address (after the comma before restaurant name)
    # Format: "Restaurant Name (shortaddr), Full Address, City, State ZIP, Country"
    parts = str(address).split(',')
    if len(parts) >= 3:
      # Use: Street, City State Zip (ignore restaurant name and country)
      clean_addr = ','.join(parts[-4:-1]).strip()  # Get the meaningful address parts
    else:
      clean_addr = address
    
    try:
      from geopy.geocoders import Nominatim
      from geopy.exc import GeocoderTimedOut, GeocoderServiceError
      
      geolocator = Nominatim(user_agent="courier_insights_v2", timeout=10)
      location = geolocator.geocode(clean_addr)
      if location:
        return float(location.latitude), float(location.longitude)
    except ImportError:
      pass  # Fall through to fallback
    except (GeocoderTimedOut, GeocoderServiceError):
      return None, None
  except Exception as e:
    pass
  
  return None, None

@st.cache_data
def get_coordinates_for_addresses(addresses_list):
  """Get lat/lon for a list of addresses with progress tracking"""
  geocoded = load_geocoded_addresses()
  geocoded_dict = dict(zip(geocoded['address'], zip(geocoded['latitude'], geocoded['longitude'])))
  
  results = {}
  new_addresses = []
  
  # Show progress
  progress_bar = st.progress(0)
  status_text = st.empty()
  
  for idx, addr in enumerate(addresses_list):
    progress_bar.progress((idx + 1) / len(addresses_list))
    status_text.text(f"Geocoding {idx + 1}/{len(addresses_list)}...")
    
    if pd.isna(addr):
      results[addr] = (None, None)
    elif addr in geocoded_dict:
      results[addr] = geocoded_dict[addr]
    else:
      lat, lon = geocode_address(addr)
      results[addr] = (lat, lon)
      if lat and lon:
        new_addresses.append({'address': addr, 'latitude': lat, 'longitude': lon})
  
  progress_bar.empty()
  status_text.empty()
  
  # Save new addresses to cache
  if new_addresses:
    try:
      Path('data').mkdir(exist_ok=True)
      new_df = pd.DataFrame(new_addresses)
      if geocoded.empty:
        new_df.to_csv('data/geocoded_addresses.csv', index=False)
      else:
        geocoded = pd.concat([geocoded, new_df], ignore_index=True).drop_duplicates(subset=['address'])
        geocoded.to_csv('data/geocoded_addresses.csv', index=False)
    except Exception as e:
      st.warning(f"Could not save geocode cache: {e}")
  
  return results

# ============================================================================
# LOAD ALL DATA
# ============================================================================

@st.cache_data
def load_data():
  """Load and prepare all data for analysis"""
  # Load raw data
  transactions = safe_read('reports/monthly_comprehensive/all_transactions_detailed.csv')
  audit = safe_read('reports/audit_trail/complete_audit_trail.csv')
  refunds = safe_read('reports/four_way_reconciliation/refund_verification_status.csv')
  multi_account = safe_read('reports/four_way_reconciliation/multi_account_reconciliation.csv')
  daily = safe_read('reports/four_way_reconciliation/daily_reconciliation_3way.csv')
  
  if transactions.empty:
    return None
  
  # Parse dates
  transactions['Trip drop off time'] = pd.to_datetime(transactions['Trip drop off time'], errors='coerce')
  if 'Bank Deposit Date' in audit.columns:
    audit['Bank Deposit Date'] = pd.to_datetime(audit['Bank Deposit Date'], errors='coerce')
  
  # Add helpful columns
  transactions['Date'] = transactions['Trip drop off time'].dt.date
  transactions['Month'] = transactions['Trip drop off time'].dt.strftime('%Y-%m')
  transactions['Hour'] = transactions['Trip drop off time'].dt.hour
  transactions['DayOfWeek'] = transactions['Trip drop off time'].dt.day_name()
  transactions['Earnings Per Mile'] = transactions['Net Earnings'] / (transactions['Trip distance'] + 0.01)
  transactions['Is Refund'] = transactions['Refund'] != 0
  transactions['Is Low Pay'] = transactions['Net Earnings'] < 3.00
  transactions['Is High Pay'] = transactions['Net Earnings'] > 15.00
  
  # Extract location info from addresses (format: "Restaurant Name, Street Address, City, State ZIP, US")
  def extract_city(addr):
    if pd.isna(addr):
      return 'Unknown'
    parts = str(addr).split(',')
    if len(parts) >= 4:
      # City is typically 2 parts before end (before State ZIP, before US)
      return parts[-3].strip()
    elif len(parts) >= 3:
      return parts[-2].strip()
    return 'Unknown'
  
  def extract_zip(addr):
    if pd.isna(addr):
      return ''
    parts = str(addr).split(',')
    if len(parts) >= 3:
      # ZIP is in the State ZIP part (e.g., "TX 75126"), extract 5-digit code
      state_zip = parts[-2].strip() # e.g., "TX 75126"
      zip_parts = state_zip.split()
      if len(zip_parts) >= 2:
        return zip_parts[-1]
    return ''
  
  def extract_restaurant(addr):
    if pd.isna(addr):
      return 'Other'
    # First part before comma is typically the restaurant/business name
    first_part = str(addr).split(',')[0].strip()
    # Remove parenthetical info (like store number)
    restaurant = first_part.split('(')[0].strip()
    return restaurant if restaurant else 'Other'
  
  transactions['Pickup City'] = transactions['Pickup address'].apply(extract_city)
  transactions['Pickup Zip'] = transactions['Pickup address'].apply(extract_zip)
  transactions['Dropoff City'] = transactions['Drop off address'].apply(extract_city)
  transactions['Dropoff Zip'] = transactions['Drop off address'].apply(extract_zip)
  transactions['Restaurant'] = transactions['Pickup address'].apply(extract_restaurant)
  transactions['Pickup Area'] = transactions['Pickup City'] + ' ' + transactions['Pickup Zip']
  transactions['Dropoff Area'] = transactions['Dropoff City'] + ' ' + transactions['Dropoff Zip']
  
  return {
    'transactions': transactions,
    'audit': audit,
    'refunds': refunds,
    'multi_account': multi_account,
    'daily': daily
  }

data = load_data()

if data is None:
  st.error("Could not load transaction data. Please ensure reports are generated.")
  st.stop()

tx = data['transactions']
audit_df = data['audit']
refunds_df = data['refunds']
multi_df = data['multi_account']

# ============================================================================
# CALCULATE KEY METRICS
# ============================================================================

total_earnings = tx['Net Earnings'].sum()
total_miles = tx['Trip distance'].sum()
total_trips = len(tx)
avg_per_mile = total_earnings / (total_miles + 0.01)
refund_count = (tx['Refund'] != 0).sum()
refund_rate = refund_count / len(tx) * 100
low_pay_trips = (tx['Net Earnings'] < 3.00).sum()
high_pay_trips = (tx['Net Earnings'] > 15.00).sum()

# ============================================================================
# SIDEBAR NAVIGATION & PERSISTENT HEADER
# ============================================================================

with st.sidebar:
  # Display JTech Logo
  st.markdown('<div class="logo-container">', unsafe_allow_html=True)
  st.image("JTechLogistics_Logo.svg")
  st.markdown('</div>', unsafe_allow_html=True)
  
  # Navigation Section - FIRST
  st.markdown('<span class="nav-label">Navigation</span>', unsafe_allow_html=True)
  
  # Create a session state variable to track the selected page
  if 'current_page' not in st.session_state:
    st.session_state.current_page = "Overview"

  # Navigation items with descriptions
  nav_items = [
    {"label": "Overview", "page": "Overview", "desc": "Daily pulse"},
    {"label": "Routes", "page": "Routes", "desc": "Best paths"},
    {"label": "Locations", "page": "Locations", "desc": "Map intel"},
    {"label": "Schedule", "page": "Schedule", "desc": "When to drive"},
    {"label": "Payments", "page": "Payments", "desc": "Cashflow"},
    {"label": "Issues", "page": "Issues", "desc": "Fix problems"},
    {"label": "Trends", "page": "Trends", "desc": "Patterns"},
    {"label": "Year-End Report", "page": "Year-End Report", "desc": "Annual analysis"}
  ]

  # Navigation
  st.markdown('<span class="nav-label">Navigation</span>', unsafe_allow_html=True)
  
  # Use selectbox for clean, working navigation
  nav_labels = [item["label"] for item in nav_items]
  current_index = nav_labels.index(st.session_state.current_page) if st.session_state.current_page in nav_labels else 0
  
  selected_nav = st.selectbox(
    "Select Page",
    nav_labels,
    index=current_index,
    label_visibility="collapsed"
  )
  
  # Update session state when selection changes
  if selected_nav != st.session_state.current_page:
    matching_item = next((item for item in nav_items if item["label"] == selected_nav), None)
    if matching_item:
      st.session_state.current_page = matching_item["page"]
      st.rerun()

  st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
  st.divider()
  st.markdown('<div style="margin: 20px 0;"></div>', unsafe_allow_html=True)
  
  # Key Metrics Panel
  st.markdown('<span class="metrics-header">Performance Metrics</span>', unsafe_allow_html=True)
  st.markdown('<div class="sidebar-metrics">', unsafe_allow_html=True)
  
  # Check if there are cross-account transfers
  cross_account_total = 0
  if not multi_df.empty and 'Amount' in multi_df.columns:
    cross_account_total = multi_df['Amount'].sum()
  
  metrics_html = f"""
  <div class="metric-row">
    <span class="metric-label">Total Earnings</span>
    <span class="metric-value">{format_money(total_earnings)}</span>
  </div>
  """
  
  if cross_account_total > 0:
    metrics_html += f"""
  <div class="metric-row" style="font-size: 11px; padding-left: 8px;">
    <span class="metric-label" style="color: #6b7280;">Inc. cross-account</span>
    <span class="metric-value" style="color: #6b7280;">{format_money(cross_account_total)}</span>
  </div>
  """
  
  metrics_html += f"""
  <div class="metric-row">
    <span class="metric-label">Total Miles</span>
    <span class="metric-value">{f"{total_miles:,.0f}"}</span>
  </div>
  <div class="metric-row">
    <span class="metric-label">$/Mile</span>
    <span class="metric-value">{format_money(avg_per_mile)}</span>
  </div>
  <div class="metric-row">
    <span class="metric-label">Total Trips</span>
    <span class="metric-value">{f"{total_trips:,}"}</span>
  </div>
  <div class="metric-row">
    <span class="metric-label">Refund Rate</span>
    <span class="metric-value">{format_percent(refund_rate)}</span>
  </div>
  <div class="metric-row">
    <span class="metric-label">Refunds</span>
    <span class="metric-value">{refund_count}</span>
  </div>
  """
  st.markdown(metrics_html, unsafe_allow_html=True)
  st.markdown('</div>', unsafe_allow_html=True)
  
  page = st.session_state.current_page

# ============================================================================
# PAGE: OVERVIEW (Home)
# ============================================================================

if page == "Overview":
  st.title("Overview")
  st.write("Visual intelligence: See where you earn the most")
  
  st.divider()
  
  # Current month summary
  current_month = pd.Timestamp.now().strftime('%Y-%m')
  month_data = tx[tx['Month'] == current_month]
  
  col1, col2, col3, col4 = st.columns(4)
  if not month_data.empty:
    col1.metric("This Month Earnings", format_money(month_data['Net Earnings'].sum()))
    col2.metric("This Month Trips", len(month_data))
    col3.metric("This Month Miles", f"{month_data['Trip distance'].sum():.0f}")
    col4.metric("This Month Avg/Mile", format_money(month_data['Net Earnings'].sum() / month_data['Trip distance'].sum()))
  
  st.divider()
  
  # MAP VIEW: Best Cities by Tip Rate
  st.subheader("Best Cities by Tip Rate")
  
  city_coords = {
    'Dallas': (32.7767, -96.7970),
    'Plano': (33.0198, -96.6989),
    'McKinney': (33.1972, -96.6397),
    'Frisco': (33.1507, -96.8236),
    'Allen': (33.1031, -96.6705),
    'Richardson': (32.9483, -96.7299),
    'Garland': (32.9126, -96.6389),
    'Mesquite': (32.7668, -96.5992),
    'Irving': (32.8140, -96.9489),
    'Carrollton': (32.9537, -96.8903),
    'Lewisville': (33.0462, -96.9942),
    'Denton': (33.2148, -97.1331),
    'Fort Worth': (32.7555, -97.3308),
    'Arlington': (32.7357, -97.1081),
    'Forney': (32.7479, -96.4719),
    'Balch Springs': (32.7287, -96.6228),
    'Seagoville': (32.6390, -96.5386)
  }
  
  city_stats = tx.groupby('Pickup City').agg({
    'Net Earnings': 'sum',
    'Tip': 'sum',
    'Fare': 'sum',
    'Trip UUID': 'count'
  }).reset_index()
  city_stats.columns = ['Pickup City', 'Net Earnings', 'Tip', 'Fare', 'Trip Count']
  city_stats['Base'] = city_stats['Fare'].where(city_stats['Fare'] > 0, city_stats['Net Earnings'])
  city_stats = city_stats[city_stats['Base'] > 0]
  city_stats['Tip Rate %'] = ((city_stats['Tip'] / city_stats['Base']) * 100).clip(upper=100).round(1)
  
  # Filter to meaningful sample size: at least $200 earnings and 3+ trips
  city_stats_filtered = city_stats[(city_stats['Net Earnings'] >= 200) & (city_stats['Trip Count'] >= 3)].copy()

  # Coordinates: use known map, otherwise default to Dallas centroid with jitter
  dallas_lat, dallas_lon = 32.7767, -96.7970
  city_stats_filtered['lat'] = city_stats_filtered['Pickup City'].map(lambda x: city_coords.get(x, (dallas_lat, dallas_lon))[0])
  city_stats_filtered['lon'] = city_stats_filtered['Pickup City'].map(lambda x: city_coords.get(x, (dallas_lat, dallas_lon))[1])
  missing_mask = ~city_stats_filtered['Pickup City'].isin(city_coords.keys())
  if missing_mask.any():
    city_stats_filtered.loc[missing_mask, 'lat'] = city_stats_filtered.loc[missing_mask, 'lat'] + np.random.normal(0, 0.05, missing_mask.sum())
    city_stats_filtered.loc[missing_mask, 'lon'] = city_stats_filtered.loc[missing_mask, 'lon'] + np.random.normal(0, 0.05, missing_mask.sum())

  if city_stats_filtered.empty:
    st.info("No cities with significant activity ($200+ earnings, 3+ trips). Focus on building volume in key areas.")
  else:
    fig_cities = px.scatter_mapbox(
      city_stats_filtered,
      lat='lat',
      lon='lon',
      size='Net Earnings',
      color='Tip Rate %',
      hover_name='Pickup City',
      hover_data={
        'Net Earnings': ':$,.0f',
        'Tip Rate %': ':.1f',
        'Trip Count': True,
        'lat': False,
        'lon': False
      },
      color_continuous_scale='RdYlGn',
      size_max=30,
      mapbox_style='streets',
      height=500
    )
    # Auto-zoom to fit data bounds
    lat_range = city_stats_filtered['lat'].max() - city_stats_filtered['lat'].min()
    lon_range = city_stats_filtered['lon'].max() - city_stats_filtered['lon'].min()
    center_lat = (city_stats_filtered['lat'].max() + city_stats_filtered['lat'].min()) / 2
    center_lon = (city_stats_filtered['lon'].max() + city_stats_filtered['lon'].min()) / 2
    max_range = max(lat_range, lon_range) if max(lat_range, lon_range) > 0 else 1
    # Better zoom calculation: lower number = more zoomed out, can see more area
    if max_range < 0.2:
      zoom_level = 14
    elif max_range < 0.5:
      zoom_level = 12
    elif max_range < 1:
      zoom_level = 11
    elif max_range < 2:
      zoom_level = 10
    else:
      zoom_level = 9
    fig_cities.update_layout(
      margin=dict(l=0, r=0, t=0, b=0),
      mapbox=dict(center=dict(lat=center_lat, lon=center_lon), zoom=zoom_level),
      height=500
    )
    st.plotly_chart(fig_cities, use_container_width=True, key="cities_map")
  
  # Top 5 cities by tip rate (from filtered set)
  top_tip_cities = city_stats_filtered.nlargest(5, 'Tip Rate %')[['Pickup City', 'Tip Rate %', 'Net Earnings', 'Trip Count']]
  st.caption("**Sweet Spots (Best Tip Rates with Significant Volume):**")
  for _, row in top_tip_cities.iterrows():
    st.caption(f"- **{row['Pickup City']}**: {row['Tip Rate %']:.1f}% tip rate, {format_money(row['Net Earnings'])} total ({int(row['Trip Count'])} trips)")
  
  st.divider()
  
  # CHART VIEW: Best Restaurants by Earnings and Quality
  st.subheader("🍔 Best Restaurants by Earnings & Quality")
  
  st.markdown("""
  **Quality Metrics:** We measure restaurant performance using two key indicators:
  
  - **Average Per Trip:** $\\bar{x}_{\\text{trip}} = \\frac{\\text{Total Earnings}}{\\text{Trip Count}}$
  - **Quality Score:** $Q = 100\\% - \\text{Reimbursement Rate}\\%$ (higher is better)
  
  Restaurants with more trips and higher quality scores are more reliable income sources.
  """)
  
  rest_stats = (
    tx.groupby('Restaurant')
      .agg(
        Net_Earnings=('Net Earnings', 'sum'),
        Avg_Earnings=('Net Earnings', 'mean'),
        Refund_Count=('Refund', lambda x: (x != 0).sum()),
        Trip_Count=('Restaurant', 'size'),
        City=('Pickup City', lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown')
      )
      .reset_index()
  )
  rest_stats.columns = ['Restaurant', 'Net Earnings', 'Avg Earnings', 'Refund Count', 'Trip Count', 'City']
  rest_stats['Refund Rate %'] = (rest_stats['Refund Count'] / rest_stats['Trip Count'] * 100).round(1)
  rest_stats['Quality Score'] = (100 - rest_stats['Refund Rate %']).round(1)

  # Filter for restaurants with 3+ trips and sort by total earnings
  top_restaurants = rest_stats[rest_stats['Trip Count'] >= 3].nlargest(15, 'Net Earnings')

  if not top_restaurants.empty:
    # Create bubble chart: X=Total Earnings, Y=Quality Score, Size=Trip Count
    fig_restaurants = px.scatter(
      top_restaurants,
      x='Net Earnings',
      y='Quality Score',
      size='Trip Count',
      color='Avg Earnings',
      hover_name='Restaurant',
      hover_data={
        'City': True,
        'Net Earnings': ':$,.0f',
        'Avg Earnings': ':$,.2f',
        'Quality Score': ':.1f',
        'Trip Count': True,
        'Refund Count': True
      },
      color_continuous_scale='RdYlGn',
      size_max=50,
      height=500,
      labels={
        'Net Earnings': 'Total Earnings ($)',
        'Quality Score': 'Quality Score (100 = perfect)',
        'Avg Earnings': 'Avg per Trip'
      }
    )
    fig_restaurants.update_layout(
      title="Restaurant Performance: Earnings vs Quality (bubble size = trip count)",
      xaxis_title="Total Earnings ($)",
      yaxis_title="Quality Score (lower = more refunds)",
      showlegend=True,
      hovermode='closest'
    )
    # Add reference line at 85% quality
    fig_restaurants.add_hline(y=85, line_dash="dash", line_color="orange", 
                             annotation_text="Quality Threshold (85%)", 
                             annotation_position="right")
    st.plotly_chart(fig_restaurants, use_container_width=True, key="restaurants_chart")
    
    st.caption("💡 **Look for**: Large bubbles (many trips) in the upper-right (high earnings + quality). Avoid bottom-left (low earnings + poor quality).")
  
  st.divider()
  
  # Show top 5 by earnings and top 5 by quality side by side with better UI
  col1, col2 = st.columns(2)
  
  with col1:
    st.subheader("Top 5 by Total Earnings")
    top_by_earnings = rest_stats[rest_stats['Trip Count'] >= 3].nlargest(5, 'Net Earnings')
    for idx, (_, row) in enumerate(top_by_earnings.iterrows(), 1):
      logo = get_restaurant_logo(row['Restaurant'])
      logo_html = f'<img src="{logo}" style="height:28px; margin-right:10px; vertical-align:middle; border-radius:4px; display:inline-block;" onerror="this.style.display=\'none\'">' if logo else ""
      st.markdown(f"""
{idx}. {logo_html}**{row['Restaurant']}**  
   {format_money(row['Net Earnings'])} • {int(row['Trip Count'])} trips • {row['Quality Score']:.0f}% quality
""", unsafe_allow_html=True)
  
  with col2:
    st.subheader("Top 5 by Quality Score")
    top_by_quality = rest_stats[(rest_stats['Trip Count'] >= 5) & (rest_stats['Net Earnings'] > 50)].nlargest(5, 'Quality Score')
    if not top_by_quality.empty:
      for idx, (_, row) in enumerate(top_by_quality.iterrows(), 1):
        logo = get_restaurant_logo(row['Restaurant'])
        logo_html = f'<img src="{logo}" style="height:28px; margin-right:10px; vertical-align:middle; border-radius:4px; display:inline-block;" onerror="this.style.display=\'none\'">' if logo else ""
        st.markdown(f"""
{idx}. {logo_html}**{row['Restaurant']}**  
   {row['Quality Score']:.0f}% quality • {format_money(row['Net Earnings'])} • 0 refunds
""", unsafe_allow_html=True)
    else:
      st.info("Need 5+ trips and $50+ earnings to rank")
  
  st.divider()
  
  # High reimbursement (Shop & Pay / Order & Pay) restaurants
  high_refund = rest_stats[rest_stats['Refund Rate %'] > 15].nlargest(5, 'Refund Count')
  if not high_refund.empty:
    st.subheader("High Reimbursement Locations")
    st.caption("Shop & Pay / Order & Pay: you paid, later reimbursed")
    for idx, (_, row) in enumerate(high_refund.iterrows(), 1):
      refund_pct = row['Refund Rate %']
      logo = get_restaurant_logo(row['Restaurant'])
      logo_html = f'<img src="{logo}" style="height:28px; margin-right:10px; vertical-align:middle; border-radius:4px; display:inline-block;" onerror="this.style.display=\'none\'">' if logo else ""
      st.markdown(f"""
{idx}. {logo_html}**{row['Restaurant']}** ({row['City']})  
   {int(row['Refund Count'])}/{int(row['Trip Count'])} refunds ({refund_pct:.1f}%)
""", unsafe_allow_html=True)
  
  st.divider()

# ============================================================================
# PAGE: LOCATION INTELLIGENCE
# ============================================================================

elif page == "Locations":
  st.title("Location Intelligence")
  st.write("Which cities, restaurants, and areas pay best?")
  
  st.markdown("""
  **Earnings by Location Formula:**
  
  $$\\text{{Location Quality}} = \\text{{Avg Earnings per Trip}} \\times \\frac{{\\text{{Trip Count}}}}{{\\text{{Total Trips}}}}$$
  
  Locations with high average earnings AND good volume are your "sweet spots"—prioritize them!
  """)
  
  st.divider()
  
  # City coordinates
  city_coords = {
    'Dallas': (32.7767, -96.7970),
    'Plano': (33.0198, -96.6989),
    'McKinney': (33.1972, -96.6397),
    'Frisco': (33.1507, -96.8236),
    'Allen': (33.1031, -96.6705),
    'Richardson': (32.9483, -96.7299),
    'Garland': (32.9126, -96.6389),
    'Mesquite': (32.7668, -96.5992),
    'Irving': (32.8140, -96.9489),
    'Carrollton': (32.9537, -96.8903),
    'Lewisville': (33.0462, -96.9942),
    'Denton': (33.2148, -97.1331),
    'Fort Worth': (32.7555, -97.3308),
    'Arlington': (32.7357, -97.1081),
    'Forney': (32.7479, -96.4719),
    'Balch Springs': (32.7287, -96.6228),
    'Seagoville': (32.6390, -96.5386)
  }
  
  # Map view selector
  map_view = st.radio(
    "Map View",
    ["City Aggregation", "Heatmap Performance", "Individual Trips"],
    horizontal=True
  )
  
  if map_view == "City Aggregation":
    # Aggregate by city
    city_agg = tx.groupby('Pickup City').agg({
      'Net Earnings': 'sum',
      'Trip UUID': 'count'
    }).reset_index()
    city_agg.columns = ['City', 'Total Earnings', 'Trip Count']
    
    # Add coordinates
    map_data = []
    for _, row in city_agg.iterrows():
      if row['City'] in city_coords:
        map_data.append({
          'City': row['City'],
          'lat': city_coords[row['City']][0],
          'lon': city_coords[row['City']][1],
          'Earnings': row['Total Earnings'],
          'Trips': row['Trip Count']
        })
    
    if map_data:
      map_df = pd.DataFrame(map_data)
      fig = px.scatter_mapbox(
        map_df,
        lat='lat',
        lon='lon',
        size='Earnings',
        color='Earnings',
        hover_name='City',
        hover_data={'Earnings': ':$.2f', 'Trips': True, 'lat': False, 'lon': False},
        color_continuous_scale=['#6ba3d0', '#1e5a96', '#1a3a52'],
        size_max=50,
        height=500,
        mapbox_style='streets'
      )
      # Auto-zoom to fit data
      if len(map_df) > 0:
        lat_range = map_df['lat'].max() - map_df['lat'].min()
        lon_range = map_df['lon'].max() - map_df['lon'].min()
        center_lat = (map_df['lat'].max() + map_df['lat'].min()) / 2
        center_lon = (map_df['lon'].max() + map_df['lon'].min()) / 2
        max_range = max(lat_range, lon_range) if max(lat_range, lon_range) > 0 else 1
        if max_range < 0.2:
          zoom = 14
        elif max_range < 0.5:
          zoom = 12
        elif max_range < 1:
          zoom = 11
        elif max_range < 2:
          zoom = 10
        else:
          zoom = 9
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), mapbox=dict(center=dict(lat=center_lat, lon=center_lon), zoom=zoom))
      else:
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
      st.plotly_chart(fig, use_container_width=True)
  
  elif map_view == "Heatmap Performance":
    # Create heatmap with city earnings
    heat_data = []
    for city, coords in city_coords.items():
      city_earnings = tx[tx['Pickup City'] == city]['Net Earnings'].mean()
      if pd.notna(city_earnings):
        heat_data.append({
          'lat': coords[0],
          'lon': coords[1],
          'earnings': city_earnings
        })
    
    if heat_data:
      heatmap_df = pd.DataFrame(heat_data)
      fig = px.density_mapbox(
        heatmap_df,
        lat='lat',
        lon='lon',
        z='earnings',
        radius=25,
        mapbox_style='streets',
        height=500,
        color_continuous_scale=['#6ba3d0', '#1e5a96', '#1a3a52']
      )
      # Auto-zoom
      center_lat = 32.9
      center_lon = -96.8
      if len(heatmap_df) > 0:
        lat_range = heatmap_df['lat'].max() - heatmap_df['lat'].min()
        lon_range = heatmap_df['lon'].max() - heatmap_df['lon'].min()
        center_lat = (heatmap_df['lat'].max() + heatmap_df['lat'].min()) / 2
        center_lon = (heatmap_df['lon'].max() + heatmap_df['lon'].min()) / 2
        max_range = max(lat_range, lon_range) if max(lat_range, lon_range) > 0 else 1
        if max_range < 0.2:
          zoom = 14
        elif max_range < 0.5:
          zoom = 12
        elif max_range < 1:
          zoom = 11
        elif max_range < 2:
          zoom = 10
        else:
          zoom = 9
      else:
        zoom = 9
      fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), mapbox=dict(center=dict(lat=center_lat, lon=center_lon), zoom=zoom))
      st.plotly_chart(fig, use_container_width=True)
      
      # Stats table
      st.subheader("Performance Stats")
      stats = tx.groupby('Pickup City').agg({
        'Net Earnings': ['mean', 'sum', 'count'],
        'Tip': 'mean'
      }).round(2)
      stats.columns = ['Avg Earnings', 'Total', 'Trips', 'Avg Tip']
      stats = stats.sort_values('Avg Earnings', ascending=False).head(10)
      st.dataframe(stats, use_container_width=True)
  
  else:  # Individual Trips
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
      min_earn = st.number_input("Min Earnings", value=0.0, step=5.0)
    with col2:
      max_earn = st.number_input("Max Earnings", value=50.0, step=5.0)
    with col3:
      # Create human-friendly month options
      month_options = ['All'] + sorted(tx['Month'].unique().tolist())
      month_display = ['All'] + [format_month_human(m) for m in sorted(tx['Month'].unique().tolist())]
      selected_month_display = st.selectbox("Month", month_display)
      # Convert back to YYYY-MM format for filtering
      if selected_month_display == 'All':
        selected_month = 'All'
      else:
        selected_month_idx = month_display.index(selected_month_display)
        selected_month = month_options[selected_month_idx]
    
    # Filter data
    filtered = tx[(tx['Net Earnings'] >= min_earn) & (tx['Net Earnings'] <= max_earn)]
    if selected_month != 'All':
      filtered = filtered[filtered['Month'] == selected_month]
    
    # Map individual trips
    trip_data = []
    for _, row in filtered.head(200).iterrows():
      city = row['Pickup City']
      if city in city_coords:
        trip_data.append({
          'lat': city_coords[city][0],
          'lon': city_coords[city][1],
          'Earnings': row['Net Earnings'],
          'Restaurant': row['Restaurant'],
          'City': city
        })
    
    if trip_data:
      trip_df = pd.DataFrame(trip_data)
      fig = px.scatter_mapbox(
        trip_df,
        lat='lat',
        lon='lon',
        color='Earnings',
        size='Earnings',
        hover_name='Restaurant',
        hover_data={'City': True, 'Earnings': ':$.2f', 'lat': False, 'lon': False},
        color_continuous_scale=['#6ba3d0', '#1e5a96', '#1a3a52'],
        size_max=15,
        height=500,
        mapbox_style='streets'
      )
      # Auto-zoom
      if len(trip_df) > 0:
        lat_range = trip_df['lat'].max() - trip_df['lat'].min()
        lon_range = trip_df['lon'].max() - trip_df['lon'].min()
        center_lat = (trip_df['lat'].max() + trip_df['lat'].min()) / 2
        center_lon = (trip_df['lon'].max() + trip_df['lon'].min()) / 2
        max_range = max(lat_range, lon_range) if max(lat_range, lon_range) > 0 else 1
        if max_range < 0.2:
          zoom = 14
        elif max_range < 0.5:
          zoom = 12
        elif max_range < 1:
          zoom = 11
        elif max_range < 2:
          zoom = 10
        else:
          zoom = 9
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), mapbox=dict(center=dict(lat=center_lat, lon=center_lon), zoom=zoom))
      else:
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
      st.plotly_chart(fig, use_container_width=True)
  
  st.divider()
  
  # Top cities at a glance
  st.subheader(" Your Top Cities")
  
  top_cities_quick = tx['Pickup City'].value_counts().head(5).index
  cols = st.columns(len(top_cities_quick))
  
  for idx, city in enumerate(top_cities_quick):
    city_trips = tx[tx['Pickup City'] == city]
    with cols[idx]:
      st.metric(
        city,
        format_money(city_trips['Net Earnings'].mean()),
        f"{len(city_trips)} trips"
      )
  
  st.divider()
  
  # City analysis
  st.subheader(" Best Cities to Work (by earnings)")
  
  city_stats = tx.groupby('Pickup City').agg({
    'Net Earnings': ['sum', 'mean', 'count'],
    'Trip distance': 'mean',
    'Tip': 'sum'
  }).round(2)
  city_stats.columns = ['Total', 'Avg Earnings', 'Trip Count', 'Avg Distance', 'Total Tips']
  city_stats = city_stats[city_stats['Trip Count'] >= 2].sort_values('Avg Earnings', ascending=False)
  
  city_display = city_stats.copy()
  city_display['Total'] = city_display['Total'].apply(format_money)
  city_display['Avg Earnings'] = city_display['Avg Earnings'].apply(format_money)
  city_display['Total Tips'] = city_display['Total Tips'].apply(format_money)
  city_display['Avg Distance'] = city_display['Avg Distance'].apply(lambda x: f"{x:.1f}mi")
  
  st.dataframe(city_display, width='stretch')
  st.caption("Focus here: High avg earnings + good tip rates = sweet spots")
  
  st.divider()
  
  # Top restaurants
  st.subheader(" Best Restaurants to Pickup From")
  
  restaurant_stats = tx.groupby('Restaurant').agg({
    'Net Earnings': ['sum', 'mean', 'count'],
    'Tip': ['sum', 'mean'],
    'Refund': 'sum'
  }).round(2)
  restaurant_stats.columns = ['Total $', 'Avg Per Trip', 'Trips', 'Total Tips', 'Avg Tip', 'Total Refunds']
  restaurant_stats = restaurant_stats[restaurant_stats['Trips'] >= 2].sort_values('Avg Per Trip', ascending=False)
  
  rest_display = restaurant_stats.copy()
  rest_display['Total $'] = rest_display['Total $'].apply(format_money)
  rest_display['Avg Per Trip'] = rest_display['Avg Per Trip'].apply(format_money)
  rest_display['Total Tips'] = rest_display['Total Tips'].apply(format_money)
  rest_display['Avg Tip'] = rest_display['Avg Tip'].apply(format_money)
  rest_display['Total Refunds'] = rest_display['Total Refunds'].apply(format_money)
  rest_display['Trips'] = rest_display['Trips'].astype(int)
  
  st.dataframe(rest_display, width='stretch')

# ============================================================================
# PAGE: SCHEDULE OPTIMIZER
# ============================================================================

elif page == "Schedule":
  st.title("Schedule Optimizer")
  st.write("Best times to work: hours and days that pay the most")
  
  st.divider()
  
  # Hourly analysis
  st.subheader("Earnings by Hour of Day")
  
  hourly = tx.groupby('Hour').agg({
    'Net Earnings': ['sum', 'mean', 'count'],
    'Tip': 'mean'
  }).round(2)
  hourly.columns = ['Total', 'Avg Per Trip', 'Trip Count', 'Avg Tip']
  hourly = hourly.sort_index()
  
  fig = go.Figure()
  fig.add_trace(go.Bar(
    x=hourly.index,
    y=hourly['Avg Per Trip'],
    name='Avg Per Trip',
    marker_color='lightblue',
    yaxis='y'
  ))
  fig.add_trace(go.Scatter(
    x=hourly.index,
    y=hourly['Trip Count'],
    name='Trip Count',
    marker_color='red',
    yaxis='y2'
  ))
  fig.update_layout(
    title="Average Earnings & Trip Volume by Hour",
    xaxis_title="Hour of Day",
    yaxis=dict(title="Avg Earnings per Trip ($)"),
    yaxis2=dict(title="Number of Trips", overlaying='y', side='right'),
    hovermode='x unified',
    height=400
  )
  st.plotly_chart(fig, width='stretch')
  
  st.divider()
  
  # Day of week analysis
  st.subheader(" Earnings by Day of Week")
  
  dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  daily_stats = tx.groupby('DayOfWeek').agg({
    'Net Earnings': ['sum', 'mean', 'count']
  }).reindex(dow_order)
  daily_stats.columns = ['Total', 'Avg Per Trip', 'Trip Count']
  
  fig = px.bar(daily_stats.reset_index(), x='DayOfWeek', y='Total',
        title="Total Earnings by Day of Week",
        color='Total',
        color_continuous_scale='Greens',
        height=400)
  fig.update_xaxes(categoryorder="array", categoryarray=dow_order)
  st.plotly_chart(fig, width='stretch')
  
  st.divider()
  
  # Recommendation
  st.subheader(" Your Optimal Schedule")
  best_hour = hourly['Avg Per Trip'].idxmax()
  best_day = daily_stats['Avg Per Trip'].idxmax()
  
  col1, col2 = st.columns(2)
  col1.success(f"Best Hour: {best_hour:02d}:00 - {format_money(hourly.loc[best_hour, 'Avg Per Trip'])} avg")
  col2.success(f"Best Day: {best_day} - {format_money(daily_stats.loc[best_day, 'Avg Per Trip'])} avg")

# ============================================================================
# PAGE: MILEAGE EFFICIENCY
# ============================================================================
elif page == "Issues":
  st.title("Issue Tracker")
  st.write("Efficiency analysis, refunds, disputes, and anomalies")
  
  st.divider()
  
  # Tab selection
  issue_tab = st.radio(
    "Issue Category",
    ["Efficiency", "Refunds & Disputes", "Anomalies"],
    horizontal=True
  )
  
  st.divider()
  
  if issue_tab == "Efficiency":
    st.subheader("Mileage Efficiency Analysis")
    
    st.markdown(f"""
    **Efficiency Calculation:**
    
    $$\\text{{Efficiency}} = \\frac{{\\text{{Total Net Earnings}}}}{{\\text{{Total Miles}}}} = \\frac{{{format_money(total_earnings)}}}{{{total_miles:,.0f} \\text{{ mi}}}} = {format_money(avg_per_mile)}/\\text{{mi}}$$
    
    Your efficiency score measures how much you earn per mile driven. Higher is better!
    """)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Miles", f"{total_miles:,.0f}")
    col2.metric("Total Earnings", format_money(total_earnings))
    col3.metric("$/Mile (Overall)", format_money(avg_per_mile))
    col4.metric("Efficiency Score", f"{(avg_per_mile * 10):.1f}/10", help="$/Mile normalized to 10")
    
    st.divider()
    
    # Most efficient trips (require valid distance)
    st.subheader("Most Efficient Trips ($/Mile)")
    valid_eff = tx[(tx['Trip distance'].notna()) & (tx['Trip distance'] > 0)]
    missing_distance = len(tx) - len(valid_eff)
    
    if valid_eff.empty:
      st.info("No trips have a recorded distance. The source export may have missing distance data.")
    else:
      efficient = valid_eff.nlargest(10, 'Earnings Per Mile')[['Trip drop off time', 'Restaurant', 'Pickup City', 'Trip distance', 'Net Earnings', 'Earnings Per Mile']]
      eff_display = efficient.copy()
      eff_display['Trip drop off time'] = eff_display['Trip drop off time'].dt.strftime('%m-%d %H:%M')
      eff_display['Location'] = eff_display['Restaurant'] + ' (' + eff_display['Pickup City'] + ')'
      eff_display = eff_display[['Trip drop off time', 'Location', 'Trip distance', 'Net Earnings', 'Earnings Per Mile']]
      eff_display['Trip distance'] = eff_display['Trip distance'].apply(lambda x: f"{x:.1f}mi")
      eff_display['Net Earnings'] = eff_display['Net Earnings'].apply(format_money)
      eff_display['Earnings Per Mile'] = eff_display['Earnings Per Mile'].apply(format_money)
      
      st.dataframe(eff_display, width='stretch', hide_index=True)
      st.caption("These trips require a recorded distance. Short distance, good payout = maximize these!")
    
    if missing_distance > 0:
      st.caption(f"{missing_distance} trips skipped because distance was missing or zero in the source export.")
  
  elif issue_tab == "Refunds & Disputes":
    st.subheader("Refunds & Dispute Forensics (Shop & Pay / Order & Pay reimbursements you fronted)")
    
    # Refund summary
    refunded_trips = tx[tx['Refund'] != 0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Refunded Trips (Shop/Order & Pay)", len(refunded_trips))
    col2.metric("Refund Rate", format_percent(refund_rate))
    col3.metric("Total Reimbursed (you fronted)", format_money(tx['Refund'].sum()))
    
    st.divider()
    
    # Refunded trips detail
    if not refunded_trips.empty:
      ref_display = refunded_trips[['Trip drop off time', 'Restaurant', 'Pickup City', 'Trip distance', 'Net Earnings', 'Refund']].copy()
      ref_display['Trip drop off time'] = ref_display['Trip drop off time'].dt.strftime('%m-%d %H:%M')
      ref_display['Location'] = ref_display['Restaurant'] + ' (' + ref_display['Pickup City'] + ')'
      ref_display = ref_display[['Trip drop off time', 'Location', 'Trip distance', 'Net Earnings', 'Refund']]
      ref_display['Trip distance'] = ref_display['Trip distance'].apply(lambda x: f"{x:.1f}mi")
      ref_display['Net Earnings'] = ref_display['Net Earnings'].apply(format_money)
      ref_display['Refund'] = ref_display['Refund'].apply(format_money)
      
      st.dataframe(ref_display, width='stretch', hide_index=True)
    else:
      st.success("No refunds found!")
  
  elif issue_tab == "Anomalies":
    st.subheader("Payment Anomalies")
    
    # Low pay anomalies
    low_pay = tx[tx['Net Earnings'] < 2.50]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Trips <$2.50", len(low_pay))
    col2.metric("Total Low Pay", format_money(low_pay['Net Earnings'].sum()))
    col3.metric("Lost Potential", format_money(len(low_pay) * 3.00 - low_pay['Net Earnings'].sum()), help="If they were $3 each")
    
    st.divider()
    
    if not low_pay.empty:
      low_pay_display = low_pay[['Trip drop off time', 'Restaurant', 'Pickup City', 'Trip distance', 'Net Earnings', 'Tip']].copy()
      low_pay_display['Trip drop off time'] = low_pay_display['Trip drop off time'].dt.strftime('%m-%d %H:%M')
      low_pay_display['Location'] = low_pay_display['Restaurant'] + ' (' + low_pay_display['Pickup City'] + ')'
      low_pay_display = low_pay_display[['Trip drop off time', 'Location', 'Trip distance', 'Net Earnings', 'Tip']]
      low_pay_display['Trip distance'] = low_pay_display['Trip distance'].apply(lambda x: f"{x:.1f}mi")
      low_pay_display['Net Earnings'] = low_pay_display['Net Earnings'].apply(format_money)
      low_pay_display['Tip'] = low_pay_display['Tip'].apply(format_money)
      st.dataframe(low_pay_display.head(20), width='stretch', hide_index=True)

# ============================================================================
# PAGE: ROUTE OPTIMIZER
# ============================================================================

elif page == "Routes":
  st.title("Route Optimizer")
  st.write("Find the best areas to work based on time, earnings, and demand patterns")
  
  st.divider()
  
  # ===== MAP 1: TRIP PICKUP HEATMAP =====
  st.subheader("📍 Pickup Location Density Heatmap")
  st.caption("Heat intensity = number of trips from that area")
  
  pickup_data = tx[tx['Pickup City'].notna()].copy()
  if not pickup_data.empty:
    dallas_lat, dallas_lon = 32.7767, -96.7970
    city_coords = {
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
    }
    
    pickup_data['lat'] = pickup_data['Pickup City'].map(lambda x: city_coords.get(x, (dallas_lat, dallas_lon))[0])
    pickup_data['lon'] = pickup_data['Pickup City'].map(lambda x: city_coords.get(x, (dallas_lat, dallas_lon))[1])
    
    # Add jitter to prevent overlapping
    pickup_data['lat'] = pickup_data['lat'] + np.random.normal(0, 0.03, len(pickup_data))
    pickup_data['lon'] = pickup_data['lon'] + np.random.normal(0, 0.03, len(pickup_data))
    
    fig_pickup = px.density_mapbox(
      pickup_data,
      lat='lat',
      lon='lon',
      mapbox_style='streets',
      height=500,
      color_continuous_scale='Viridis',
      radius=40,
      zoom=9
    )
    fig_pickup.update_layout(
      margin=dict(l=0, r=0, t=0, b=0),
      mapbox=dict(center=dict(lat=32.85, lon=-96.85), zoom=9)
    )
    st.plotly_chart(fig_pickup, use_container_width=True, key="pickup_heatmap")
  else:
    st.warning("No pickup location data available")
  
  st.divider()
  
  # ===== MAP 2: TOP EARNING ZONES =====
  st.subheader("💰 Top Earning Zones by Location")
  st.caption("Street-level view of top earning pickup locations")
  
  # Get actual pickup coordinates from addresses
  pickup_with_address = tx[tx['Pickup address'].notna()].copy()
  
  if not pickup_with_address.empty:
    # Get unique addresses to geocode
    unique_addresses = tuple(pickup_with_address['Pickup address'].unique().tolist())
    
    with st.spinner(f"🔄 Geocoding {len(unique_addresses)} addresses... (this may take a moment)"):
      coords_dict = get_coordinates_for_addresses(unique_addresses)
    
    # Add coordinates to data
    pickup_with_address['lat'] = pickup_with_address['Pickup address'].map(lambda x: coords_dict.get(x, (None, None))[0])
    pickup_with_address['lon'] = pickup_with_address['Pickup address'].map(lambda x: coords_dict.get(x, (None, None))[1])
    
    # Remove rows without coordinates
    pickup_with_coords = pickup_with_address[pickup_with_address['lat'].notna() & pickup_with_address['lon'].notna()]
    
    if not pickup_with_coords.empty:
      # Aggregate by address 
      pickup_agg = pickup_with_coords.groupby('Pickup address').agg({
        'Net Earnings': ['sum', 'mean'],
        'Trip UUID': 'count',
        'lat': 'first',
        'lon': 'first'
      }).reset_index()
      pickup_agg.columns = ['Address', 'Total Earnings', 'Avg per Trip', 'Trip Count', 'lat', 'lon']
      pickup_agg = pickup_agg[pickup_agg['Trip Count'] >= 2].sort_values('Total Earnings', ascending=False).head(20)
      
      if not pickup_agg.empty:
        fig_pickup_zones = px.scatter_mapbox(
          pickup_agg,
          lat='lat',
          lon='lon',
          size='Total Earnings',
          color='Avg per Trip',
          hover_name='Address',
          hover_data={
            'Total Earnings': ':$,.0f',
            'Avg per Trip': ':$,.2f',
            'Trip Count': True,
            'lat': False,
            'lon': False
          },
          color_continuous_scale='RdYlGn',
          size_max=30,
          mapbox_style='streets',
          height=500
        )
        
        # Auto-zoom
        lat_range = pickup_agg['lat'].max() - pickup_agg['lat'].min()
        lon_range = pickup_agg['lon'].max() - pickup_agg['lon'].min()
        center_lat = (pickup_agg['lat'].max() + pickup_agg['lat'].min()) / 2
        center_lon = (pickup_agg['lon'].max() + pickup_agg['lon'].min()) / 2
        max_range = max(lat_range, lon_range) if max(lat_range, lon_range) > 0 else 1
        
        if max_range < 0.02:
          zoom_level = 16
        elif max_range < 0.05:
          zoom_level = 15
        elif max_range < 0.1:
          zoom_level = 14
        elif max_range < 0.2:
          zoom_level = 13
        elif max_range < 0.5:
          zoom_level = 12
        elif max_range < 1:
          zoom_level = 11
        elif max_range < 2:
          zoom_level = 10
        else:
          zoom_level = 9
        
        fig_pickup_zones.update_layout(
          margin=dict(l=0, r=0, t=0, b=0),
          mapbox=dict(center=dict(lat=center_lat, lon=center_lon), zoom=zoom_level),
          height=500
        )
        st.plotly_chart(fig_pickup_zones, use_container_width=True, key="pickup_zones_map")
      else:
        st.info("No locations with 2+ trips found")
    else:
      geocoded_count = sum(1 for lat, lon in coords_dict.values() if lat and lon)
      st.warning(f"Only {geocoded_count}/{len(unique_addresses)} addresses could be geocoded. Geocoding service may have limits.")
  else:
    st.info("No pickup address data available")
  
  st.divider()
  
  # ===== TABLE + MAP: TOP CITIES =====
  st.subheader("🏙️ Top Cities by Earnings")
  
  city_stats = tx.groupby('Pickup City').agg({
    'Net Earnings': ['sum', 'mean', 'count']
  }).round(2)
  city_stats.columns = ['Total', 'Avg Earnings', 'Trip Count']
  city_stats = city_stats[city_stats['Trip Count'] >= 5].sort_values('Avg Earnings', ascending=False).head(10)
  
  # Add coordinates for map
  city_stats['lat'] = city_stats.index.map(lambda x: city_coords.get(x, (dallas_lat, dallas_lon))[0])
  city_stats['lon'] = city_stats.index.map(lambda x: city_coords.get(x, (dallas_lat, dallas_lon))[1])
  city_stats_with_coords = city_stats.reset_index()
  
  # Map view
  if not city_stats_with_coords.empty:
    fig_top_cities = px.scatter_mapbox(
      city_stats_with_coords,
      lat='lat',
      lon='lon',
      size='Total',
      color='Avg Earnings',
      hover_name='Pickup City',
      hover_data={
        'Total': ':$,.0f',
        'Avg Earnings': ':$,.2f',
        'Trip Count': True,
        'lat': False,
        'lon': False
      },
      color_continuous_scale='Viridis',
      size_max=45,
      mapbox_style='streets',
      height=450
    )
    # Auto-zoom
    lat_range = city_stats_with_coords['lat'].max() - city_stats_with_coords['lat'].min()
    lon_range = city_stats_with_coords['lon'].max() - city_stats_with_coords['lon'].min()
    center_lat = (city_stats_with_coords['lat'].max() + city_stats_with_coords['lat'].min()) / 2
    center_lon = (city_stats_with_coords['lon'].max() + city_stats_with_coords['lon'].min()) / 2
    max_range = max(lat_range, lon_range) if max(lat_range, lon_range) > 0 else 1
    if max_range < 0.2:
      zoom = 14
    elif max_range < 0.5:
      zoom = 12
    elif max_range < 1:
      zoom = 11
    elif max_range < 2:
      zoom = 10
    else:
      zoom = 9
    fig_top_cities.update_layout(
      margin=dict(l=0, r=0, t=0, b=0),
      mapbox=dict(center=dict(lat=center_lat, lon=center_lon), zoom=zoom)
    )
    st.plotly_chart(fig_top_cities, use_container_width=True, key="top_cities_map")
  
  # Table view
  city_display = city_stats.copy()
  city_display['Total'] = city_display['Total'].apply(format_money)
  city_display['Avg Earnings'] = city_display['Avg Earnings'].apply(format_money)
  city_display['Trip Count'] = city_display['Trip Count'].astype(int)
  
  st.dataframe(city_display, use_container_width=True)
  st.caption("Focus on cities with high average earnings and strong trip frequency")
  
  st.divider()
  
  # ===== TABLE + MAP: TOP RESTAURANTS =====
  st.subheader("🍔 Top Restaurants by Payouts")
  
  restaurant_stats = tx.groupby('Restaurant').agg({
    'Net Earnings': ['sum', 'mean', 'count'],
    'Pickup City': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown'
  }).round(2)
  restaurant_stats.columns = ['Total $', 'Avg Per Trip', 'Trips', 'City']
  restaurant_stats = restaurant_stats[restaurant_stats['Trips'] >= 3].sort_values('Avg Per Trip', ascending=False).head(10)
  
  # Add coordinates for map
  restaurant_stats['lat'] = restaurant_stats['City'].map(lambda x: city_coords.get(x, (dallas_lat, dallas_lon))[0])
  restaurant_stats['lon'] = restaurant_stats['City'].map(lambda x: city_coords.get(x, (dallas_lat, dallas_lon))[1])
  restaurant_stats_with_coords = restaurant_stats.reset_index()
  
  # Map view
  if not restaurant_stats_with_coords.empty:
    fig_top_restaurants = px.scatter_mapbox(
      restaurant_stats_with_coords,
      lat='lat',
      lon='lon',
      size='Total $',
      color='Avg Per Trip',
      hover_name='Restaurant',
      hover_data={
        'City': True,
        'Total $': ':$,.0f',
        'Avg Per Trip': ':$,.2f',
        'Trips': True,
        'lat': False,
        'lon': False
      },
      color_continuous_scale='RdYlGn',
      size_max=40,
      mapbox_style='streets',
      height=450
    )
    # Auto-zoom
    lat_range = restaurant_stats_with_coords['lat'].max() - restaurant_stats_with_coords['lat'].min()
    lon_range = restaurant_stats_with_coords['lon'].max() - restaurant_stats_with_coords['lon'].min()
    center_lat = (restaurant_stats_with_coords['lat'].max() + restaurant_stats_with_coords['lat'].min()) / 2
    center_lon = (restaurant_stats_with_coords['lon'].max() + restaurant_stats_with_coords['lon'].min()) / 2
    max_range = max(lat_range, lon_range) if max(lat_range, lon_range) > 0 else 1
    if max_range < 0.2:
      zoom = 14
    elif max_range < 0.5:
      zoom = 12
    elif max_range < 1:
      zoom = 11
    elif max_range < 2:
      zoom = 10
    else:
      zoom = 9
    fig_top_restaurants.update_layout(
      margin=dict(l=0, r=0, t=0, b=0),
      mapbox=dict(center=dict(lat=center_lat, lon=center_lon), zoom=zoom)
    )
    st.plotly_chart(fig_top_restaurants, use_container_width=True, key="top_restaurants_map")
  
  # Table view
  rest_display = restaurant_stats.copy()
  rest_display['Total $'] = rest_display['Total $'].apply(format_money)
  rest_display['Avg Per Trip'] = rest_display['Avg Per Trip'].apply(format_money)
  rest_display['Trips'] = rest_display['Trips'].astype(int)
  
  st.dataframe(rest_display, use_container_width=True)
  st.caption("These restaurants consistently provide the best payouts per trip")

# ============================================================================
# PAGE: ANOMALY DETECTION (REMOVED - CONSOLIDATED INTO ISSUES)
# ============================================================================

elif page == "Anomaly Detection":
  # Redirect to Issues page
  st.warning("This page has been consolidated into the Issues page. Redirecting...")
  st.session_state.current_page = "Issues"
  st.rerun()

# ============================================================================
# PAGE: DISPUTE FORENSICS (REMOVED - CONSOLIDATED INTO ISSUES)
# ============================================================================

elif page == "Dispute Forensics":
  # Redirect to Issues page
  st.warning("This page has been consolidated into the Issues page. Redirecting...")
  st.session_state.current_page = "Issues"
  st.rerun()

# ============================================================================
# PAGE: MILEAGE EFFICIENCY (REMOVED - CONSOLIDATED INTO ISSUES)
# ============================================================================

elif page == "Mileage Efficiency":
  # Redirect to Issues page
  st.warning("This page has been consolidated into the Issues page. Redirecting...")
  st.session_state.current_page = "Issues"
  st.rerun()

# ============================================================================
# PAGE: PAYMENT RECONCILIATION
# ============================================================================
  st.title("Mileage Efficiency")
  st.write("Minimize driving, maximize earnings. Track your efficiency.")
  
  st.divider()
  
  # Efficiency metrics
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Total Miles", f"{total_miles:,.0f}")
  col2.metric("Total Earnings", format_money(total_earnings))
  col3.metric("$/Mile (Overall)", format_money(avg_per_mile))
  col4.metric("Efficiency Score", f"{(avg_per_mile * 10):.1f}/10", help="$/Mile normalized to 10")
  
  st.divider()
  
  # Monthly efficiency trend
  st.subheader(" Efficiency Trend Over Time")
  
  monthly = tx.groupby('Month').agg({
    'Net Earnings': 'sum',
    'Trip distance': 'sum',
    'Trip UUID': 'count'
  }).round(2)
  monthly['Earnings Per Mile'] = (monthly['Net Earnings'] / monthly['Trip distance']).round(2)
  monthly = monthly.reset_index()
  
  fig = go.Figure()
  fig.add_trace(go.Scatter(
    x=monthly['Month'],
    y=monthly['Earnings Per Mile'],
    mode='lines+markers',
    name='$/Mile',
    line=dict(color='#1f77b4', width=3),
    marker=dict(size=10)
  ))
  fig.update_layout(
    title="Your Efficiency Trend ($/Mile)",
    xaxis_title="Month",
    yaxis_title="Earnings per Mile ($)",
    height=400,
    hovermode='x unified'
  )
  st.plotly_chart(fig, width='stretch')
  
  st.divider()
  
  # Trip distance distribution
  st.subheader(" Trip Distance Distribution")
  
  fig = px.histogram(tx, x='Trip distance', nbins=30,
           title="How far are your trips?",
           color_discrete_sequence=['#2ca02c'],
           height=400)
  fig.update_xaxes(title="Trip Distance (miles)")
  fig.update_yaxes(title="Number of Trips")
  st.plotly_chart(fig, width='stretch')
  
  st.divider()
  
  # Long distance vs short distance comparison
  st.subheader(" Short Trips vs Long Trips")
  
  short = tx[tx['Trip distance'] <= 3]
  long = tx[tx['Trip distance'] > 10]
  
  col1, col2 = st.columns(2)
  
  with col1:
    st.metric("Short Trips (≤3 mi)", len(short))
    st.metric(" Avg Earnings", format_money(short['Net Earnings'].mean()))
    st.metric(" $/Mile", format_money(short['Net Earnings'].sum() / short['Trip distance'].sum()))
  
  with col2:
    st.metric("Long Trips (>10 mi)", len(long))
    st.metric(" Avg Earnings", format_money(long['Net Earnings'].mean()))
    st.metric(" $/Mile", format_money(long['Net Earnings'].sum() / long['Trip distance'].sum() if long['Trip distance'].sum() > 0 else 0))

# ============================================================================
# PAGE: ANOMALY DETECTION
# ============================================================================

elif page == "Anomaly Detection":
  st.title("Anomaly Detection")
  st.write("Payment issues, refunds, and reconciliation problems")
  
  st.divider()
  
  # Refund summary
  st.subheader(" Refund Analysis")
  
  refunded_trips = tx[tx['Refund'] != 0]
  
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Refunded Trips", len(refunded_trips))
  col2.metric("Refund Rate", format_percent(refund_rate))
  col3.metric("Total Refunded", format_money(tx['Refund'].sum()))
  col4.metric("Avg Refund", format_money(refunded_trips['Refund'].mean() if len(refunded_trips) > 0 else 0))
  
  st.divider()
  
  # Refunded trips detail
  st.subheader("Refunded Trips Detail")
  
  if not refunded_trips.empty:
    ref_display = refunded_trips[['Trip drop off time', 'Restaurant', 'Pickup City', 'Trip distance', 'Net Earnings', 'Refund']].copy()
    ref_display['Trip drop off time'] = ref_display['Trip drop off time'].dt.strftime('%m-%d %H:%M')
    ref_display['Location'] = ref_display['Restaurant'] + ' (' + ref_display['Pickup City'] + ')'
    ref_display = ref_display[['Trip drop off time', 'Location', 'Trip distance', 'Net Earnings', 'Refund']]
    ref_display['Trip distance'] = ref_display['Trip distance'].apply(lambda x: f"{x:.1f}mi")
    ref_display['Net Earnings'] = ref_display['Net Earnings'].apply(format_money)
    ref_display['Refund'] = ref_display['Refund'].apply(format_money)
    
    st.dataframe(ref_display, width='stretch', hide_index=True)
  else:
    st.success("No refunds found!")
  
  st.divider()
  
  # Low pay anomalies
  st.subheader(" Suspiciously Low Payments")
  
  low_pay = tx[tx['Net Earnings'] < 2.50]
  
  col1, col2, col3 = st.columns(3)
  col1.metric("Trips <$2.50", len(low_pay))
  col2.metric("Total Low Pay", format_money(low_pay['Net Earnings'].sum()))
  col3.metric("Lost Potential", format_money(len(low_pay) * 3.00 - low_pay['Net Earnings'].sum()), help="If they were $3 each")
  
  if not low_pay.empty:
    low_pay_display = low_pay[['Trip drop off time', 'Restaurant', 'Pickup City', 'Trip distance', 'Net Earnings', 'Tip']].copy()
    low_pay_display['Trip drop off time'] = low_pay_display['Trip drop off time'].dt.strftime('%m-%d %H:%M')
    low_pay_display['Location'] = low_pay_display['Restaurant'] + ' (' + low_pay_display['Pickup City'] + ')'
    low_pay_display = low_pay_display[['Trip drop off time', 'Location', 'Trip distance', 'Net Earnings', 'Tip']]
    low_pay_display['Trip distance'] = low_pay_display['Trip distance'].apply(lambda x: f"{x:.1f}mi")
    low_pay_display['Net Earnings'] = low_pay_display['Net Earnings'].apply(format_money)
    low_pay_display['Tip'] = low_pay_display['Tip'].apply(format_money)
    st.dataframe(low_pay_display.head(20), width='stretch', hide_index=True)
  
  st.divider()
  
  # Bank reconciliation status
  if not multi_df.empty:
    st.subheader(" Bank Reconciliation Status")
    
    for idx, row in multi_df.iterrows():
      metric = str(row['Metric']).strip()
      value = str(row['Value']).strip()
      
      if 'Payments' in metric and 'Total' in metric:
        st.metric("Uber's Records", value)
      elif 'Total Deposits' in metric and 'All' in metric:
        st.metric("Bank Deposits (All)", value)
      elif 'Gap' in metric and 'Final' in metric:
        st.metric("Unaccounted Gap", value)
      elif 'Status' in metric:
        st.success(value)

# ============================================================================
# PAGE: PAYMENT RECONCILIATION
# ============================================================================

elif page == "Payments":
  st.title("Payment Reconciliation")
  st.write("Compare Uber payments reported to bank deposits • Track payment processing timeline")
  
  st.divider()
  
  # Summary metrics
  st.subheader("💵 Payment Summary")
  
  if not audit_df.empty:
    # Parse payment dates and strip timezone to keep both columns tz-naive
    audit_df['Payment Date'] = pd.to_datetime(audit_df['Payment Date'], errors='coerce', utc=True).dt.tz_convert(None)
    if 'Bank Deposit Date' in audit_df.columns:
      audit_df['Bank Deposit Date'] = pd.to_datetime(audit_df['Bank Deposit Date'], errors='coerce', utc=True).dt.tz_convert(None)
    
    total_payments = audit_df['Payment Net Earnings'].sum() if 'Payment Net Earnings' in audit_df.columns else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Uber Reported", format_money(total_payments))
    
    # Count matched deposits
    matched = len(audit_df[audit_df['Bank Deposit Date'].notna()]) if 'Bank Deposit Date' in audit_df.columns else 0
    total_count = len(audit_df)
    col2.metric("Deposits Matched", f"{matched}/{total_count}")
    
    # Reconciliation statuses
    if 'Reconciliation Status' in audit_df.columns:
      status_counts = audit_df['Reconciliation Status'].value_counts()
      bank_matched = status_counts.get('BANK_MATCHED', 0)
      refund_tracked = status_counts.get('REFUND_TRACKED', 0)
      col3.metric("Bank Matched", bank_matched)
      col4.metric("Refund Tracked", refund_tracked)
    
    # Expandable sections to view specific transactions
    st.markdown("---")
    st.markdown("**View Specific Transactions:**")
    
    view_option = st.selectbox(
      "Select Transaction Type",
      ["All Transactions", "Bank Matched Only", "Unmatched Deposits", "Refund Tracked", "Pending/Issues"],
      label_visibility="collapsed"
    )
    
    # Filter based on selection
    if view_option == "Bank Matched Only":
      filtered_df = audit_df[audit_df['Reconciliation Status'] == 'BANK_MATCHED'].copy()
      st.success(f"Showing {len(filtered_df)} bank-matched transactions")
    elif view_option == "Unmatched Deposits":
      filtered_df = audit_df[audit_df['Bank Deposit Date'].isna()].copy()
      st.warning(f"Showing {len(filtered_df)} unmatched transactions")
    elif view_option == "Refund Tracked":
      filtered_df = audit_df[audit_df['Reconciliation Status'] == 'REFUND_TRACKED'].copy()
      st.info(f"Showing {len(filtered_df)} refund-tracked transactions")
    elif view_option == "Pending/Issues":
      filtered_df = audit_df[~audit_df['Reconciliation Status'].isin(['BANK_MATCHED', 'REFUND_TRACKED'])].copy()
      st.error(f"Showing {len(filtered_df)} pending/issue transactions")
    else:
      filtered_df = audit_df.copy()
      st.info(f"Showing all {len(filtered_df)} transactions")
    
    # Display transactions with expandable details
    if not filtered_df.empty:
      st.markdown("**Click on any transaction to see full details:**")
      
      for idx, row in filtered_df.iterrows():
        # Create summary line
        payment_date_str = pd.to_datetime(row['Payment Date']).strftime('%B %d, %Y') if pd.notna(row.get('Payment Date')) else 'N/A'
        amount_str = format_money(row.get('Payment Net Earnings', 0))
        status_str = row.get('Reconciliation Status', 'Unknown')
        
        # Status emoji
        status_emoji = "✅" if status_str == "BANK_MATCHED" else "⚠️" if status_str == "REFUND_TRACKED" else "❌"
        
        with st.expander(f"{status_emoji} {payment_date_str} - {amount_str} ({status_str})"):
          # Create two columns for organized display
          col1, col2 = st.columns(2)
          
          with col1:
            st.markdown("**📄 Payment Information (Uber)**")
            if 'Payment Date' in row and pd.notna(row['Payment Date']):
              st.caption(f"Payment Date: {pd.to_datetime(row['Payment Date']).strftime('%B %d, %Y %I:%M %p')}")
            if 'Payment Net Earnings' in row:
              st.caption(f"Amount: {format_money(row['Payment Net Earnings'])}")
            if 'Payment Period Start' in row and pd.notna(row['Payment Period Start']):
              st.caption(f"Period Start: {pd.to_datetime(row['Payment Period Start']).strftime('%B %d, %Y')}")
            if 'Payment Period End' in row and pd.notna(row['Payment Period End']):
              st.caption(f"Period End: {pd.to_datetime(row['Payment Period End']).strftime('%B %d, %Y')}")
            if 'Trip Count' in row:
              st.caption(f"Trips in Period: {row['Trip Count']}")
            if 'Payment Method' in row:
              st.caption(f"Payment Method: {row['Payment Method']}")
          
          with col2:
            st.markdown("**🏦 Bank Information**")
            if 'Bank Deposit Date' in row:
              deposit_date = pd.to_datetime(row['Bank Deposit Date'], errors='coerce')
              if pd.notna(deposit_date):
                st.caption(f"Deposit Date: {deposit_date.strftime('%B %d, %Y')}")
              else:
                st.caption("Deposit Date: ⚠️ NOT FOUND IN BANK")
            if 'Bank Amount' in row and pd.notna(row['Bank Amount']):
              st.caption(f"Bank Amount: {format_money(row['Bank Amount'])}")
            if 'Bank Description' in row and pd.notna(row['Bank Description']):
              st.caption(f"Bank Description: {row['Bank Description']}")
            if 'Bank Account' in row and pd.notna(row['Bank Account']):
              st.caption(f"Account: {row['Bank Account']}")
            
            st.markdown("**📊 Reconciliation**")
            if 'Reconciliation Status' in row:
              st.caption(f"Status: {row['Reconciliation Status']}")
            if 'Match Confidence' in row and pd.notna(row['Match Confidence']):
              st.caption(f"Match Confidence: {row['Match Confidence']}")
            if 'Days to Deposit' in row and pd.notna(row['Days to Deposit']):
              st.caption(f"Days to Deposit: {int(row['Days to Deposit'])} days")
          
          # Show ALL available columns in expandable section
          st.markdown("---")
          st.markdown("**🔍 All Available Data:**")
          
          # Create a clean display of all non-null values
          all_data = {}
          for col in row.index:
            if pd.notna(row[col]) and row[col] != '':
              if 'Date' in col or 'Time' in col:
                try:
                  all_data[col] = pd.to_datetime(row[col]).strftime('%B %d, %Y %I:%M %p')
                except:
                  all_data[col] = str(row[col])
              elif 'Earnings' in col or 'Amount' in col or 'Fee' in col or 'Tip' in col:
                try:
                  all_data[col] = format_money(float(row[col]))
                except:
                  all_data[col] = str(row[col])
              else:
                all_data[col] = str(row[col])
          
          # Display as formatted text
          for key, value in all_data.items():
            st.caption(f"**{key}:** {value}")
  
  st.divider()
  
  # Daily breakdown
  st.subheader("📅 Daily Payment Timeline")
  
  if not audit_df.empty and 'Payment Date' in audit_df.columns:
    # Group by payment date to see daily totals
    daily_payment = audit_df.groupby(audit_df['Payment Date'].dt.date).agg({
      'Payment Net Earnings': 'sum'
    }).reset_index()
    daily_payment.columns = ['Date', 'Payments Reported']
    # Format dates as human-friendly
    daily_payment['Date'] = pd.to_datetime(daily_payment['Date']).dt.strftime('%B %d, %Y')
    
    # Group by deposit date if available
    if 'Bank Deposit Date' in audit_df.columns:
      daily_deposit = audit_df.dropna(subset=['Bank Deposit Date']).groupby(audit_df['Bank Deposit Date'].dt.date).agg({
        'Payment Net Earnings': 'sum'
      }).reset_index()
      daily_deposit.columns = ['Date', 'Bank Deposited']
      daily_deposit['Date'] = pd.to_datetime(daily_deposit['Date']).dt.strftime('%B %d, %Y')
      
      # Merge to compare side-by-side
      daily_comparison = daily_payment.merge(daily_deposit, on='Date', how='outer').fillna(0)
      daily_comparison['Gap'] = daily_comparison['Payments Reported'] - daily_comparison['Bank Deposited']
      
      # Format for display
      display_comparison = daily_comparison.copy()
      display_comparison['Payments Reported'] = display_comparison['Payments Reported'].apply(format_money)
      display_comparison['Bank Deposited'] = display_comparison['Bank Deposited'].apply(format_money)
      display_comparison['Gap'] = display_comparison['Gap'].apply(format_money)
      
      st.dataframe(display_comparison, use_container_width=True, hide_index=True)
      st.caption("Daily breakdown: When Uber reported payments vs when they hit your bank")
    else:
      st.dataframe(daily_payment, use_container_width=True, hide_index=True)
  
  st.divider()
  
  # Processing delay analysis
  st.subheader("Payment Processing Delay")
  
  if not audit_df.empty and 'Payment Date' in audit_df.columns and 'Bank Deposit Date' in audit_df.columns:
    # Calculate processing delay (days between payment and deposit)
    audit_df['Processing Days'] = (audit_df['Bank Deposit Date'] - audit_df['Payment Date']).dt.days
    
    # Show distribution
    processing_data = audit_df[(audit_df['Processing Days'].notna()) & (audit_df['Processing Days'] >= 0) & (audit_df['Processing Days'] <= 30)]
    
    if not processing_data.empty:
      fig = px.histogram(processing_data, x='Processing Days', nbins=10,
               title="Payment Processing Delay (Days from Reported to Deposited)",
               color_discrete_sequence=['#FF8C00'],
               height=400)
      fig.update_xaxes(title="Days to Deposit")
      fig.update_yaxes(title="Number of Payments")
      st.plotly_chart(fig, width='stretch')
      
      avg_delay = processing_data['Processing Days'].mean()
      max_delay = processing_data['Processing Days'].max()
      min_delay = processing_data['Processing Days'].min()
      
      col1, col2, col3 = st.columns(3)
      col1.metric("Avg Processing Time", f"{avg_delay:.1f} days")
      col2.metric("Longest Delay", f"{max_delay:.0f} days")
      col3.metric("Fastest Deposit", f"{min_delay:.0f} days")
  
  st.divider()
  
  # Reconciliation status breakdown
  st.subheader(" Reconciliation Status")
  
  if not audit_df.empty and 'Reconciliation Status' in audit_df.columns:
    status_counts = audit_df['Reconciliation Status'].value_counts()
    
    fig = px.pie(
      values=status_counts.values,
      names=status_counts.index,
      title="Payment Reconciliation Status Distribution",
      color_discrete_map={
        'BANK_MATCHED': '#2ca02c',
        'REFUND_TRACKED': '#ff7f0e',
        'OK': '#1f77b4'
      }
    )
    st.plotly_chart(fig, width='stretch')
    
    st.write("**Status Meanings:**")
    st.write("- **BANK_MATCHED**: Payment found in bank deposits")
    st.write("- **REFUND_TRACKED**: Payment includes a refund")
    st.write("- **OK**: Payment recorded but not yet deposited")

# ============================================================================
# PAGE: DISPUTE FORENSICS
# ============================================================================

elif page == "Dispute Forensics":
  st.title("Dispute Forensics")
  st.write("Investigate problem trips, refunds, and issues • Find Trip IDs for Uber disputes")
  
  st.divider()
  
  # Search functionality
  st.subheader(" Find Problem Trips")
  
  col1, col2 = st.columns([2, 1])
  
  with col1:
    search_type = st.selectbox("Filter by:", [
      "All Trips",
      "Refunded",
      "Low Pay (<$3)",
      "Zero Earnings",
      "High Refund Losses",
      "Extreme Low Pay (<$1)",
      "No Tips Received"
    ])
  
  with col2:
    trip_id_search = st.text_input("Or search by Trip ID:", placeholder="paste UUID here")
  
  # Apply filters
  if trip_id_search:
    filtered = tx[tx['Trip UUID'].str.contains(trip_id_search, case=False, na=False)]
  elif search_type == "Refunded":
    filtered = tx[tx['Refund'] != 0]
  elif search_type == "Low Pay (<$3)":
    filtered = tx[tx['Net Earnings'] < 3.00]
  elif search_type == "Zero Earnings":
    filtered = tx[tx['Net Earnings'] == 0]
  elif search_type == "High Refund Losses":
    filtered = tx[tx['Refund'] < -5]
  elif search_type == "Extreme Low Pay (<$1)":
    filtered = tx[tx['Net Earnings'] < 1.00]
  elif search_type == "No Tips Received":
    filtered = tx[tx['Tip'] == 0]
  else:
    filtered = tx
  
  if not filtered.empty:
    st.metric("Trips Found", len(filtered), help=f"Out of {len(tx)} total")
    
    st.divider()
    
    # Summary stats for filtered trips
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Earnings", format_money(filtered['Net Earnings'].sum()))
    col2.metric("Avg Per Trip", format_money(filtered['Net Earnings'].mean()))
    col3.metric("Total Refunded", format_money(filtered['Refund'].sum()))
    col4.metric("Total Tips Lost", format_money(filtered[filtered['Tip'] == 0]['Net Earnings'].sum()))
    
    st.divider()
    
    # Detailed view WITH TRIP ID
    st.subheader(" Full Details (Click Row to Copy Trip ID)")
    
    detail_cols = ['Trip UUID', 'Trip drop off time', 'Restaurant', 'Pickup City', 'Pickup Zip',
           'Trip distance', 'Fare', 'Tip', 'Incentive', 'Boost', 'Refund', 'Net Earnings']
    detail_cols = [c for c in detail_cols if c in filtered.columns]
    
    display_df = filtered[detail_cols].copy()
    display_df['Trip drop off time'] = display_df['Trip drop off time'].dt.strftime('%Y-%m-%d %H:%M')
    display_df['Fare'] = display_df['Fare'].apply(format_money)
    display_df['Tip'] = display_df['Tip'].apply(format_money)
    display_df['Incentive'] = display_df['Incentive'].apply(format_money)
    display_df['Boost'] = display_df['Boost'].apply(format_money)
    display_df['Refund'] = display_df['Refund'].apply(format_money)
    display_df['Net Earnings'] = display_df['Net Earnings'].apply(format_money)
    
    # Reorder columns for readability
    display_df = display_df[['Trip UUID', 'Trip drop off time', 'Restaurant', 'Pickup City', 'Trip distance', 
                'Fare', 'Tip', 'Incentive', 'Boost', 'Refund', 'Net Earnings']]
    
    st.dataframe(display_df, width='stretch', hide_index=True)
    
    st.caption(" Copy the Trip UUID and paste it when contacting Uber support")
    
    st.divider()
    
    # Issue breakdown
    st.subheader(" Issue Breakdown")
    
    issue_counts = {
      "Refunded": len(filtered[filtered['Refund'] != 0]),
      "No Tips": len(filtered[filtered['Tip'] == 0]),
      "Low Pay (<$3)": len(filtered[filtered['Net Earnings'] < 3.00]),
      "Zero Earnings": len(filtered[filtered['Net Earnings'] == 0])
    }
    
    issue_counts = {k: v for k, v in issue_counts.items() if v > 0}
    
    if issue_counts:
      fig = px.pie(
        values=list(issue_counts.values()),
        names=list(issue_counts.keys()),
        title="Issue Distribution"
      )
      st.plotly_chart(fig, width='stretch')
    
    st.divider()
    
    # Export options
    st.subheader(" Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
      # Full details CSV
      st.download_button(
        "Download Full Details (CSV)",
        filtered[['Trip UUID', 'Trip drop off time', 'Pickup address', 'Drop off address', 
             'Trip distance', 'Fare', 'Tip', 'Refund', 'Net Earnings']].to_csv(index=False),
        "disputed_trips_full.csv",
        "text/csv"
      )
    
    with col2:
      # Trip IDs only (for Uber support)
      trip_ids = filtered['Trip UUID'].tolist()
      trip_id_text = '\n'.join(trip_ids)
      st.download_button(
        "Download Trip IDs Only",
        trip_id_text,
        "trip_ids.txt",
        "text/plain"
      )
    
    with col3:
      # Summary stats
      summary = f"""Dispute Summary Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Total Trips: {len(filtered)}
Total Earnings: ${filtered['Net Earnings'].sum():.2f}
Average Per Trip: ${filtered['Net Earnings'].mean():.2f}
Total Refunded: ${filtered['Refund'].sum():.2f}
Trips with No Tips: {len(filtered[filtered['Tip'] == 0])}

--TRIP IDs--
{trip_id_text}
"""
      st.download_button(
        "Download Summary Report",
        summary,
        "dispute_summary.txt",
        "text/plain"
      )
  else:
    st.info("No trips found matching your search. Try a different filter.")

# ============================================================================
# PAGE: TRENDS & FORECAST
# ============================================================================

elif page == "Trends":
  st.title("Trends & Forecast")
  st.write("Long-term patterns, seasonality, and what's changing")
  
  st.divider()
  
  # Monthly earnings trend
  st.subheader("📊 Monthly Earnings Trend")
  
  monthly = tx.groupby('Month').agg({
    'Net Earnings': 'sum',
    'Trip UUID': 'count',
    'Tip': 'sum'
  }).reset_index()
  monthly.columns = ['Month', 'Earnings', 'Trips', 'Total Tips']
  
  # Add human-friendly month labels for display
  monthly['Month Display'] = monthly['Month'].apply(format_month_human)
  
  fig = go.Figure()
  fig.add_trace(go.Bar(
    x=monthly['Month Display'],
    y=monthly['Earnings'],
    name='Earnings',
    marker_color='lightgreen',
    yaxis='y'
  ))
  fig.add_trace(go.Scatter(
    x=monthly['Month Display'],
    y=monthly['Trips'],
    name='Trips',
    marker_color='red',
    yaxis='y2'
  ))
  fig.update_layout(
    title="Monthly Earnings vs Trip Count",
    xaxis_title="Month",
    yaxis=dict(title="Earnings ($)"),
    yaxis2=dict(title="Number of Trips", overlaying='y', side='right'),
    hovermode='x unified',
    height=400
  )
  st.plotly_chart(fig, use_container_width=True)
  
  st.divider()
  
  # Key changes
  st.subheader("📈 What's Changing?")
  
  if len(monthly) >= 2:
    last = monthly.iloc[-1]
    prev = monthly.iloc[-2]
    
    col1, col2, col3 = st.columns(3)
    
    earnings_change = ((last['Earnings'] - prev['Earnings']) / prev['Earnings'] * 100) if prev['Earnings'] > 0 else 0
    trips_change = ((last['Trips'] - prev['Trips']) / prev['Trips'] * 100) if prev['Trips'] > 0 else 0
    tip_change = ((last['Total Tips'] - prev['Total Tips']) / prev['Total Tips'] * 100) if prev['Total Tips'] > 0 else 0
    
    col1.metric(
      f"{format_month_human(last['Month'])} vs {format_month_human(prev['Month'])}",
      format_money(last['Earnings']),
      delta=f"{earnings_change:+.1f}%"
    )
    col2.metric("Trip Count Change", f"{int(last['Trips'])} trips", delta=f"{trips_change:+.1f}%")
    col3.metric("Tips Change", format_money(last['Total Tips']), delta=f"{tip_change:+.1f}%")
  
  st.divider()
  
  # Projection
  st.subheader("🔮 Earnings Projection")
  
  if len(monthly) >= 2:
    # Simple linear regression
    x = np.arange(len(monthly))
    y = monthly['Earnings'].values
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    
    # Project next 3 months
    future_months = np.arange(len(monthly), len(monthly) + 3)
    future_earnings = p(future_months)
    
    last_month_date = pd.to_datetime(monthly.iloc[-1]['Month'] + '-01')
    future_dates = [(last_month_date + pd.DateOffset(months=i+1)).strftime('%Y-%m') for i in range(3)]
    future_dates_human = [format_month_human(d) for d in future_dates]
    
    st.info(f"""
    Based on your trend:
    - **{future_dates_human[0]}**: {format_money(max(0, future_earnings[0]))}
    - **{future_dates_human[1]}**: {format_money(max(0, future_earnings[1]))}
    - **{future_dates_human[2]}**: {format_money(max(0, future_earnings[2]))}
    
    (Linear projection - actual results depend on effort and market)
    """)

# ============================================================================
# PAGE: YEAR-END REPORT
# ============================================================================

elif page == "Year-End Report":
  st.title("Annual Performance Report: Executive Summary")
  st.write("*Comprehensive year-end analysis & transportation business performance review*")
  
  st.divider()
  
  # Calculate annual metrics
  total_annual_earnings = tx['Net Earnings'].sum()
  total_annual_trips = len(tx)
  total_annual_miles = tx['Trip distance'].sum()
  avg_per_mile_annual = total_annual_earnings / total_annual_miles if total_annual_miles > 0 else 0
  avg_per_trip_annual = total_annual_earnings / total_annual_trips if total_annual_trips > 0 else 0
  refund_count_annual = (tx['Refund'] != 0).sum()
  refund_rate_annual = (refund_count_annual / total_annual_trips * 100) if total_annual_trips > 0 else 0
  
  # Get unique cities and restaurants
  unique_cities = tx['Pickup City'].nunique()
  unique_restaurants = tx['Restaurant'].nunique()
  
  # Monthly breakdown
  monthly_data = tx.groupby('Month').agg({
    'Net Earnings': 'sum',
    'Trip UUID': 'count',
    'Trip distance': 'sum'
  }).reset_index()
  monthly_data.columns = ['Month', 'Earnings', 'Trips', 'Miles']
  
  st.markdown("""
  ## 📊 EXECUTIVE OVERVIEW
  
  This year-end analysis evaluates your courier operation's financial performance, operational efficiency, 
  and market positioning across a comprehensive data set spanning multiple months of active delivery service.
  """)
  
  # Key metrics cards
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Annual Earnings", format_money(total_annual_earnings), 
              delta=format_money(monthly_data.iloc[-1]['Earnings'] - monthly_data.iloc[0]['Earnings']) if len(monthly_data) > 1 else None)
  col2.metric("Total Trips", f"{total_annual_trips:,}", delta="trips")
  col3.metric("Total Miles", f"{total_annual_miles:,.0f}", delta="miles")
  col4.metric("Efficiency", format_money(avg_per_mile_annual), delta="$/mile")
  
  st.divider()
  
  st.markdown(f"""
  ## 💼 BUSINESS PERFORMANCE ANALYSIS
  
  ### Financial Performance
  
  Your courier operation generated **{format_money(total_annual_earnings)}** in net earnings across **{total_annual_trips:,}** active trips. 
  This represents a significant volume of delivery work with measurable profitability metrics. 
  The average trip yield was **{format_money(avg_per_trip_annual)}**, while your cost efficiency stood at **{format_money(avg_per_mile_annual)} per mile driven**.
  
  The transportation network analysis reveals operation across **{unique_cities:,}** unique cities and **{unique_restaurants:,}** distinct restaurants, 
  indicating a diversified service portfolio. This geographic and vendor diversification is a strength, as it 
  reduces dependency on any single market or client segment.
  
  ### Operational Efficiency Metrics
  
  **Efficiency Formula:** Your cost efficiency is calculated as:
  
  $$\\eta = \\frac{{\\text{{Total Net Earnings}}}}{{\\text{{Total Miles Driven}}}} = \\frac{{{format_money(total_annual_earnings)}}}{{{total_annual_miles:,.0f} \\text{{ mi}}}} = {format_money(avg_per_mile_annual)}/\\text{{mile}}$$
  
  At **{format_money(avg_per_mile_annual)} per mile**, your operation operates within competitive industry ranges for micro-mobility courier services. 
  Premium operations typically target **$0.80–$1.20 per mile**. To improve this metric:
  
  - Focus on longer-distance orders (reduces relative overhead)
  - Minimize empty miles by batching nearby pickups
  - Prioritize high-tip restaurants during peak hours
  - Reduce time spent waiting at pickup locations
  
  **Trip Frequency:** With **{total_annual_trips:,} trips** across {len(monthly_data)} months of data, your average monthly volume is **{total_annual_trips / len(monthly_data):.0f} trips**. 
  This indicates consistent demand utilization. However, trip volume variance suggests seasonal or demand-driven fluctuations.
  """)
  
  st.divider()
  
  st.markdown("""
  ### Reimbursement Activity
  """)
  
  col1, col2 = st.columns(2)
  
  with col1:
    st.metric("Reimbursement Rate", f"{refund_rate_annual:.2f}%", 
              help="Shop & Pay / Order & Pay trips where you paid and were reimbursed")
    st.caption(f"Total reimbursements: {refund_count_annual}")
  
  with col2:
    direct_pay_rate = 100 - refund_rate_annual
    st.metric("Direct Pay Rate", f"{direct_pay_rate:.2f}%",
              help="Percentage of trips where Uber paid directly")
  
  st.info(f"""
  **Reimbursement Overview:** {refund_rate_annual:.2f}% of your trips involved Shop & Pay or Order & Pay reimbursements. 
  This is a normal part of courier operations - you advance the funds and Uber reimburses when the customer pays. 
  Monitor reimbursement lag times to ensure timely payment processing.
  """)
  
  st.divider()
  
  st.markdown("""
  ### Monthly Performance Trend
  """)
  
  # Monthly earnings chart
  fig_monthly = px.bar(
    monthly_data,
    x='Month',
    y='Earnings',
    title="Monthly Net Earnings Trajectory",
    color='Earnings',
    color_continuous_scale='Viridis',
    height=400
  )
  fig_monthly.update_xaxes(title="Month")
  fig_monthly.update_yaxes(title="Net Earnings ($)")
  st.plotly_chart(fig_monthly, use_container_width=True)
  
  col1, col2 = st.columns(2)
  with col1:
    best_month = monthly_data.loc[monthly_data['Earnings'].idxmax()]
    worst_month = monthly_data.loc[monthly_data['Earnings'].idxmin()]
    st.metric("Best Month", best_month['Month'], 
              delta=format_money(best_month['Earnings']))
    st.caption(f"{best_month['Trips']:.0f} trips, {best_month['Miles']:.0f} miles")
  
  with col2:
    st.metric("Lowest Month", worst_month['Month'],
              delta=format_money(worst_month['Earnings']),
              delta_color="inverse")
    st.caption(f"{worst_month['Trips']:.0f} trips, {worst_month['Miles']:.0f} miles")
  
  st.divider()
  
  st.markdown("""
  ### Geographic Market Penetration
  
  Your operation spans multiple metropolitan areas within your service region. Market concentration analysis 
  is essential for business sustainability:
  """)
  
  # Top cities analysis
  city_annual = tx.groupby('Pickup City').agg({
    'Net Earnings': 'sum',
    'Trip UUID': 'count'
  }).reset_index()
  city_annual.columns = ['City', 'Earnings', 'Trips']
  city_annual['Share %'] = (city_annual['Earnings'] / city_annual['Earnings'].sum() * 100).round(1)
  city_annual = city_annual.sort_values('Earnings', ascending=False).head(8)
  
  top_3_concentration = city_annual.head(3)['Share %'].sum()
  
  fig_cities = px.pie(
    city_annual,
    values='Earnings',
    names='City',
    title=f"Earnings Distribution by City (Top {len(city_annual)})",
    height=450
  )
  st.plotly_chart(fig_cities, use_container_width=True)
  
  st.markdown(f"""
  **Market Concentration Analysis:**
  - Your top 3 cities account for **{top_3_concentration:.1f}%** of total earnings
  - Geographic diversification: **{unique_cities} unique cities served**
  - Recommendation: {'Diversify into underperforming cities' if top_3_concentration > 70 else 'Current geographic mix is well-balanced'}
  """)
  
  st.divider()
  
  st.markdown("""
  ### Restaurant Partner Performance
  
  Vendor selection significantly impacts earnings consistency and quality:
  """)
  
  # Top restaurants
  rest_annual = tx.groupby('Restaurant').agg({
    'Net Earnings': 'sum',
    'Trip UUID': 'count'
  }).reset_index()
  rest_annual.columns = ['Restaurant', 'Earnings', 'Trips']
  rest_annual = rest_annual.sort_values('Earnings', ascending=False).head(8)
  
  fig_restaurants = px.bar(
    rest_annual,
    x='Restaurant',
    y='Earnings',
    color='Trips',
    title="Top Restaurants by Annual Revenue",
    height=400,
    color_continuous_scale='Spectral'
  )
  fig_restaurants.update_xaxes(tickangle=-45)
  st.plotly_chart(fig_restaurants, use_container_width=True)
  
  st.divider()
  
  st.markdown(f"""
  ## 📈 STRATEGIC RECOMMENDATIONS
  
  Based on comprehensive analysis of {total_annual_trips:,} trips across {len(monthly_data)} months:
  
  **1. REVENUE OPTIMIZATION**
  
  Target efficiency growth:
  $$\\eta_{{\\text{{target}}}} = \\eta_{{\\text{{current}}}} \\times 1.20 = {format_money(avg_per_mile_annual)} \\times 1.20 = {format_money(avg_per_mile_annual * 1.20)}/\\text{{mile}}$$
  
  - Focus on high-tip restaurant partnerships
  - Shift work hours toward peak demand windows
  
  **2. OPERATIONAL SCALING**
  - Monthly volume is {total_annual_trips / len(monthly_data):.0f} trips—sustainable growth target is +20–30%
  - Expand to underutilized cities for geographic load balancing
  - Implement route optimization to reduce empty miles
  
  **3. REIMBURSEMENT MANAGEMENT**
  - Monitor Shop & Pay / Order & Pay reimbursement lag times
  - Prioritize higher-margin direct-pay trips when available
  - Track which restaurants have faster reimbursement processing
  
  **4. FINANCIAL PLANNING**
  - Annual earnings: {format_money(total_annual_earnings)}
  - Projected monthly average: {format_money(total_annual_earnings / len(monthly_data))}
  - Reserve 15–20% for vehicle maintenance, insurance, fuel fluctuations
  
  **5. COMPETITIVE POSITIONING**
  - Benchmark against industry standards: $0.80–$1.20/mile for experienced couriers
  - Your current position: {'Below' if avg_per_mile_annual < 0.80 else 'At' if avg_per_mile_annual < 1.20 else 'Above'} industry average
  - Path to premium tier: Focus on quality, reliability, and geographic coverage
  """)
  
  st.divider()
  
  st.markdown(f"""
  ## 🎯 CONCLUSION
  
  This year demonstrates a **operationally sound and financially viable** courier business. 
  With {total_annual_trips:,} trips and {format_money(total_annual_earnings)} in earnings, 
  you've established a sustainable delivery operation with clear growth opportunities.
  
  **Primary Focus for Next Year:**
  
  $$\\begin{{align}}
  \\text{{1. Efficiency}} & : {format_money(avg_per_mile_annual)}/\\text{{mi}} \\rightarrow {format_money(avg_per_mile_annual * 1.20)}/\\text{{mi}} \\\\
  \\text{{2. Monthly Volume}} & : {total_annual_trips / len(monthly_data):.0f} \\rightarrow {total_annual_trips / len(monthly_data) * 1.25:.0f} \\text{{ trips}} \\\\
  \\text{{3. Monitor}} & : \\text{{Shop \\& Pay lag times}}
  \\end{{align}}$$
  
  *Report Generated: Year-End {pd.Timestamp.now().year} | Data Period: {format_month_human(monthly_data.iloc[0]['Month'])} – {format_month_human(monthly_data.iloc[-1]['Month'])}*
  """)

st.divider()
st.caption("Courier Insights • Purpose-built for courier optimization • Last updated: today")