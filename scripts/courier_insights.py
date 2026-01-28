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
    border-bottom: 3px solid #1e5a96;
    padding-bottom: 12px;
    margin-bottom: 20px;
    font-weight: 700;
    font-size: 28px !important;
  }
  
  h2 {
    color: #000000 !important;
    margin-top: 32px;
    margin-bottom: 16px;
    font-weight: 700;
    font-size: 22px !important;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 8px;
  }
  
  h3 {
    color: #000000 !important;
    margin-top: 20px;
    margin-bottom: 12px;
    font-weight: 600;
    font-size: 18px !important;
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
    line-height: 1.6;
  }
  
  .stMarkdown p {
    color: #000000 !important;
    font-size: 15px;
    margin-bottom: 12px;
  }
  
  .stMarkdown strong {
    color: #000000 !important;
    font-weight: 600;
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
    /* Hide UI elements */
    .stSidebar {
      display: none !important;
    }
    .stAppHeader {
      display: none !important;
    }
    .stToolbar {
      display: none !important;
    }
    [data-testid="stToolbar"] {
      display: none !important;
    }
    button {
      display: none !important;
    }
    
    /* Page setup */
    @page {
      size: letter;
      margin: 0.75in;
    }
    
    main {
      padding: 0 !important;
      max-width: 100% !important;
    }
    
    /* Typography for print */
    body {
      background: white !important;
      color: #000 !important;
      font-size: 10pt !important;
    }
    
    .stMarkdown h1 {
      page-break-after: avoid;
      page-break-before: auto;
      margin-top: 0;
      border: none;
      padding-bottom: 8px;
      font-size: 18pt !important;
    }
    
    .stMarkdown h2 {
      page-break-after: avoid;
      page-break-before: auto;
      margin-top: 16px;
      font-size: 14pt !important;
    }
    
    .stMarkdown h3 {
      page-break-after: avoid;
      font-size: 12pt !important;
    }
    
    /* Prevent awkward breaks */
    .stDataFrame, [data-testid="stDataFrame"] {
      page-break-inside: avoid;
      page-break-after: auto;
      margin: 8px 0;
      max-height: 9in;
      overflow: visible !important;
    }
    
    .plotly-container, .js-plotly-plot {
      page-break-inside: avoid;
      page-break-after: auto;
      max-height: 8in;
    }
    
    .stMetric, [data-testid="stMetric"] {
      page-break-inside: avoid;
      display: inline-block;
      width: auto;
      margin: 4px 8px;
    }
    
    /* Column layouts */
    .stColumns, [data-testid="column"] {
      page-break-inside: avoid;
    }
    
    /* Dividers */
    hr {
      page-break-after: avoid;
      margin: 8px 0;
    }
    
    /* Tables - constrain width */
    .dataframe {
      font-size: 9pt !important;
      max-width: 100% !important;
      overflow: hidden !important;
    }
    
    .dataframe th, .dataframe td {
      padding: 4px 6px !important;
      font-size: 9pt !important;
    }
    
    /* Force page breaks between major sections */
    .stMarkdown:has(h1) {
      page-break-before: always;
    }
    
    .stMarkdown:has(h1):first-child {
      page-break-before: avoid;
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

def load_geocoded_addresses():
  """Load pre-geocoded addresses from CSV (generated by pre_geocode_addresses.py)"""
  geocode_file = Path('data/geocoded_addresses.csv')
  if geocode_file.exists():
    return pd.read_csv(geocode_file)
  return pd.DataFrame(columns=['address', 'latitude', 'longitude'])

def get_coordinates_for_addresses(addresses_list):
  """Get lat/lon for addresses from pre-geocoded CSV - instant lookup"""
  geocoded = load_geocoded_addresses()
  geocoded_dict = dict(zip(geocoded['address'], zip(geocoded['latitude'], geocoded['longitude'])))
  
  results = {}
  for addr in addresses_list:
    if pd.isna(addr):
      results[addr] = (None, None)
    else:
      results[addr] = geocoded_dict.get(addr, (None, None))
  
  return results

# ============================================================================
# LOAD ALL DATA
# ============================================================================

def load_data():
  """Load and prepare all data for analysis"""
  # Load raw data - only load what's needed
  try:
    transactions = safe_read('reports/monthly_comprehensive/all_transactions_detailed.csv')
    audit = safe_read('reports/audit_trail/complete_audit_trail.csv')
    refunds = safe_read('reports/four_way_reconciliation/refund_verification_status.csv')
    multi_account = safe_read('reports/four_way_reconciliation/multi_account_reconciliation.csv')
    daily = safe_read('reports/four_way_reconciliation/daily_reconciliation_3way.csv')
  except Exception as e:
    st.error(f"Error loading CSV files: {e}")
    return None
  
  if transactions.empty:
    st.error("No transaction data found. Please check that all_transactions_detailed.csv has data.")
    return None
  
  # Parse dates
  transactions['Trip drop off time'] = pd.to_datetime(transactions['Trip drop off time'], errors='coerce')
  if not audit.empty and 'Bank Deposit Date' in audit.columns:
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
  
  # Normalize text fields (optimized - only key columns)
  text_cols = ['Pickup City', 'Dropoff City', 'Restaurant']
  for col in text_cols:
    if col in transactions.columns:
      transactions[col] = transactions[col].astype(str).str.strip().str.title()
  
  # Rebuild area strings with normalized data
  transactions['Pickup Area'] = transactions['Pickup City'] + ' ' + transactions['Pickup Zip']
  transactions['Dropoff Area'] = transactions['Dropoff City'] + ' ' + transactions['Dropoff Zip']
  
  return {
    'transactions': transactions,
    'audit': audit,
    'refunds': refunds,
    'multi_account': multi_account,
    'daily': daily
  }

# ============================================================================
# LAZY DATA LOADING HELPER
# ============================================================================

def get_data():
  """Lazy data loader - only loads when called, caches in session state"""
  if 'data_cache' not in st.session_state:
    st.session_state.data_cache = load_data()
  return st.session_state.data_cache

# ============================================================================
# SIDEBAR NAVIGATION & PERSISTENT HEADER
# ============================================================================

with st.sidebar:
  # Display JTech Logo
  st.markdown('<div class="logo-container">', unsafe_allow_html=True)
  st.image("JTechLogistics_Logo.svg")
  st.markdown('</div>', unsafe_allow_html=True)
  
  # Navigation
  st.markdown('<span class="nav-label">Navigation</span>', unsafe_allow_html=True)
  
  # Create a session state variable to track the selected page
  if 'current_page' not in st.session_state:
    st.session_state.current_page = "Overview"

  # Navigation items with descriptions
  nav_items = [
    {"label": "Dashboard", "page": "Overview", "desc": "Key metrics"},
    {"label": "Pickup Hotspots", "page": "Routes", "desc": "Restaurant density"},
    {"label": "Earnings Map", "page": "Locations", "desc": "Top zones"},
    {"label": "Best Times", "page": "Schedule", "desc": "Peak hours"},
    {"label": "Payment Tracking", "page": "Payments", "desc": "Reconciliation"},
    {"label": "Performance", "page": "Issues", "desc": "Efficiency"},
    {"label": "Profit Analysis", "page": "P&L", "desc": "Income vs cost"},
    {"label": "Trends", "page": "Trends", "desc": "Patterns"},
    {"label": "Year-End Report", "page": "Year-End Report", "desc": "Annual summary"}
  ]

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

  page = st.session_state.current_page

# ============================================================================
# PAGE: OVERVIEW (Home)
# ============================================================================

if page == "Overview":
  st.title("Overview")
  st.write("Your quick pulse: recent earnings, trends, and top spots")
  
  try:
    # Show loading indicator if data not cached
    if 'data_cache' not in st.session_state:
      with st.spinner("⏳ Loading courier data (first time only)... Please wait..."):
        data = get_data()
    else:
      data = get_data()
    
    if data is None:
      st.error("Could not load transaction data. Please ensure reports are generated.")
      st.stop()
    
    tx = data['transactions']
  except Exception as e:
    st.error(f"Error loading data: {e}")
    import traceback
    st.code(traceback.format_exc())
    st.stop()
  
  st.divider()
  
  # Period selector (based on available months in data)
  month_list = sorted(tx['Month'].unique().tolist()) if 'Month' in tx.columns else []
  period = st.radio(
    "Recent Period",
    ["Last 3 months", "Last 1 month", "Last 6 months", "All"],
    horizontal=True,
    index=0
  )
  if period == "All" or not month_list:
    recent_tx = tx
    recent_months = month_list
  else:
    take_n = 3 if period == "Last 3 months" else (1 if period == "Last 1 month" else 6)
    recent_months = month_list[-take_n:]
    recent_tx = tx[tx['Month'].isin(recent_months)]
  
  # Clarify what "Recent" means
  try:
    if recent_months and len(recent_months) > 0:
      months_human = [format_month_human(m) for m in recent_months]
      if len(months_human) == 1:
        period_desc = months_human[0]
      else:
        period_desc = f"{months_human[0]} – {months_human[-1]} ({len(months_human)} months)"
    else:
      period_desc = "All data"
    st.caption(f"Recent period: {period_desc}")
  except Exception:
    st.caption("Recent period: All data")
  
  # KPIs
  k1, k2, k3, k4, k5 = st.columns(5)
  total_e = recent_tx['Net Earnings'].sum()
  trips = len(recent_tx)
  avg_trip = (total_e / trips) if trips > 0 else 0
  total_miles = recent_tx['Trip distance'].sum() if 'Trip distance' in recent_tx.columns else float('nan')
  avg_per_mile = (total_e / total_miles) if pd.notna(total_miles) and total_miles > 0 else float('nan')
  
  k1.metric("Total Earnings", format_money(total_e))
  k2.metric("Trips", f"{trips}")
  k3.metric("Avg per Trip", format_money(avg_trip))
  k4.metric("Miles", f"{total_miles:.0f}" if pd.notna(total_miles) else "—")
  k5.metric("Avg/Mile", format_money(avg_per_mile) if pd.notna(avg_per_mile) else "—")
  
  # Tip rate (robust to missing Fare/Tip)
  if {'Tip', 'Fare'}.issubset(recent_tx.columns):
    base_series = recent_tx['Fare'].where(recent_tx['Fare'] > 0, recent_tx['Net Earnings'])
    tip_rate = (recent_tx['Tip'].sum() / base_series.sum()) if base_series.sum() > 0 else 0
    st.caption(f"Tip rate: {(tip_rate * 100):.1f}% over selected period")
  else:
    st.caption("Tip rate: —")
  
  # Earnings trend by month
  if 'Month' in recent_tx.columns and not recent_tx.empty:
    st.subheader("Earnings Trend (by month)")
    trend_df = recent_tx.groupby('Month', as_index=False)['Net Earnings'].sum()
    trend_df = trend_df.sort_values('Month')
    fig_trend = px.bar(trend_df, x='Month', y='Net Earnings', title='Monthly Earnings', labels={'Net Earnings': 'Earnings ($)'})
    fig_trend.update_layout(margin=dict(l=40, r=20, t=50, b=40), height=300)
    st.plotly_chart(fig_trend, use_container_width=True)
  
  st.divider()
  
  # Top cities and restaurants
  st.subheader("Top Spots")
  c1, c2 = st.columns(2)
  with c1:
    st.caption("Top Cities by Total Earnings")
    if 'Pickup City' in recent_tx.columns and not recent_tx.empty:
      city_tbl = recent_tx.groupby('Pickup City').agg({'Net Earnings': 'sum', 'Trip UUID': 'count'}).reset_index()
      city_tbl = city_tbl.sort_values('Net Earnings', ascending=False).head(5)
      city_tbl['Net Earnings'] = city_tbl['Net Earnings'].apply(format_money)
      city_tbl.rename(columns={'Trip UUID': 'Trips'}, inplace=True)
      st.dataframe(city_tbl, width=500)
    else:
      st.caption("—")
  with c2:
    st.caption("Top Restaurants by Avg Earnings (min 10 trips)")
    if 'Restaurant' in recent_tx.columns and not recent_tx.empty:
      rest_tbl = recent_tx.groupby('Restaurant').agg({'Net Earnings': ['mean', 'sum', 'count']}).reset_index()
      rest_tbl.columns = ['Restaurant', 'Avg', 'Total', 'Trips']
      rest_tbl = rest_tbl[rest_tbl['Trips'] >= 10].sort_values('Avg', ascending=False).head(5)
      rest_tbl['Avg'] = rest_tbl['Avg'].apply(format_money)
      rest_tbl['Total'] = rest_tbl['Total'].apply(format_money)
      st.dataframe(rest_tbl[['Restaurant', 'Avg', 'Trips']], width=500)
    else:
      st.caption("—")
  
  st.divider()
  
  # Quick navigation
  st.subheader("Quick Actions")
  a1, a2, a3 = st.columns(3)
  with a1:
    if st.button("Go to Payments"):
      try:
        st.query_params = {"page": "Payments"}
        st.rerun()
      except Exception:
        pass
  with a2:
    if st.button("Go to Locations"):
      try:
        st.query_params = {"page": "Locations"}
        st.rerun()
      except Exception:
        pass
  with a3:
    if st.button("Open Processing Delay"):
      try:
        st.query_params = {"page": "Payments"}
        st.rerun()
      except Exception:
        pass
  
  st.divider()
  
  # (Removed) Best Cities by Tip Rate map
  # This section was removed to simplify the overview and avoid confusing maps.
  st.divider()
  
  # CHART VIEW: Best Restaurants by Earnings and Quality
  st.subheader("Best Restaurants by Earnings & Quality")
  
  st.markdown(r"""
  **Quality Metrics:** We measure restaurant performance using two key indicators:
  
  - **Average Per Trip:** $\bar{x}_{\text{trip}} = \frac{\text{Total Earnings}}{\text{Trip Count}}$
  - **Quality Score:** $Q = 100\% - \text{Reimbursement Rate}\%$ (higher is better)
  
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

  # Filter for restaurants with 10+ trips and sort by total earnings
  top_restaurants = rest_stats[rest_stats['Trip Count'] >= 10].nlargest(15, 'Net Earnings')

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
    st.plotly_chart(fig_restaurants, width=1000, key="restaurants_chart")
    
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
# PAGE: P&L (Profit & Loss)
# ============================================================================

if page == "P&L":
  # Load data
  data = get_data()
  if data is None:
    st.error("Could not load transaction data. Please ensure reports are generated.")
    st.stop()
  tx = data['transactions']
  
  st.title("Profit & Loss")
  st.write("Estimate profit by combining earnings with mileage and fees.")
  st.divider()

  # Period selector
  month_list = sorted(tx['Month'].unique().tolist()) if 'Month' in tx.columns else []
  period = st.radio(
    "Period",
    ["Last 3 months", "Last 6 months", "Last 12 months", "All"],
    horizontal=True,
    index=0
  )
  if period == "All" or not month_list:
    pl_tx = tx
    sel_months = month_list
  else:
    take_n = 3 if period == "Last 3 months" else (6 if period == "Last 6 months" else 12)
    sel_months = month_list[-take_n:]
    pl_tx = tx[tx['Month'].isin(sel_months)]

  # Fixed parameters
  cost_per_mile = 0.20
  include_instant_pay = True
  include_adjustments = True

  # Revenue components (handle missing columns)
  revenue_total = pl_tx['Net Earnings'].sum() if 'Net Earnings' in pl_tx.columns else 0.0
  fare_total = pl_tx['Fare'].sum() if 'Fare' in pl_tx.columns else float('nan')
  tip_total = pl_tx['Tip'].sum() if 'Tip' in pl_tx.columns else float('nan')
  refund_total = pl_tx['Refund'].sum() if include_adjustments and 'Refund' in pl_tx.columns else float('nan')
  incentive_total = pl_tx['Incentive'].sum() if 'Incentive' in pl_tx.columns else float('nan')
  boost_total = pl_tx['Boost'].sum() if 'Boost' in pl_tx.columns else float('nan')

  # Expenses
  miles = pl_tx['Trip distance'].sum() if 'Trip distance' in pl_tx.columns else 0.0
  mileage_cost = cost_per_mile * miles
  instant_pay_fee = pl_tx['Instant Pay Fee'].sum() if include_instant_pay and 'Instant Pay Fee' in pl_tx.columns else 0.0
  expenses_total = mileage_cost + instant_pay_fee

  # Profit
  est_profit = revenue_total - expenses_total

  # KPIs
  k1, k2, k3, k4 = st.columns(4)
  k1.metric("Revenue", format_money(revenue_total))
  k2.metric("Expenses", format_money(expenses_total))
  k3.metric("Estimated Profit", format_money(est_profit))
  k4.metric("Miles", f"{miles:,.0f}")

  # Promotions diagnostic (Incentive/Boost presence)
  inc_entries = int((pl_tx['Incentive'] > 0).sum()) if 'Incentive' in pl_tx.columns else 0
  boost_entries = int((pl_tx['Boost'] > 0).sum()) if 'Boost' in pl_tx.columns else 0
  inc_total = pl_tx['Incentive'].sum() if 'Incentive' in pl_tx.columns else float('nan')
  boost_total = pl_tx['Boost'].sum() if 'Boost' in pl_tx.columns else float('nan')
  if inc_entries == 0 and boost_entries == 0:
    st.caption("Promotions: No Incentive or Boost entries found in the selected period.")
  else:
    inc_txt = format_money(inc_total) if pd.notna(inc_total) else '—'
    boost_txt = format_money(boost_total) if pd.notna(boost_total) else '—'
    st.caption(f"Promotions: Incentives {inc_txt} ({inc_entries} entries), Boost {boost_txt} ({boost_entries} entries)")

  # Breakdown table by month
  if 'Month' in pl_tx.columns and not pl_tx.empty:
    st.subheader("Monthly Breakdown")
    cols = {
      'Revenue': lambda df: df['Net Earnings'].sum() if 'Net Earnings' in df.columns else 0.0,
      'Miles': lambda df: df['Trip distance'].sum() if 'Trip distance' in df.columns else 0.0,
      'Instant Pay Fee': lambda df: df['Instant Pay Fee'].sum() if include_instant_pay and 'Instant Pay Fee' in df.columns else 0.0,
      'Fare': lambda df: df['Fare'].sum() if 'Fare' in df.columns else float('nan'),
      'Tip': lambda df: df['Tip'].sum() if 'Tip' in df.columns else float('nan'),
      'Refunds': lambda df: df['Refund'].sum() if include_adjustments and 'Refund' in df.columns else float('nan'),
      'Incentive': lambda df: df['Incentive'].sum() if 'Incentive' in df.columns else float('nan'),
      'Boost': lambda df: df['Boost'].sum() if 'Boost' in df.columns else float('nan')
    }
    mb = []
    for m, mdf in pl_tx.groupby('Month'):
      row = {'Month': m}
      for k, fn in cols.items():
        try:
          row[k] = fn(mdf)
        except Exception:
          row[k] = float('nan')
      row['Mileage Cost'] = cost_per_mile * (row.get('Miles') or 0.0)
      row['Expenses'] = (row['Mileage Cost'] + (row.get('Instant Pay Fee') or 0.0))
      row['Profit'] = (row.get('Revenue') or 0.0) - row['Expenses']
      mb.append(row)
    mb_df = pd.DataFrame(mb).sort_values('Month')
    display_df = mb_df.copy()
    money_cols = ['Revenue','Instant Pay Fee','Fare','Tip','Refunds','Incentive','Boost','Mileage Cost','Expenses','Profit']
    for c in money_cols:
      if c in display_df.columns:
        display_df[c] = display_df[c].apply(lambda x: format_money(x) if pd.notna(x) else '—')
    st.dataframe(display_df, use_container_width=True)

    # Export
    csv_bytes = mb_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download P&L CSV", data=csv_bytes, file_name="monthly_pnl.csv", mime="text/csv")

  st.caption(f"Note: Profit estimated at ${cost_per_mile}/mi mileage cost and all fees included.")

  st.divider()
  
  # Daily Income vs Personal Spending (excludes reimbursements)
  st.subheader("Daily Income vs Personal Spending")
  st.caption("Spending includes Instant Pay fees and optional uploaded personal expenses; reimbursements are excluded.")
  
  # Optional personal expenses upload (Date, Amount[, Description])
  exp_file = st.file_uploader("Add Personal Expenses CSV (Date, Amount[, Description])", type=["csv"], key="pnl_exp_upload")
  personal_exp = None
  if exp_file is not None:
    try:
      personal_exp = pd.read_csv(exp_file)
      if 'Date' in personal_exp.columns:
        personal_exp['Date'] = pd.to_datetime(personal_exp['Date'], errors='coerce').dt.date
      if 'Amount' in personal_exp.columns:
        personal_exp['Amount'] = pd.to_numeric(personal_exp['Amount'], errors='coerce')
      personal_exp = personal_exp.dropna(subset=['Date', 'Amount'])
    except Exception:
      st.warning("Could not parse expenses file; please ensure it has Date and Amount columns.")
      personal_exp = None

  # Build daily frame from trips
  if 'Trip drop off time' in pl_tx.columns and not pl_tx.empty:
    pl_tx['Trip drop off time'] = pd.to_datetime(pl_tx['Trip drop off time'], errors='coerce')
    daily = pl_tx.dropna(subset=['Trip drop off time']).copy()
    daily['Date'] = daily['Trip drop off time'].dt.date
    daily_agg = daily.groupby('Date').agg({
      'Net Earnings': 'sum',
      'Trip distance': 'sum',
      'Instant Pay Fee': 'sum' if include_instant_pay and 'Instant Pay Fee' in daily.columns else 'sum'
    }).reset_index()
    # Handle missing columns gracefully
    if 'Instant Pay Fee' not in daily.columns or not include_instant_pay:
      daily_agg['Instant Pay Fee'] = 0.0
    if 'Trip distance' not in daily.columns:
      daily_agg['Trip distance'] = 0.0
    # Compute costs and profit
    daily_agg['Mileage Cost'] = daily_agg['Trip distance'] * cost_per_mile
    daily_agg['Spending'] = daily_agg['Instant Pay Fee'] + daily_agg['Mileage Cost']
    # Merge personal expenses
    if personal_exp is not None and not personal_exp.empty:
      exp_by_day = personal_exp.groupby('Date')['Amount'].sum().reset_index().rename(columns={'Amount': 'Personal Expenses'})
      daily_agg = daily_agg.merge(exp_by_day, on='Date', how='left')
      daily_agg['Personal Expenses'] = daily_agg['Personal Expenses'].fillna(0.0)
      daily_agg['Spending'] = daily_agg['Spending'] + daily_agg['Personal Expenses']
    else:
      daily_agg['Personal Expenses'] = 0.0
    daily_agg['Income'] = daily_agg['Net Earnings']
    daily_agg['Profit'] = daily_agg['Income'] - daily_agg['Spending']

    # Display
    disp = daily_agg.copy()
    for col in ['Income','Spending','Profit','Instant Pay Fee','Mileage Cost','Personal Expenses']:
      if col in disp.columns:
        disp[col] = disp[col].apply(lambda x: format_money(x))
    if 'Trip distance' in disp.columns:
      disp['Trip distance'] = disp['Trip distance'].apply(lambda x: f"{x:.1f}mi")
    st.dataframe(disp.sort_values('Date'), use_container_width=True)
  else:
    st.info("No trip drop-off times available to build daily view.")

# PAGE: LOCATION INTELLIGENCE
# ============================================================================

elif page == "Locations":
  # Load data
  data = get_data()
  if data is None:
    st.error("Could not load transaction data. Please ensure reports are generated.")
    st.stop()
  tx = data['transactions']
  
  st.title("Location Intelligence")
  st.write("Which cities, restaurants, and areas pay best?")
  
  st.markdown(r"""
  **Earnings by Location Formula:**
  
  $$\text{Location Quality} = \text{Avg Earnings per Trip} \times \frac{\text{Trip Count}}{\text{Total Trips}}$$
  
  Locations with high average earnings AND good volume are your "sweet spots"—prioritize them!
  """)
  
  st.divider()
  
  # SWEET SPOTS SECTION
  st.subheader("Your Sweet Spots (Best Pay + Volume)")
  
  # Calculate location quality scores
  total_trips = len(tx)
  city_quality = tx.groupby('Pickup City').agg({
    'Net Earnings': ['sum', 'mean', 'count'],
    'Tip': 'mean'
  }).reset_index()
  city_quality.columns = ['City', 'Total Earnings', 'Avg Earnings', 'Trip Count', 'Avg Tip']
  city_quality['Location Quality'] = city_quality['Avg Earnings'] * (city_quality['Trip Count'] / total_trips)
  city_quality = city_quality.sort_values('Location Quality', ascending=False)
  
  # Display top 5 sweet spots
  col1, col2, col3, col4, col5 = st.columns(5)
  
  for idx, (_, row) in enumerate(city_quality.head(5).iterrows()):
    with [col1, col2, col3, col4, col5][idx]:
      quality_score = row['Location Quality']
      st.metric(
        row['City'],
        f"{quality_score:.2f}",
        f"${row['Avg Earnings']:.2f}/trip • {int(row['Trip Count'])} trips"
      )
  
  # Detailed sweet spots table
  st.markdown("**Top Sweet Spots by Quality Score:**")
  sweet_spots_display = city_quality.head(8).copy()
  sweet_spots_display['Total Earnings'] = sweet_spots_display['Total Earnings'].apply(format_money)
  sweet_spots_display['Avg Earnings'] = sweet_spots_display['Avg Earnings'].apply(format_money)
  sweet_spots_display['Avg Tip'] = sweet_spots_display['Avg Tip'].apply(format_money)
  sweet_spots_display['Location Quality'] = sweet_spots_display['Location Quality'].round(3)
  sweet_spots_display['Trip Count'] = sweet_spots_display['Trip Count'].astype(int)
  sweet_spots_display = sweet_spots_display[['City', 'Location Quality', 'Avg Earnings', 'Trip Count', 'Avg Tip', 'Total Earnings']]
  
  st.dataframe(sweet_spots_display, width=1000, hide_index=True)
  
  st.info("""
  💡 **How to use Sweet Spots:**
  - **Higher Quality Score** = Better combination of pay + frequency
  - **Focus your efforts** on these cities - they offer best ROI
  - **During peak hours**, these areas will be most productive
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
  
  # Region focus selector
  region = st.radio(
    "Region",
    ["Dallas Metro", "All"],
    horizontal=True
  )

  # Map view selector
  map_view = st.radio(
    "Map View",
    ["City Aggregation", "Heatmap Performance", "Individual Trips"],
    horizontal=True
  )

  # Dallas metro city filter
  dallas_metro_cities = {
    'Dallas', 'Richardson', 'Garland', 'Mesquite', 'Irving', 'Carrollton',
    'Plano', 'Allen', 'Frisco', 'McKinney', 'Balch Springs', 'Seagoville', 'Forney'
  }
  dallas_center = (32.7767, -96.7970)
  tx_region = tx[tx['Pickup City'].isin(dallas_metro_cities)] if region == "Dallas Metro" else tx
  
  if map_view == "City Aggregation":
    # Aggregate by city with quality scores
    city_agg = tx_region.groupby('Pickup City').agg({
      'Net Earnings': ['sum', 'mean', 'count'],
      'Tip': 'mean'
    }).reset_index()
    city_agg.columns = ['City', 'Total Earnings', 'Avg Earnings', 'Trip Count', 'Avg Tip']
    
    # Calculate location quality score
    city_agg['Location Quality'] = city_agg['Avg Earnings'] * (city_agg['Trip Count'] / total_trips)
    city_agg['Quality Rank'] = city_agg['Location Quality'].rank(ascending=False)
    
    # Sort by quality and take top 10
    city_agg_top = city_agg.nlargest(10, 'Location Quality').sort_values('Location Quality', ascending=True)
    
    # Horizontal bar chart instead of map
    fig = px.bar(
      city_agg_top,
      x='Location Quality',
      y='City',
      orientation='h',
      color='Avg Earnings',
      color_continuous_scale='Viridis',
      hover_data={'Total Earnings': ':$,.0f', 'Avg Earnings': ':$,.2f', 'Trip Count': True},
      title='Top 10 Cities by Location Quality Score',
      labels={'Location Quality': 'Quality Score', 'City': 'City'},
      height=450
    )
    fig.update_layout(
      margin=dict(l=150, r=40, t=50, b=40),
      coloraxis_colorbar=dict(title="Avg Earnings ($)")
    )
    st.plotly_chart(fig, width=1000)
  
  elif map_view == "Heatmap Performance":
    # Heatmap controls: style, intensity, metric
    hc1, hc2, hc3 = st.columns(3)
    with hc1:
      palette = st.selectbox("Palette", ["Blues (soft)", "Cividis (neutral)", "Viridis (contrast)", "YlOrRd (warm)", "Turbo (original)"])
      palette_map = {
        "Blues (soft)": "Blues",
        "Cividis (neutral)": "Cividis",
        "Viridis (contrast)": "Viridis",
        "YlOrRd (warm)": "YlOrRd",
        "Turbo (original)": "Turbo"
      }
      palette_val = palette_map.get(palette, "Blues")
    with hc2:
      radius = st.slider("Intensity (radius)", min_value=10, max_value=60, value=25, step=5)
    with hc3:
      opacity = st.slider("Opacity", min_value=0.3, max_value=1.0, value=0.7, step=0.1)

    metric = st.selectbox("Heatmap Metric", ["Avg Earnings per Trip", "Trip Count", "Total Earnings"], index=0)

    # Create heatmap data from city aggregates
    heat_data = []
    city_iter = dallas_metro_cities if region == "Dallas Metro" else city_coords.keys()
    for city in city_iter:
      coords = city_coords.get(city)
      if not coords:
        continue
      city_df = tx_region[tx_region['Pickup City'] == city]
      if city_df.empty:
        continue
      if metric == "Avg Earnings per Trip":
        value = city_df['Net Earnings'].mean()
      elif metric == "Trip Count":
        value = len(city_df)
      else:
        value = city_df['Net Earnings'].sum()
      if pd.notna(value) and value > 0:
        heat_data.append({
          'lat': coords[0],
          'lon': coords[1],
          'value': value
        })
    
    if heat_data:
      heatmap_df = pd.DataFrame(heat_data)
      fig = px.density_mapbox(
        heatmap_df,
        lat='lat',
        lon='lon',
        z='value',
        radius=radius,
        mapbox_style='carto-positron',
        height=500,
        color_continuous_scale=palette_val,
        title=f"Heatmap ({metric})"
      )
      fig.update_traces(opacity=opacity)
      # Auto-zoom with Dallas-focused default
      center_lat, center_lon = dallas_center if region == "Dallas Metro" else (32.9, -96.8)
      if len(heatmap_df) > 0:
        lat_range = heatmap_df['lat'].max() - heatmap_df['lat'].min()
        lon_range = heatmap_df['lon'].max() - heatmap_df['lon'].min()
        center_lat = (heatmap_df['lat'].max() + heatmap_df['lat'].min()) / 2
        center_lon = (heatmap_df['lon'].max() + heatmap_df['lon'].min()) / 2
        max_range = max(lat_range, lon_range) if max(lat_range, lon_range) > 0 else 1
        if region == "Dallas Metro":
          # Clamp zoom to show Dallas area clearly
          if max_range < 0.2:
            zoom = 12
          elif max_range < 0.5:
            zoom = 11
          else:
            zoom = 10
        else:
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
        zoom = 10 if region == "Dallas Metro" else 9
      fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        mapbox=dict(center=dict(lat=center_lat, lon=center_lon), zoom=zoom),
        height=550,
        hovermode='closest'
      )
      st.plotly_chart(fig, width=1000)
      
      # Stats table
      st.subheader("Performance Stats")
      stats = tx.groupby('Pickup City').agg({
        'Net Earnings': ['mean', 'sum', 'count'],
        'Tip': 'mean'
      }).round(2)
      stats.columns = ['Avg Earnings', 'Total', 'Trips', 'Avg Tip']
      stats = stats.sort_values('Avg Earnings', ascending=False).head(10)
      st.dataframe(stats, width=1000)
  
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
    filtered = tx_region[(tx_region['Net Earnings'] >= min_earn) & (tx_region['Net Earnings'] <= max_earn)]
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
        color_continuous_scale='Plasma',
        size_max=20,
        height=500,
        mapbox_style='carto-positron',
        title='Individual Trips (Color & Size = Earnings)'
      )
      # Auto-zoom
      if len(trip_df) > 0:
        lat_range = trip_df['lat'].max() - trip_df['lat'].min()
        lon_range = trip_df['lon'].max() - trip_df['lon'].min()
        center_lat = (trip_df['lat'].max() + trip_df['lat'].min()) / 2
        center_lon = (trip_df['lon'].max() + trip_df['lon'].min()) / 2
        max_range = max(lat_range, lon_range) if max(lat_range, lon_range) > 0 else 1
        if region == "Dallas Metro":
          # Keep Dallas context tight
          if max_range < 0.2:
            zoom = 12
          elif max_range < 0.5:
            zoom = 11
          else:
            zoom = 10
        else:
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
        # Default Dallas view when no data
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), mapbox=dict(center=dict(lat=dallas_center[0], lon=dallas_center[1]), zoom=10))
      st.plotly_chart(fig, width=1000)
  
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
  
  st.dataframe(city_display, width=1000)
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
  
  st.dataframe(rest_display, width=1000)

