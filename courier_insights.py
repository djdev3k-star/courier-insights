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

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    /* Main Container */
    .main {
        padding-top: 2rem !important;
    }
    
    /* Sidebar Logo */
    .logo-container {
        text-align: center;
        padding: 8px 0;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    .logo-container img {
        max-width: 140px;
        height: auto;
    }
    
    /* Sidebar Metrics - Clean and Minimal */
    .sidebar-metrics {
        background: #f8f9fa;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 24px;
        border-left: 4px solid #0066cc;
    }
    
    .metrics-header {
        font-size: 12px;
        font-weight: 700;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        display: block;
    }
    
    .metric-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-size: 13px;
    }
    
    .metric-label {
        color: #666;
        font-weight: 500;
    }
    
    .metric-value {
        color: #0066cc;
        font-weight: 700;
    }
    
    /* Navigation Section */
    .nav-section {
        margin-bottom: 8px;
    }
    
    .nav-label {
        font-size: 11px;
        font-weight: 700;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 12px 0 8px 0;
        display: block;
    }
    
    /* Radio button styling */
    [role="radio"] {
        background: transparent !important;
    }
    
    .stRadio > label {
        padding: 8px 12px !important;
        border-radius: 6px !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        margin-bottom: 4px !important;
    }
    
    .stRadio > label:hover {
        background: #f0f2f6 !important;
    }
    
    /* Page Title */
    .page-title {
        color: #0066cc;
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Page Header Styling */
    h1 {
        color: #1a1a1a !important;
        border-bottom: 2px solid #0066cc;
        padding-bottom: 12px;
        margin-bottom: 16px;
    }
    
    h2 {
        color: #0066cc !important;
        margin-top: 24px;
        margin-bottom: 12px;
        font-weight: 700;
    }
    
    h3 {
        color: #333 !important;
        margin-top: 16px;
        margin-bottom: 10px;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: rgba(0, 0, 0, 0.08);
        margin: 20px 0;
    }
    
    /* Data Tables */
    .dataframe {
        background: #f8f9fa !important;
        border-radius: 8px !important;
    }
    
    .stDataFrame {
        margin: 16px 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 16px;
        border-radius: 8px;
        border: 1px solid #e8eaed;
        margin-bottom: 12px;
    }
    
    /* Sidebar header text */
    .stSidebar h3 {
        color: #1a1a1a;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 12px;
        margin-top: 0;
    }
    
    .stSidebar p {
        color: #666;
        font-size: 13px;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# GLOBAL HELPER FUNCTIONS
# ============================================================================

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
        if len(parts) >= 3:
            # City is typically 2 parts before end (before State ZIP)
            return parts[-2].strip()
        return 'Unknown'
    
    def extract_zip(addr):
        if pd.isna(addr):
            return ''
        parts = str(addr).split(',')
        if len(parts) >= 3:
            # ZIP is in the last part before US, extract 5-digit code
            state_zip = parts[-2].strip()  # e.g., "TX 75126"
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
    
    # Key Metrics Panel
    st.markdown('<span class="metrics-header">Performance Metrics</span>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-metrics">', unsafe_allow_html=True)
    
    metrics_html = f"""
    <div class="metric-row">
        <span class="metric-label">Total Earnings</span>
        <span class="metric-value">{format_money(total_earnings)}</span>
    </div>
    <div class="metric-row">
        <span class="metric-label">Total Miles</span>
        <span class="metric-value">{total_miles:,.0f}</span>
    </div>
    <div class="metric-row">
        <span class="metric-label">$/Mile</span>
        <span class="metric-value">{format_money(avg_per_mile)}</span>
    </div>
    <div class="metric-row">
        <span class="metric-label">Total Trips</span>
        <span class="metric-value">{total_trips:,}</span>
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
    
    # Navigation Section
    st.markdown('<span class="nav-label">Navigation</span>', unsafe_allow_html=True)
    page = st.radio("", [
        "🏠 Opportunity Finder",
        "📍 Location Intelligence", 
        "⏰ Schedule Optimizer",
        "🛣️ Mileage Efficiency",
        "⚠️ Anomaly Detection",
        "� Payment Reconciliation",
        "�🔍 Dispute Forensics",
        "📊 Trends & Forecast"
    ], label_visibility="collapsed")

# ============================================================================
# PAGE: OPPORTUNITY FINDER (Home)
# ============================================================================

if page == "🏠 Opportunity Finder":
    st.title("🏠 Opportunity Finder")
    st.write("Outliers, alerts, and opportunities to optimize your earnings")
    
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
    
    # ALERTS SECTION
    st.subheader("🚨 Active Alerts")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if refund_count > 0:
            st.error(f"⚠️ {refund_count} Refunds Detected")
            st.caption(f"Total refund amount: {format_money(tx['Refund'].sum())}")
    
    with col2:
        if low_pay_trips > 0:
            st.warning(f"📉 {low_pay_trips} Low-Pay Trips")
            st.caption(f"<$3.00 (investigate why)")
    
    with col3:
        if high_pay_trips > 0:
            st.success(f"💰 {high_pay_trips} High-Pay Trips")
            st.caption(f">$15.00 (replicate this!)")
    
    st.divider()
    
    # OUTLIERS: Worst trips
    st.subheader("🔴 Worst Performing Trips")
    worst = tx.nsmallest(10, 'Net Earnings')[['Trip drop off time', 'Restaurant', 'Pickup City', 'Trip distance', 'Net Earnings', 'Refund']]
    worst_display = worst.copy()
    worst_display['Trip drop off time'] = worst_display['Trip drop off time'].dt.strftime('%m-%d %H:%M')
    worst_display['Location'] = worst_display['Restaurant'] + ' (' + worst_display['Pickup City'] + ')'
    worst_display = worst_display[['Trip drop off time', 'Location', 'Trip distance', 'Net Earnings', 'Refund']]
    worst_display['Trip distance'] = worst_display['Trip distance'].apply(lambda x: f"{x:.1f}mi")
    worst_display['Net Earnings'] = worst_display['Net Earnings'].apply(format_money)
    worst_display['Refund'] = worst_display['Refund'].apply(lambda x: format_money(x) if x != 0 else "—")
    
    st.dataframe(worst_display, width='stretch', hide_index=True)
    st.caption("Why were these low? Refund? Bad location? Check Dispute Forensics for details.")
    
    st.divider()
    
    # OUTLIERS: Best trips
    st.subheader("🟢 Best Performing Trips")
    best = tx.nlargest(10, 'Net Earnings')[['Trip drop off time', 'Restaurant', 'Pickup City', 'Trip distance', 'Net Earnings', 'Tip']]
    best_display = best.copy()
    best_display['Trip drop off time'] = best_display['Trip drop off time'].dt.strftime('%m-%d %H:%M')
    best_display['Location'] = best_display['Restaurant'] + ' (' + best_display['Pickup City'] + ')'
    best_display = best_display[['Trip drop off time', 'Location', 'Trip distance', 'Net Earnings', 'Tip']]
    best_display['Trip distance'] = best_display['Trip distance'].apply(lambda x: f"{x:.1f}mi")
    best_display['Net Earnings'] = best_display['Net Earnings'].apply(format_money)
    best_display['Tip'] = best_display['Tip'].apply(format_money)
    
    st.dataframe(best_display, width='stretch', hide_index=True)
    st.caption("Pattern: What made these trips valuable? Location? Time? Distance? Replicate!")
    
    st.divider()
    
    # Most efficient trips
    st.subheader("⚡ Most Efficient Trips ($/Mile)")
    efficient = tx.nlargest(10, 'Earnings Per Mile')[['Trip drop off time', 'Restaurant', 'Pickup City', 'Trip distance', 'Net Earnings', 'Earnings Per Mile']]
    eff_display = efficient.copy()
    eff_display['Trip drop off time'] = eff_display['Trip drop off time'].dt.strftime('%m-%d %H:%M')
    eff_display['Location'] = eff_display['Restaurant'] + ' (' + eff_display['Pickup City'] + ')'
    eff_display = eff_display[['Trip drop off time', 'Location', 'Trip distance', 'Net Earnings', 'Earnings Per Mile']]
    eff_display['Trip distance'] = eff_display['Trip distance'].apply(lambda x: f"{x:.1f}mi")
    eff_display['Net Earnings'] = eff_display['Net Earnings'].apply(format_money)
    eff_display['Earnings Per Mile'] = eff_display['Earnings Per Mile'].apply(format_money)
    
    st.dataframe(eff_display, width='stretch', hide_index=True)
    st.caption("These trips were quick money. Short distance, good payout = maximize these!")

# ============================================================================
# PAGE: LOCATION INTELLIGENCE
# ============================================================================

elif page == "📍 Location Intelligence":
    st.title("📍 Location Intelligence")
    st.write("Which cities, restaurants, and areas pay best?")
    
    st.divider()
    
    # Top cities at a glance
    st.subheader("🏙️ Your Top Cities")
    
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
    st.subheader("🏙️ Best Cities to Work (by earnings)")
    
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
    st.subheader("🍽️ Best Restaurants to Pickup From")
    
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
    st.caption("Watch refunds by restaurant - some locations have quality/timing issues")
    
    st.divider()
    
    # Zip code heatmap
    st.subheader("📌 Earnings by Zip Code")
    
    zip_stats = tx.groupby('Pickup Zip').agg({
        'Net Earnings': ['sum', 'mean', 'count'],
        'Tip': 'mean'
    }).round(2)
    zip_stats.columns = ['Total', 'Avg Earnings', 'Trip Count', 'Avg Tip']
    zip_stats = zip_stats[zip_stats['Trip Count'] >= 2].sort_values('Avg Earnings', ascending=False)
    
    zip_display = zip_stats.copy()
    zip_display['Total'] = zip_display['Total'].apply(format_money)
    zip_display['Avg Earnings'] = zip_display['Avg Earnings'].apply(format_money)
    zip_display['Avg Tip'] = zip_display['Avg Tip'].apply(format_money)
    zip_display['Trip Count'] = zip_display['Trip Count'].astype(int)
    
    st.dataframe(zip_display, width='stretch')
    
    st.divider()
    
    # City-Zip breakdown (detailed view)
    st.subheader("🗺️ Detailed: City Names with Zip Codes")
    
    detailed = tx.groupby(['Pickup City', 'Pickup Zip']).agg({
        'Net Earnings': ['sum', 'mean', 'count'],
        'Refund': 'sum'
    }).round(2)
    detailed.columns = ['Total Earnings', 'Avg Per Trip', 'Trips', 'Total Refunds']
    detailed = detailed[detailed['Trips'] >= 2].sort_values('Avg Per Trip', ascending=False)
    
    detail_display = detailed.copy()
    detail_display.index.names = ['City', 'Zip']
    detail_display = detail_display.reset_index()
    detail_display['Location'] = detail_display['City'] + ' ' + detail_display['Zip']
    detail_display = detail_display[['Location', 'Total Earnings', 'Avg Per Trip', 'Trips', 'Total Refunds']]
    
    detail_display['Total Earnings'] = detail_display['Total Earnings'].apply(format_money)
    detail_display['Avg Per Trip'] = detail_display['Avg Per Trip'].apply(format_money)
    detail_display['Total Refunds'] = detail_display['Total Refunds'].apply(format_money)
    detail_display['Trips'] = detail_display['Trips'].astype(int)
    
    st.dataframe(detail_display, width='stretch', hide_index=True)
    
    st.divider()
    
    # Earnings distribution by city
    st.subheader("📊 Earnings Distribution by City")
    
    top_cities = tx['Pickup City'].value_counts().head(8).index
    city_data = tx[tx['Pickup City'].isin(top_cities)]
    
    fig = px.box(city_data, x='Pickup City', y='Net Earnings',
                title="Earnings Range by Top Cities",
                color='Pickup City',
                height=400)
    st.plotly_chart(fig, width='stretch')
    
    st.divider()
    
    # Restaurant earnings trend
    st.subheader("🍔 Top Restaurants - Earnings Comparison")
    
    top_restaurants = tx['Restaurant'].value_counts().head(10).index
    rest_data = tx[tx['Restaurant'].isin(top_restaurants)]
    
    fig = px.box(rest_data, x='Restaurant', y='Net Earnings',
                title="Earnings Range by Top Restaurants (10+ orders)",
                color='Restaurant',
                height=400)
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig, width='stretch')

# ============================================================================
# PAGE: SCHEDULE OPTIMIZER
# ============================================================================

elif page == "⏰ Schedule Optimizer":
    st.title("⏰ Schedule Optimizer")
    st.write("Best times to work: hours and days that pay the most")
    
    st.divider()
    
    # Hourly analysis
    st.subheader("⏱️ Earnings by Hour of Day")
    
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
    st.subheader("📅 Earnings by Day of Week")
    
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
    st.subheader("💡 Your Optimal Schedule")
    best_hour = hourly['Avg Per Trip'].idxmax()
    best_day = daily_stats['Avg Per Trip'].idxmax()
    
    col1, col2 = st.columns(2)
    col1.success(f"Best Hour: {best_hour:02d}:00 - {format_money(hourly.loc[best_hour, 'Avg Per Trip'])} avg")
    col2.success(f"Best Day: {best_day} - {format_money(daily_stats.loc[best_day, 'Avg Per Trip'])} avg")

# ============================================================================
# PAGE: MILEAGE EFFICIENCY
# ============================================================================

elif page == "🛣️ Mileage Efficiency":
    st.title("🛣️ Mileage Efficiency")
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
    st.subheader("📈 Efficiency Trend Over Time")
    
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
    st.subheader("📊 Trip Distance Distribution")
    
    fig = px.histogram(tx, x='Trip distance', nbins=30,
                      title="How far are your trips?",
                      color_discrete_sequence=['#2ca02c'],
                      height=400)
    fig.update_xaxes(title="Trip Distance (miles)")
    fig.update_yaxes(title="Number of Trips")
    st.plotly_chart(fig, width='stretch')
    
    st.divider()
    
    # Long distance vs short distance comparison
    st.subheader("🎯 Short Trips vs Long Trips")
    
    short = tx[tx['Trip distance'] <= 3]
    long = tx[tx['Trip distance'] > 10]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Short Trips (≤3 mi)", len(short))
        st.metric("  Avg Earnings", format_money(short['Net Earnings'].mean()))
        st.metric("  $/Mile", format_money(short['Net Earnings'].sum() / short['Trip distance'].sum()))
    
    with col2:
        st.metric("Long Trips (>10 mi)", len(long))
        st.metric("  Avg Earnings", format_money(long['Net Earnings'].mean()))
        st.metric("  $/Mile", format_money(long['Net Earnings'].sum() / long['Trip distance'].sum() if long['Trip distance'].sum() > 0 else 0))

# ============================================================================
# PAGE: ANOMALY DETECTION
# ============================================================================

elif page == "⚠️ Anomaly Detection":
    st.title("⚠️ Anomaly Detection")
    st.write("Payment issues, refunds, and reconciliation problems")
    
    st.divider()
    
    # Refund summary
    st.subheader("💸 Refund Analysis")
    
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
    st.subheader("📉 Suspiciously Low Payments")
    
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
        st.subheader("🏦 Bank Reconciliation Status")
        
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

elif page == "💰 Payment Reconciliation":
    st.title("💰 Payment Reconciliation")
    st.write("Compare Uber payments reported to bank deposits • Track payment processing timeline")
    
    st.divider()
    
    # Summary metrics
    st.subheader("📊 Payment Summary")
    
    if not audit_df.empty:
        # Parse payment dates
        audit_df['Payment Date'] = pd.to_datetime(audit_df['Payment Date'], errors='coerce')
        if 'Bank Deposit Date' in audit_df.columns:
            audit_df['Bank Deposit Date'] = pd.to_datetime(audit_df['Bank Deposit Date'], errors='coerce')
        
        total_payments = audit_df['Payment Net Earnings'].sum() if 'Payment Net Earnings' in audit_df.columns else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Uber Reported", format_money(total_payments))
        
        # Count matched deposits
        matched = len(audit_df[audit_df['Bank Deposit Date'].notna()]) if 'Bank Deposit Date' in audit_df.columns else 0
        col2.metric("Deposits Matched", f"{matched}/{len(audit_df)}")
        
        # Reconciliation statuses
        if 'Reconciliation Status' in audit_df.columns:
            status_counts = audit_df['Reconciliation Status'].value_counts()
            col3.metric("Bank Matched", status_counts.get('BANK_MATCHED', 0))
            col4.metric("Refund Tracked", status_counts.get('REFUND_TRACKED', 0))
    
    st.divider()
    
    # Daily breakdown
    st.subheader("📅 Daily Payment Timeline")
    
    if not audit_df.empty and 'Payment Date' in audit_df.columns:
        # Group by payment date to see daily totals
        daily_payment = audit_df.groupby(audit_df['Payment Date'].dt.date).agg({
            'Payment Net Earnings': 'sum'
        }).reset_index()
        daily_payment.columns = ['Date', 'Payments Reported']
        daily_payment['Date'] = daily_payment['Date'].astype(str)
        
        # Group by deposit date if available
        if 'Bank Deposit Date' in audit_df.columns:
            daily_deposit = audit_df.dropna(subset=['Bank Deposit Date']).groupby(audit_df['Bank Deposit Date'].dt.date).agg({
                'Payment Net Earnings': 'sum'
            }).reset_index()
            daily_deposit.columns = ['Date', 'Bank Deposited']
            daily_deposit['Date'] = daily_deposit['Date'].astype(str)
            
            # Merge to compare side-by-side
            daily_comparison = daily_payment.merge(daily_deposit, on='Date', how='outer').fillna(0)
            daily_comparison['Gap'] = daily_comparison['Payments Reported'] - daily_comparison['Bank Deposited']
            
            # Format for display
            display_comparison = daily_comparison.copy()
            display_comparison['Payments Reported'] = display_comparison['Payments Reported'].apply(format_money)
            display_comparison['Bank Deposited'] = display_comparison['Bank Deposited'].apply(format_money)
            display_comparison['Gap'] = display_comparison['Gap'].apply(format_money)
            
            st.dataframe(display_comparison, width='stretch', hide_index=True)
            st.caption("Daily breakdown: When Uber reported payments vs when they hit your bank")
        else:
            st.dataframe(daily_payment, width='stretch', hide_index=True)
    
    st.divider()
    
    # Processing delay analysis
    st.subheader("⏱️ Payment Processing Delay")
    
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
    st.subheader("✅ Reconciliation Status")
    
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
        st.write("- **BANK_MATCHED**: Payment found in bank deposits ✅")
        st.write("- **REFUND_TRACKED**: Payment includes a refund 🔄")
        st.write("- **OK**: Payment recorded but not yet deposited ⏳")

# ============================================================================
# PAGE: DISPUTE FORENSICS
# ============================================================================

elif page == "🔍 Dispute Forensics":
    st.title("🔍 Dispute Forensics")
    st.write("Investigate problem trips, refunds, and issues • Find Trip IDs for Uber disputes")
    
    st.divider()
    
    # Search functionality
    st.subheader("🔎 Find Problem Trips")
    
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
        st.subheader("📋 Full Details (Click Row to Copy Trip ID)")
        
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
        
        st.caption("📌 Copy the Trip UUID and paste it when contacting Uber support")
        
        st.divider()
        
        # Issue breakdown
        st.subheader("📊 Issue Breakdown")
        
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
        st.subheader("📥 Export Data")
        
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

elif page == "📊 Trends & Forecast":
    st.title("📊 Trends & Forecast")
    st.write("Long-term patterns, seasonality, and what's changing")
    
    st.divider()
    
    # Monthly earnings trend
    st.subheader("📈 Monthly Earnings Trend")
    
    monthly = tx.groupby('Month').agg({
        'Net Earnings': 'sum',
        'Trip UUID': 'count',
        'Tip': 'sum'
    }).reset_index()
    monthly.columns = ['Month', 'Earnings', 'Trips', 'Total Tips']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly['Month'],
        y=monthly['Earnings'],
        name='Earnings',
        marker_color='lightgreen',
        yaxis='y'
    ))
    fig.add_trace(go.Scatter(
        x=monthly['Month'],
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
    st.plotly_chart(fig, width='stretch')
    
    st.divider()
    
    # Key changes
    st.subheader("🔄 What's Changing?")
    
    if len(monthly) >= 2:
        last = monthly.iloc[-1]
        prev = monthly.iloc[-2]
        
        col1, col2, col3 = st.columns(3)
        
        earnings_change = ((last['Earnings'] - prev['Earnings']) / prev['Earnings'] * 100) if prev['Earnings'] > 0 else 0
        trips_change = ((last['Trips'] - prev['Trips']) / prev['Trips'] * 100) if prev['Trips'] > 0 else 0
        tip_change = ((last['Total Tips'] - prev['Total Tips']) / prev['Total Tips'] * 100) if prev['Total Tips'] > 0 else 0
        
        col1.metric("Earnings Change", f"{earnings_change:+.1f}%", delta=format_money(last['Earnings'] - prev['Earnings']))
        col2.metric("Trip Count Change", f"{trips_change:+.1f}%", delta=int(last['Trips'] - prev['Trips']))
        col3.metric("Tips Change", f"{tip_change:+.1f}%", delta=format_money(last['Total Tips'] - prev['Total Tips']))
    
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
        
        st.info(f"""
        Based on your trend:
        - **Next Month ({future_dates[0]})**: {format_money(max(0, future_earnings[0]))}
        - **Month After ({future_dates[1]})**: {format_money(max(0, future_earnings[1]))}
        - **3 Months Out ({future_dates[2]})**: {format_money(max(0, future_earnings[2]))}
        
        (Linear projection - actual results depend on effort and market)
        """)

st.divider()
st.caption("Courier Insights • Purpose-built for courier optimization • Last updated: today")