# ============================================================================
# PAGE: SCHEDULE OPTIMIZER
# ============================================================================

elif page == "Schedule":
  # Load data
  data = get_data()
  if data is None:
    st.error("Could not load transaction data. Please ensure reports are generated.")
    st.stop()
  tx = data['transactions']
  
  st.title("Schedule Optimizer")
  st.write("Best times to work: hours and days that pay the most")
  
  st.divider()
  
  # Hourly analysis
  st.subheader("Best Hours to Drive (Earnings per Trip)")
  
  hourly = tx.groupby('Hour').agg({
    'Net Earnings': ['sum', 'mean', 'count'],
    'Tip': 'mean'
  }).round(2)
  hourly.columns = ['Total', 'Avg Per Trip', 'Trip Count', 'Avg Tip']
  hourly = hourly.sort_index()
  
  # Dual-axis chart: Avg earnings + trip volume
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
    yaxis='y2',
    line=dict(width=3)
  ))
  fig.update_layout(
    title="Average Earnings & Trip Volume by Hour",
    xaxis_title="Hour of Day",
    yaxis=dict(title=dict(text="Avg Earnings per Trip ($)", font=dict(color="lightblue"))),
    yaxis2=dict(title=dict(text="Number of Trips", font=dict(color="red")), overlaying='y', side='right'),
    hovermode='x unified',
    height=400
  )
  st.plotly_chart(fig, use_container_width=True)
  
  # Top 5 hours ranked
  st.write("**Top 5 Hours by Average Earnings:**")
  top_hours = hourly.nlargest(5, 'Avg Per Trip')[['Avg Per Trip', 'Trip Count', 'Avg Tip']].copy()
  top_hours.index.name = 'Hour'
  top_hours_display = top_hours.reset_index()
  top_hours_display['Hour'] = top_hours_display['Hour'].apply(lambda h: f"{h:02d}:00")
  top_hours_display.columns = ['Hour', 'Avg per Trip', 'Trips', 'Avg Tip']
  top_hours_display['Avg per Trip'] = top_hours_display['Avg per Trip'].apply(format_money)
  top_hours_display['Avg Tip'] = top_hours_display['Avg Tip'].apply(format_money)
  st.dataframe(top_hours_display, use_container_width=True, hide_index=True)
  
  st.divider()
  
  # Day of week analysis
  st.subheader("Best Days to Drive (Earnings per Trip)")
  
  dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  daily_stats = tx.groupby('DayOfWeek').agg({
    'Net Earnings': ['sum', 'mean', 'count']
  }).reindex(dow_order)
  daily_stats.columns = ['Total', 'Avg Per Trip', 'Trip Count']
  
  fig = px.bar(daily_stats.reset_index(), x='DayOfWeek', y='Avg Per Trip',
        title="Average Earnings per Trip by Day of Week",
        color='Avg Per Trip',
        color_continuous_scale='Greens',
        height=400)
  fig.update_xaxes(categoryorder="array", categoryarray=dow_order)
  fig.update_yaxes(title_text="Avg Earnings per Trip ($)")
  st.plotly_chart(fig, use_container_width=True)
  
  # Top days ranked with comparison
  st.write("**Days Ranked by Average Earnings:**")
  daily_display = daily_stats.copy()
  daily_display = daily_display.reset_index().sort_values('Avg Per Trip', ascending=False)
  daily_display.columns = ['Day', 'Total', 'Avg per Trip', 'Trips']
  daily_display['Total'] = daily_display['Total'].apply(format_money)
  daily_display['Avg per Trip'] = daily_display['Avg per Trip'].apply(format_money)
  st.dataframe(daily_display, use_container_width=True, hide_index=True)
  
  st.divider()
  
  # Weekday vs Weekend comparison
  st.subheader("Weekday vs Weekend")
  weekday_data = tx[tx['DayOfWeek'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])]
  weekend_data = tx[tx['DayOfWeek'].isin(['Saturday', 'Sunday'])]
  
  w1, w2 = st.columns(2)
  with w1:
    st.metric("Weekday Avg per Trip", 
              format_money(weekday_data['Net Earnings'].mean()) if not weekday_data.empty else "—",
              f"{len(weekday_data)} trips")
  with w2:
    st.metric("Weekend Avg per Trip",
              format_money(weekend_data['Net Earnings'].mean()) if not weekend_data.empty else "—",
              f"{len(weekend_data)} trips")
  
  st.divider()
  
  # Smart recommendations
  st.subheader("Your Optimal Schedule Recommendations")
  best_hour = hourly['Avg Per Trip'].idxmax()
  best_day = daily_stats['Avg Per Trip'].idxmax()
  worst_hour = hourly['Avg Per Trip'].idxmin()
  worst_day = daily_stats['Avg Per Trip'].idxmin()
  
  col1, col2, col3, col4 = st.columns(4)
  col1.success(f"Best Hour\n{best_hour:02d}:00\n{format_money(hourly.loc[best_hour, 'Avg Per Trip'])}")
  col2.success(f"Best Day\n{best_day}\n{format_money(daily_stats.loc[best_day, 'Avg Per Trip'])}")
  col3.info(f"Lowest Hour\n{worst_hour:02d}:00\n{format_money(hourly.loc[worst_hour, 'Avg Per Trip'])}")
  col4.info(f"Lowest Day\n{worst_day}\n{format_money(daily_stats.loc[worst_day, 'Avg Per Trip'])}")
  
  st.info(f"💡 **Peak Strategy:** Focus on {best_day}s around {best_hour:02d}:00 for maximum earnings.")
  
  # Only show availability warning if lowest hour has low trip count
  worst_hour_trips = int(hourly.loc[worst_hour, 'Trip Count'])
  if worst_hour_trips < 20:
    st.caption(f"⚠️ Note: Hour {worst_hour:02d}:00 has only {worst_hour_trips} trips, which may reflect limited availability (charging, personal time) rather than poor market demand.")
  else:
    st.caption(f"⚠️ Note: Hour {worst_hour:02d}:00 has {worst_hour_trips} trips with lower per-trip earnings — genuine market pattern, not limited availability.")

# ============================================================================
# PAGE: MILEAGE EFFICIENCY
# ============================================================================
elif page == "Issues":
  # Load data
  data = get_data()
  if data is None:
    st.error("Could not load transaction data. Please ensure reports are generated.")
    st.stop()
  tx = data['transactions']
  refunds_df = data['refunds']
  
  # Calculate metrics needed for this page
  total_earnings = tx['Net Earnings'].sum()
  total_miles = tx['Trip distance'].sum()
  avg_per_mile = total_earnings / (total_miles + 0.01)
  refund_count = (tx['Refund'] != 0).sum()
  refund_rate = refund_count / len(tx) * 100 if len(tx) > 0 else 0
  
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
    
    efficiency_formula = f"""
    **Efficiency Calculation:**
    
    $$\\text{{Efficiency}} = \\frac{{\\text{{Total Net Earnings}}}}{{\\text{{Total Miles}}}} = \\frac{{{format_money(total_earnings)}}}{{{total_miles:,.0f} \\text{{ mi}}}} = {format_money(avg_per_mile)}/\\text{{mi}}$$
    
    Your efficiency score measures how much you earn per mile driven. Higher is better!
    """
    st.markdown(efficiency_formula)
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
      
      st.dataframe(eff_display, width=1000, hide_index=True)
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
      
      st.dataframe(ref_display, width=1000, hide_index=True)
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
      st.dataframe(low_pay_display.head(20), width=1000, hide_index=True)

# ============================================================================
# PAGE: ROUTE OPTIMIZER
# ============================================================================

elif page == "Routes":
  # Load data
  data = get_data()
  if data is None:
    st.error("Could not load transaction data. Please ensure reports are generated.")
    st.stop()
  tx = data['transactions']
  
  st.title("Route Optimizer")
  st.write("Find the best areas to work based on time, earnings, and demand patterns")
  
  st.divider()
  
  # ===== MAP 1: TRIP PICKUP DENSITY BY RESTAURANT =====
  st.subheader("📍 Where Are You Picking Up? (by Restaurant)")
  
  # Top restaurants by trip volume (with context)
  restaurant_trips = tx[tx['Restaurant'].notna()].groupby('Restaurant').agg({
    'Trip UUID': 'count',
    'Net Earnings': ['sum', 'mean']
  }).reset_index()
  restaurant_trips.columns = ['Restaurant', 'Trips', 'Total Earnings', 'Avg per Trip']
  restaurant_trips = restaurant_trips.sort_values('Trips', ascending=False)
  
  # Key metrics
  m1, m2, m3, m4 = st.columns(4)
  m1.metric("Total Unique Restaurants", len(restaurant_trips))
  m2.metric("Most Popular", restaurant_trips.iloc[0]['Restaurant'] if not restaurant_trips.empty else "—")
  m3.metric("Trips from Top 3", int(restaurant_trips.head(3)['Trips'].sum()))
  m4.metric("Trips from Top 10", int(restaurant_trips.head(10)['Trips'].sum()))
  
  # Top 15 restaurants by trip count with earnings context
  st.write("**Top Restaurants by Trip Volume:**")
  rest_display = restaurant_trips.head(15).copy()
  rest_display['Total Earnings'] = rest_display['Total Earnings'].apply(format_money)
  rest_display['Avg per Trip'] = rest_display['Avg per Trip'].apply(format_money)
  st.dataframe(rest_display[['Restaurant', 'Trips', 'Total Earnings', 'Avg per Trip']], use_container_width=True)
  
  st.caption("💡 **Insight:** Focus on top 5 restaurants for 40%+ of your trip volume. Mix high-volume with high-pay to optimize earnings.")
  
  st.divider()
  
  # Heatmap with context: show trip concentration by restaurant
  st.write("**Trip Distribution Across All Restaurants:**")
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
      mapbox_style='carto-positron',
      color_continuous_scale='Reds',
      radius=30,
      zoom=9,
      title='Pickup Concentration: Red = More Trips from That Area'
    )
    fig_pickup.update_layout(
      margin=dict(l=0, r=0, t=40, b=0),
      mapbox=dict(center=dict(lat=32.85, lon=-96.85), zoom=9),
      height=500,
      hovermode='closest',
      coloraxis_colorbar=dict(title="Trip<br>Density")
    )
    st.plotly_chart(fig_pickup, use_container_width=True, key="pickup_heatmap")
    
    st.caption("🎯 **Red zones** = highest concentration of pickup orders. Focus delivery routes through these areas during peak hours.")
  else:
    st.warning("No pickup location data available")
  
  st.divider()
  
  # ===== MAP 2: TOP EARNING ZONES =====
  st.subheader("Top Earning Zones by Location")
  st.caption("Street-level view of top earning pickup locations")
  
  # Get actual pickup coordinates from addresses
  pickup_with_address = tx[tx['Pickup address'].notna()].copy()
  
  if not pickup_with_address.empty:
    # Get unique addresses to geocode
    unique_addresses = tuple(pickup_with_address['Pickup address'].unique().tolist())
    
    # Get coordinates (returns immediately with cached data, loads rest in background - non-blocking)
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
      pickup_agg = pickup_agg[pickup_agg['Trip Count'] >= 10].sort_values('Total Earnings', ascending=False).head(20)
      
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
          size_max=35,
          mapbox_style='carto-positron',
          height=500,
          title='Top Street-Level Earning Zones (Green = Best Efficiency)'
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
          margin=dict(l=0, r=0, t=40, b=0),
          mapbox=dict(center=dict(lat=center_lat, lon=center_lon), zoom=zoom_level),
          height=550,
          hovermode='closest'
        )
        st.plotly_chart(fig_pickup_zones, width=1000, key="pickup_zones_map")
      else:
        st.info("No locations with 2+ trips found")
    else:
      geocoded_count = sum(1 for lat, lon in coords_dict.values() if lat and lon)
      st.warning(f"Only {geocoded_count}/{len(unique_addresses)} addresses could be geocoded. Geocoding service may have limits.")
  else:
    st.info("No pickup address data available")
  
  st.divider()
  
  # ===== TABLE + MAP: TOP CITIES =====
  st.subheader("Top Cities by Earnings")
  
  city_stats = tx.groupby('Pickup City').agg({
    'Net Earnings': ['sum', 'mean', 'count']
  }).round(2)
  city_stats.columns = ['Total', 'Avg Earnings', 'Trip Count']
  city_stats = city_stats[city_stats['Trip Count'] >= 5].sort_values('Total', ascending=True).tail(10)
  
  # Bar chart: Total Earnings by City
  fig_total = px.bar(
    city_stats.reset_index(),
    x='Total',
    y='Pickup City',
    orientation='h',
    color='Avg Earnings',
    color_continuous_scale='RdYlGn',
    hover_data={'Avg Earnings': ':.2f', 'Trip Count': True},
    title='Total Earnings by City',
    labels={'Total': 'Total Earnings ($)', 'Pickup City': 'City'},
    height=400
  )
  fig_total.update_layout(
    margin=dict(l=100, r=40, t=50, b=40),
    coloraxis_colorbar=dict(title="Avg per Trip ($)")
  )
  fig_total.update_xaxes(tickformat='$,.0f')
  st.plotly_chart(fig_total, width=1000, key="top_cities_earnings")
  
  # Table view
  city_display = city_stats.copy().sort_values('Total', ascending=False)
  city_display['Total'] = city_display['Total'].apply(format_money)
  city_display['Avg Earnings'] = city_display['Avg Earnings'].apply(format_money)
  city_display['Trip Count'] = city_display['Trip Count'].astype(int)
  
  st.dataframe(city_display, width=1000)
  st.caption("Total earnings ranked by city. Green = higher avg earnings per trip, Red = lower. Focus on cities with both strong totals and high averages.")
  
  st.divider()
  
  # ===== TABLE + MAP: TOP RESTAURANTS =====
  st.subheader("Top Restaurants by Payouts")
  
  restaurant_stats = tx.groupby('Restaurant').agg({
    'Net Earnings': ['sum', 'mean', 'count'],
    'Pickup City': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown'
  }).round(2)
  restaurant_stats.columns = ['Total $', 'Avg Per Trip', 'Trips', 'City']
  restaurant_stats = restaurant_stats[restaurant_stats['Trips'] >= 3].sort_values('Total $', ascending=False)
  
  # Top 5 restaurants with metrics
  top_5 = restaurant_stats.head(5)
  cols = st.columns(5)
  for idx, (restaurant, row) in enumerate(top_5.iterrows()):
    with cols[idx]:
      st.metric(
        label=restaurant,
        value=format_money(row['Total $']),
        delta=f"Avg: {format_money(row['Avg Per Trip'])} | {int(row['Trips'])} trips"
      )
  
  # Pie chart: Earnings distribution
  fig_pie = px.pie(
    restaurant_stats.head(8).reset_index(),
    values='Total $',
    names='Restaurant',
    title='Earnings Distribution (Top 8)',
    hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Set3
  )
  fig_pie.update_layout(
    height=550,
    margin=dict(l=0, r=300, t=50, b=0),
    legend=dict(
      x=1.02,
      y=1.0,
      xanchor='left',
      yanchor='top',
      bgcolor='rgba(255,255,255,0.8)',
      bordercolor='lightgray',
      borderwidth=1,
      font=dict(size=14)
    ),
    font=dict(size=12)
  )
  st.plotly_chart(fig_pie, width=1000, key="restaurants_pie")
  
  # Table view
  rest_display = restaurant_stats.copy().head(15)
  rest_display['Total $'] = rest_display['Total $'].apply(format_money)
  rest_display['Avg Per Trip'] = rest_display['Avg Per Trip'].apply(format_money)
  rest_display['Trips'] = rest_display['Trips'].astype(int)
  
  st.dataframe(rest_display, width=1000)
  st.caption("Top restaurants ranked by total earnings. Pie chart shows earnings distribution across top 8 restaurants.")

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
# PAGE: ANOMALY DETECTION
# ============================================================================

elif page == "Anomaly Detection":
  # Load data
  data = get_data()
  if data is None:
    st.error("Could not load transaction data. Please ensure reports are generated.")
    st.stop()
  tx = data['transactions']
  multi_df = data['multi_account']
  
  # Calculate metrics
  refund_count = (tx['Refund'] != 0).sum()
  refund_rate = refund_count / len(tx) * 100 if len(tx) > 0 else 0
  
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
    
    st.dataframe(ref_display, width=1000, hide_index=True)
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
    st.dataframe(low_pay_display.head(20), width=1000, hide_index=True)
  
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
  # Load data
  data = get_data()
  if data is None:
    st.error("Could not load transaction data. Please ensure reports are generated.")
    st.stop()
  tx = data['transactions']
  audit_df = data['audit']
  multi_df = data['multi_account']
  daily_df = data['daily']
  
  st.title("Payment Reconciliation")
  st.write("Track Uber payments from daily earnings to bank deposits")
  
  st.divider()
  
  if not audit_df.empty:
    # Parse dates
    audit_df['Payment Date'] = pd.to_datetime(audit_df['Payment Date'], errors='coerce', utc=True).dt.tz_convert(None)
    if 'Bank Deposit Date' in audit_df.columns:
      audit_df['Bank Deposit Date'] = pd.to_datetime(audit_df['Bank Deposit Date'], errors='coerce', utc=True).dt.tz_convert(None)
    
    # Details view via query params
    # Use stable query params API
    try:
      params = st.query_params
    except Exception:
      params = {}
    payment_id_param = None
    if 'payment_id' in params:
      pval = params.get('payment_id')
      payment_id_param = pval[0] if isinstance(pval, list) and len(pval) > 0 else pval
    
    # Compute stable Record ID for linking
    import hashlib
    def _compute_payment_id(row):
      base = str(row.get('Payment Date')) + '|' + str(row.get('Payment Net Earnings')) + '|' + str(row.get('Payment Method')) + '|' + str(row.get('Payment Period Start')) + '|' + str(row.get('Payment Period End')) + '|' + str(row.get('Bank Deposit Date'))
      return hashlib.sha1(base.encode('utf-8', errors='ignore')).hexdigest()[:12]
    audit_df['Record ID'] = audit_df.apply(_compute_payment_id, axis=1)
    
    if payment_id_param:
      detail = audit_df[audit_df['Record ID'] == payment_id_param]
      st.subheader("Payment Details")
      if detail.empty:
        st.error("Payment record not found.")
      else:
        drow = detail.iloc[0]
        # Header metrics
        h1, h2, h3 = st.columns(3)
        h1.metric("Date", pd.to_datetime(drow['Payment Date']).strftime('%B %d, %Y'))
        h2.metric("Amount", format_money(drow.get('Payment Net Earnings', 0)))
        status_alias = {
          'BANK_MATCHED': 'Bank Matched',
          'REFUND_TRACKED': 'Refund Tracked',
          'OK': 'Recorded (Pending)'
        }
        h3.metric("Status", status_alias.get(drow.get('Reconciliation Status'), str(drow.get('Reconciliation Status'))))
        
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
          st.markdown("**From Uber**")
          pm = drow.get('Payment Method')
          st.caption(f"Method: {pm if pd.notna(pm) else '—'}")
          if pd.notna(drow.get('Payment Period Start')):
            start = pd.to_datetime(drow['Payment Period Start']).strftime('%b %d')
            end = pd.to_datetime(drow['Payment Period End']).strftime('%b %d, %Y')
            st.caption(f"Period: {start} - {end}")
          st.caption(f"Trips: {drow.get('Trip Count', '—')}")
        with c2:
          st.markdown("**Bank**")
          bd = drow.get('Bank Deposit Date')
          if pd.notna(bd):
            st.caption(f"Deposited: {pd.to_datetime(bd).strftime('%B %d, %Y')}")
          else:
            st.caption("Deposited: Pending")
          if pd.notna(drow.get('Bank Amount')):
            st.caption(f"Bank Amount: {format_money(drow['Bank Amount'])}")
          if pd.notna(drow.get('Days to Deposit')):
            st.caption(f"Processing: {int(drow['Days to Deposit'])} days")
        
        st.markdown("---")
        st.markdown("**Location**")
        pickup = drow.get('Pickup address')
        dropoff = drow.get('Drop off address')
        if pd.notna(pickup) or pd.notna(dropoff):
          if pd.notna(pickup):
            st.caption(f"From: {pickup}")
            coords = get_coordinates_for_addresses([pickup])
            plat, plon = coords.get(pickup, (None, None))
            if pd.notna(plat) and pd.notna(plon):
              st.caption(f"[Open From in Maps](https://www.google.com/maps?q={plat},{plon})")
          if pd.notna(dropoff):
            st.caption(f"To: {dropoff}")
            coords2 = get_coordinates_for_addresses([dropoff])
            dlat, dlon = coords2.get(dropoff, (None, None))
            if pd.notna(dlat) and pd.notna(dlon):
              st.caption(f"[Open To in Maps](https://www.google.com/maps?q={dlat},{dlon})")
        else:
          st.caption("Addresses not available in payment record.")
        
        st.markdown("---")
        if st.button("Back to Payments"):
          try:
            # Clear details param and navigate back to Payments
            st.query_params = {"page": "Payments"}
          except Exception:
            pass
          try:
            st.rerun()
          except Exception:
            pass
      st.stop()
    
    # Filters
    st.subheader("All Payments")
    st.divider()
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
      search_text = st.text_input("Search", placeholder="Enter amount, status, or month name")
    
    with col2:
      # Friendly status labels mapped to internal codes
      status_labels = {
        "All": None,
        "Bank Matched": "BANK_MATCHED",
        "Refund Tracked": "REFUND_TRACKED",
        "Recorded (Pending)": "OK"
      }
      status_choice = st.selectbox("Status", list(status_labels.keys()))
    
    with col3:
      if 'Payment Date' in audit_df.columns:
        months = sorted(audit_df['Payment Date'].dt.to_period('M').unique().astype(str), reverse=True)
        month_filter = st.selectbox("Month", ["All"] + months)
    
    # Apply filters
    filtered_df = audit_df.copy()
    
    # Status filter (map friendly label to internal code)
    internal_status = status_labels.get(status_choice)
    if internal_status:
      filtered_df = filtered_df[filtered_df['Reconciliation Status'] == internal_status]
    
    # Month filter
    if month_filter != "All":
      filtered_df = filtered_df[filtered_df['Payment Date'].dt.to_period('M').astype(str) == month_filter]
    
    # Text search
    if search_text:
      search_lower = search_text.lower()
      mask = (
        filtered_df['Payment Net Earnings'].astype(str).str.contains(search_lower, na=False) |
        filtered_df['Reconciliation Status'].astype(str).str.lower().str.contains(search_lower, na=False) |
        filtered_df['Payment Date'].dt.strftime('%B %Y').str.lower().str.contains(search_lower, na=False)
      )
      filtered_df = filtered_df[mask]
    
    # Sums for current filtered set
    st.markdown("**Totals (Filtered):**")
    total_amount = filtered_df['Payment Net Earnings'].sum() if 'Payment Net Earnings' in filtered_df.columns else 0
    matched_mask = filtered_df['Bank Deposit Date'].notna() if 'Bank Deposit Date' in filtered_df.columns else pd.Series([False]*len(filtered_df))
    deposited_amount = filtered_df.loc[matched_mask, 'Payment Net Earnings'].sum() if 'Payment Net Earnings' in filtered_df.columns else 0
    pending_amount = filtered_df.loc[~matched_mask, 'Payment Net Earnings'].sum() if 'Payment Net Earnings' in filtered_df.columns else 0

    col_tot1, col_tot2, col_tot3 = st.columns(3)
    col_tot1.metric("Total", format_money(total_amount))
    col_tot2.metric("Deposited", format_money(deposited_amount))
    col_tot3.metric("Pending", format_money(pending_amount))

    # Monthly totals (Filtered)
    st.markdown("**Monthly Totals (Filtered):**")
    if 'Payment Date' in filtered_df.columns and 'Payment Net Earnings' in filtered_df.columns:
      monthly = (
        filtered_df
        .groupby(filtered_df['Payment Date'].dt.to_period('M'))['Payment Net Earnings']
        .sum()
        .reset_index()
      )
      monthly['Month'] = monthly['Payment Date'].astype(str)
      monthly['Amount'] = monthly['Payment Net Earnings'].apply(format_money)
      st.dataframe(monthly[['Month', 'Amount']].sort_values('Month', ascending=False), width=600, hide_index=True)

    # Display table
    display_df = filtered_df.sort_values('Payment Date', ascending=False).head(100).copy()
    display_df['Date'] = display_df['Payment Date'].dt.strftime('%b %d, %Y')
    display_df['Amount'] = display_df['Payment Net Earnings'].apply(format_money)
    # Map status to friendly labels for display
    status_alias = {
      'BANK_MATCHED': 'Bank Matched',
      'REFUND_TRACKED': 'Refund Tracked',
      'OK': 'Recorded (Pending)'
    }
    display_df['Status'] = display_df['Reconciliation Status'].map(lambda s: status_alias.get(s, str(s)))
    
    # Always include restaurant/address columns if available
    if 'Pickup address' in display_df.columns:
      display_df['From'] = display_df['Pickup address']
    else:
      display_df['From'] = ''
    if 'Drop off address' in display_df.columns:
      display_df['To'] = display_df['Drop off address']
    else:
      display_df['To'] = ''
    # Ensure Record ID exists for details link
    if 'Record ID' not in display_df.columns:
      import hashlib
      def _compute_payment_id_tbl(row):
        base = str(row.get('Payment Date')) + '|' + str(row.get('Payment Net Earnings')) + '|' + str(row.get('Payment Method')) + '|' + str(row.get('Payment Period Start')) + '|' + str(row.get('Payment Period End')) + '|' + str(row.get('Bank Deposit Date'))
        return hashlib.sha1(base.encode('utf-8', errors='ignore')).hexdigest()[:12]
      display_df['Record ID'] = display_df.apply(_compute_payment_id_tbl, axis=1)
    
    # Add Deposited column if available and Details link
    if 'Bank Deposit Date' in display_df.columns:
      display_df['Deposited'] = display_df['Bank Deposit Date'].dt.strftime('%b %d, %Y').fillna('Pending')
      display_df['Details'] = display_df['Record ID'].apply(lambda rid: f"[Open](/?page=Payments&payment_id={rid})")
      st.dataframe(
        display_df[['Date', 'Amount', 'Status', 'From', 'To', 'Deposited', 'Details']],
        width=1000,
        hide_index=True
      )
    else:
      display_df['Details'] = display_df['Record ID'].apply(lambda rid: f"[Open](/?page=Payments&payment_id={rid})")
      st.dataframe(
        display_df[['Date', 'Amount', 'Status', 'From', 'To', 'Details']],
        width=1000,
        hide_index=True
      )
    
    st.caption(f"Showing {len(display_df)} of {len(filtered_df)} filtered payments ({len(audit_df)} total)")
    
    st.divider()
    st.subheader("Payment Timeline")
    
    # Daily timeline
    daily_payment = audit_df.groupby(audit_df['Payment Date'].dt.date).agg({
      'Payment Net Earnings': 'sum'
    }).reset_index()
    daily_payment.columns = ['Date', 'Amount']
    daily_payment['Date'] = pd.to_datetime(daily_payment['Date'])
    daily_payment = daily_payment.sort_values('Date')
    
    fig = px.bar(daily_payment, x='Date', y='Amount',
          title="Daily Payment Timeline",
          labels={'Amount': 'Amount Reported', 'Date': 'Payment Date'},
          color_discrete_sequence=['#1f77b4'],
          height=400)
    fig.update_yaxes(tickformat='$,.2f')
    st.plotly_chart(fig, use_container_width=False, width=1000)
    
    st.divider()
    st.subheader("Processing Delay Analysis")
    
    # Compute 'Processing Days' robustly from dates if column missing
    proc_df = audit_df.copy()
    if 'Days to Deposit' in proc_df.columns:
      proc_df['Processing Days'] = proc_df['Days to Deposit']
    elif 'Payment Date' in proc_df.columns and 'Bank Deposit Date' in proc_df.columns:
      proc_df['Processing Days'] = (proc_df['Bank Deposit Date'] - proc_df['Payment Date']).dt.days

    if 'Processing Days' in proc_df.columns:
      processing_data = proc_df[(proc_df['Processing Days'].notna()) &
                                (proc_df['Processing Days'] >= 0) &
                                (proc_df['Processing Days'] <= 30)].copy()

      if not processing_data.empty:
        # View toggle: Distribution vs Trend Over Time
        view_choice = st.radio("View", ["Distribution", "Trend Over Time"], horizontal=True)

        if view_choice == "Distribution":
          chart_type = st.radio("Chart Type", ["Histogram", "Line"], horizontal=True)
          if chart_type == "Histogram":
            fig = px.histogram(processing_data, x='Processing Days', nbins=10,
                               title="How Many Days Until Payment Shows in Bank",
                               color_discrete_sequence=['#FF8C00'],
                               height=400)
            fig.update_xaxes(title="Days to Deposit")
            fig.update_yaxes(title="Count")
            st.plotly_chart(fig, use_container_width=False, width=1000)
          else:
            # Line distribution: count of payments by processing day
            dist = processing_data.groupby('Processing Days').size().reset_index(name='Count')
            dist = dist.sort_values('Processing Days')
            fig = px.line(dist, x='Processing Days', y='Count',
                          title="Count of Payments by Processing Day",
                          markers=True, height=400)
            fig.update_xaxes(title="Days to Deposit")
            fig.update_yaxes(title="Count")
            st.plotly_chart(fig, use_container_width=False, width=1000)
        else:
          # Trend over time: average processing days per period
          agg_choice = st.selectbox("Aggregate by", ["Day", "Week", "Month"], index=1)
          temp = processing_data[['Payment Date', 'Processing Days']].copy()
          temp['Payment Date'] = pd.to_datetime(temp['Payment Date'])

          if agg_choice == "Day":
            trend = temp.groupby(temp['Payment Date'].dt.date)['Processing Days'].mean().reset_index()
            trend['Date'] = pd.to_datetime(trend['Payment Date'])
          elif agg_choice == "Week":
            trend = temp.groupby(temp['Payment Date'].dt.to_period('W'))['Processing Days'].mean().reset_index()
            trend['Date'] = trend['Payment Date'].dt.start_time
          else:
            trend = temp.groupby(temp['Payment Date'].dt.to_period('M'))['Processing Days'].mean().reset_index()
            trend['Date'] = trend['Payment Date'].dt.to_timestamp()

          trend = trend.sort_values('Date')
          trend.rename(columns={'Processing Days': 'Avg Processing Days'}, inplace=True)
          fig = px.line(trend, x='Date', y='Avg Processing Days',
                        title="Average Processing Days Over Time",
                        markers=True, height=400,
                        color_discrete_sequence=['#FF8C00'])
          fig.update_yaxes(title="Avg Days")
          fig.update_xaxes(title="Date")
          st.plotly_chart(fig, use_container_width=False, width=1000)

        # Summary metrics
        avg_delay = processing_data['Processing Days'].mean()
        max_delay = processing_data['Processing Days'].max()
        col1, col2, col3 = st.columns(3)
        col1.metric("Average", f"{avg_delay:.1f} days")
        col2.metric("Longest", f"{int(max_delay)} days")
        col3.metric("Total Payments", len(processing_data))
    
    st.divider()
    st.subheader("Status Breakdown")
    
    if 'Reconciliation Status' in audit_df.columns:
      status_alias = {
        'BANK_MATCHED': 'Bank Matched',
        'REFUND_TRACKED': 'Refund Tracked',
        'OK': 'Recorded (Pending)'
      }
      status_counts = audit_df['Reconciliation Status'].value_counts()
      # Map internal codes to friendly names for chart labels
      friendly_names = [status_alias.get(s, str(s)) for s in status_counts.index]
      
      fig = px.pie(
        values=status_counts.values,
        names=friendly_names,
        title="Payment Status Distribution",
        color_discrete_map={
          'Bank Matched': '#2ca02c',
          'Refund Tracked': '#ff7f0e',
          'Recorded (Pending)': '#1f77b4'
        },
        height=400
      )
      st.plotly_chart(fig, use_container_width=False, width=1000)
      
      st.markdown("**Status Key:**")
      st.markdown("- **Bank Matched**: Payment confirmed in bank deposits")
      st.markdown("- **Refund Tracked**: Payment includes refund data")
      st.markdown("- **Recorded (Pending)**: Payment recorded by Uber, not yet found in bank")

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
    
    st.dataframe(display_df, width=1000, hide_index=True)
    
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
      st.plotly_chart(fig, width=1000)
    
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
  # Load data
  data = get_data()
  if data is None:
    st.error("Could not load transaction data. Please ensure reports are generated.")
    st.stop()
  tx = data['transactions']
  
  st.title("Trends & Forecast")
  st.write("Long-term patterns, seasonality, and what's changing")
  
  st.divider()
  
  # Monthly earnings trend
  st.subheader("Monthly Earnings Trend")
  
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
  st.plotly_chart(fig, width=1000)
  
  st.divider()
  
  # Key changes
  st.subheader("What's Changing?")
  
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
  # Load data
  data = get_data()
  if data is None:
    st.error("Could not load transaction data. Please ensure reports are generated.")
    st.stop()
  tx = data['transactions']
  
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
  ## EXECUTIVE OVERVIEW
  
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
  
  st.markdown(rf"""
  ## BUSINESS PERFORMANCE ANALYSIS
  
  ### Financial Performance
  
  Your courier operation generated **{format_money(total_annual_earnings)}** in net earnings across **{total_annual_trips:,}** active trips. 
  This represents a significant volume of delivery work with measurable profitability metrics. 
  The average trip yield was **{format_money(avg_per_trip_annual)}**, while your cost efficiency stood at **{format_money(avg_per_mile_annual)} per mile driven**.
  
  The transportation network analysis reveals operation across **{unique_cities:,}** unique cities and **{unique_restaurants:,}** distinct restaurants, 
  indicating a diversified service portfolio. This geographic and vendor diversification is a strength, as it 
  reduces dependency on any single market or client segment.
  
  ### Operational Efficiency Metrics
  
  **Efficiency Formula:** Your cost efficiency is calculated as:
  
  $$\eta = \frac{{\text{{Total Net Earnings}}}}{{\text{{Total Miles Driven}}}} = \frac{{{format_money(total_annual_earnings)}}}{{{total_annual_miles:,.0f} \text{{ mi}}}} = {format_money(avg_per_mile_annual)}/\text{{mile}}$$
  
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
  st.plotly_chart(fig_monthly, width=1000)
  
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
  st.plotly_chart(fig_cities, width=1000)
  
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
  st.plotly_chart(fig_restaurants, width=1000)
  
  st.divider()
  
  st.markdown(rf"""
  ## STRATEGIC RECOMMENDATIONS
  
  Based on comprehensive analysis of {total_annual_trips:,} trips across {len(monthly_data)} months:
  
  **1. REVENUE OPTIMIZATION**
  
  Target efficiency growth:
  $$\eta_{{\text{{target}}}} = \eta_{{\text{{current}}}} \times 1.20 = {format_money(avg_per_mile_annual)} \times 1.20 = {format_money(avg_per_mile_annual * 1.20)}/\text{{mile}}$$
  
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
  
  st.markdown(rf"""
  ## CONCLUSION
  
  This year demonstrates a **operationally sound and financially viable** courier business. 
  With {total_annual_trips:,} trips and {format_money(total_annual_earnings)} in earnings, 
  you've established a sustainable delivery operation with clear growth opportunities.
  
  **Primary Focus for Next Year:**
  
  $$\begin{{aligned}}
  \text{{1. Efficiency}} & : {format_money(avg_per_mile_annual)}/\text{{mi}} \rightarrow {format_money(avg_per_mile_annual * 1.20)}/\text{{mi}} \\
  \text{{2. Monthly Volume}} & : {total_annual_trips / len(monthly_data):.0f} \rightarrow {total_annual_trips / len(monthly_data) * 1.25:.0f} \text{{ trips}} \\
  \text{{3. Monitor}} & : \text{{Shop & Pay lag times}}
  \end{{aligned}}$$
  
  *Report Generated: Year-End {pd.Timestamp.now().year} | Data Period: {format_month_human(monthly_data.iloc[0]['Month'])} – {format_month_human(monthly_data.iloc[-1]['Month'])}*
  """)

st.divider()
st.caption("Courier Insights • Purpose-built for courier optimization • Last updated: today")
