"""
Interactive Insights Dashboard - Actionable view of reconciliation issues
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Courier Insights", layout="wide")

# Global helper function for safe file reading
def safe_read(path):
    """Safely read CSV file, return empty DataFrame if missing or error"""
    p = Path(path)
    if p.exists():
        try:
            return pd.read_csv(p)
        except Exception as e:
            st.warning(f"Could not read {path}: {e}")
    return pd.DataFrame()

# Load data
@st.cache_data
def load_insights():
    summary = safe_read('reports/four_way_reconciliation/four_way_summary.csv')
    daily = safe_read('reports/four_way_reconciliation/daily_reconciliation_3way.csv')
    refunds = safe_read('reports/four_way_reconciliation/refund_verification_status.csv')
    audit = safe_read('reports/audit_trail/complete_audit_trail.csv')
    transactions = safe_read('reports/monthly_comprehensive/all_transactions_detailed.csv')
    bank_refunds_enriched = safe_read('bank/bank_refund_status_enriched.csv')
    multi_account = safe_read('reports/four_way_reconciliation/multi_account_reconciliation.csv')

    # Parse known datetime columns when present
    if 'Date' in daily.columns:
        daily['Date'] = pd.to_datetime(daily['Date'], errors='coerce')
    if 'Date' in refunds.columns:
        refunds['Date'] = pd.to_datetime(refunds['Date'], errors='coerce')
    if 'Trip drop off time' in audit.columns:
        audit['Trip drop off time'] = pd.to_datetime(audit['Trip drop off time'], errors='coerce')
    if 'Trip drop off time' in transactions.columns:
        transactions['Trip drop off time'] = pd.to_datetime(transactions['Trip drop off time'], errors='coerce')
    if 'Trip drop off time' in bank_refunds_enriched.columns:
        bank_refunds_enriched['Trip drop off time'] = pd.to_datetime(bank_refunds_enriched['Trip drop off time'], errors='coerce')
    if 'Date' in bank_refunds_enriched.columns:
        bank_refunds_enriched['Date'] = pd.to_datetime(bank_refunds_enriched['Date'], errors='coerce')

    return summary, daily, refunds, audit, transactions, bank_refunds_enriched, multi_account

summary, daily, refunds, audit, transactions, bank_refunds_enriched, multi_account = load_insights()

# Helpers for robust metrics and schemas
def _to_float(val, default=0.0):
    try:
        if pd.isna(val):
            return float(default)
        if isinstance(val, str):
            return float(val.replace('$', '').replace(',', '').strip())
        return float(val)
    except Exception:
        return float(default)

def get_summary_metric(df: pd.DataFrame, metric_name: str, default=0.0):
    if df.empty:
        return float(default)
    if 'Metric' in df.columns and 'Value' in df.columns:
        row = df.loc[df['Metric'] == metric_name, 'Value']
        if len(row) > 0:
            return _to_float(row.values[0], default)
    return float(default)

def ensure_daily_columns(daily_df: pd.DataFrame):
    if daily_df.empty:
        return daily_df
    # Ensure core numeric columns
    for col in ['Net Earnings', 'Bank Total']:
        if col in daily_df.columns:
            daily_df[col] = pd.to_numeric(daily_df[col], errors='coerce').fillna(0.0)
    # Compute Abs Difference if missing
    if 'Abs Difference' not in daily_df.columns and all(c in daily_df.columns for c in ['Net Earnings', 'Bank Total']):
        daily_df['Abs Difference'] = (daily_df['Net Earnings'] - daily_df['Bank Total']).abs()
    # Parse Date
    if 'Date' in daily_df.columns:
        daily_df['Date'] = pd.to_datetime(daily_df['Date'], errors='coerce')
    return daily_df

def ensure_refund_columns(refunds_df: pd.DataFrame):
    if refunds_df.empty:
        return refunds_df
    # Standardize Checked
    if 'Checked' not in refunds_df.columns:
        if 'Refund Verification Match' in refunds_df.columns:
            refunds_df['Checked'] = refunds_df['Refund Verification Match']
        else:
            refunds_df['Checked'] = ''
    # Standardize amounts
    amount_cols = ['Refund Amount', 'Refund']
    present_amount = next((c for c in amount_cols if c in refunds_df.columns), None)
    if present_amount is None:
        refunds_df['Refund Amount'] = 0.0
    else:
        refunds_df['Refund Amount'] = pd.to_numeric(refunds_df[present_amount], errors='coerce').fillna(0.0)
    if 'Payment Refund' in refunds_df.columns:
        refunds_df['Payment Refund'] = pd.to_numeric(refunds_df['Payment Refund'], errors='coerce').fillna(0.0)
    else:
        refunds_df['Payment Refund'] = 0.0
    # Date
    if 'Date' in refunds_df.columns:
        refunds_df['Date'] = pd.to_datetime(refunds_df['Date'], errors='coerce')
    return refunds_df

def ensure_transactions_columns(tx_df: pd.DataFrame):
    if tx_df.empty:
        return tx_df
    # Time
    if 'Trip drop off time' in tx_df.columns:
        tx_df['Trip drop off time'] = pd.to_datetime(tx_df['Trip drop off time'], errors='coerce')
    # Numeric components
    for col in ['Net Earnings', 'Fare', 'Tip', 'Refund', 'Incentive', 'Boost', 'Instant Pay Fees']:
        if col in tx_df.columns:
            tx_df[col] = pd.to_numeric(tx_df[col], errors='coerce').fillna(0.0)
        else:
            tx_df[col] = 0.0
    # If Net Earnings missing, compute from components
    if 'Net Earnings' in tx_df.columns and (tx_df['Net Earnings'] == 0).all():
        tx_df['Net Earnings'] = (
            tx_df.get('Fare', 0) + tx_df.get('Tip', 0) + tx_df.get('Refund', 0)
            + tx_df.get('Incentive', 0) + tx_df.get('Boost', 0) - tx_df.get('Instant Pay Fees', 0)
        )
    # Status default
    if 'Status' not in tx_df.columns:
        tx_df['Status'] = 'Unknown'
    return tx_df

# Normalize dataframes
daily = ensure_daily_columns(daily)
refunds = ensure_refund_columns(refunds)
transactions = ensure_transactions_columns(transactions)

# Build daily fallbacks from transactions when needed
def build_daily_from_transactions(daily_df: pd.DataFrame, tx_df: pd.DataFrame):
    daily_out = daily_df.copy()
    # Ensure Date column exists in daily
    if 'Date' not in daily_out.columns:
        daily_out['Date'] = pd.NaT
    # If Net Earnings missing or empty, compute from transactions per day
    needs_net = ('Net Earnings' not in daily_out.columns) or daily_out['Net Earnings'].isna().all() or (daily_out['Net Earnings'] == 0).all()
    if needs_net and not tx_df.empty and 'Trip drop off time' in tx_df.columns:
        tx = tx_df[['Trip drop off time', 'Net Earnings']].dropna()
        tx['Date'] = tx['Trip drop off time'].dt.date
        tx_daily = tx.groupby('Date')['Net Earnings'].sum().reset_index()
        tx_daily['Date'] = pd.to_datetime(tx_daily['Date'], errors='coerce')
        if daily_out.empty:
            daily_out = tx_daily.rename(columns={'Net Earnings': 'Net Earnings'})
        else:
            daily_out = pd.merge(daily_out, tx_daily, on='Date', how='left', suffixes=('', '_tx'))
            if 'Net Earnings' not in daily_out.columns and 'Net Earnings_tx' in daily_out.columns:
                daily_out['Net Earnings'] = daily_out['Net Earnings_tx']
            elif 'Net Earnings_tx' in daily_out.columns:
                # Fill missing values from tx
                daily_out['Net Earnings'] = daily_out['Net Earnings'].fillna(daily_out['Net Earnings_tx'])
            if 'Net Earnings_tx' in daily_out.columns:
                daily_out.drop(columns=['Net Earnings_tx'], inplace=True)
    # Ensure Bank Total exists
    if 'Bank Total' not in daily_out.columns:
        daily_out['Bank Total'] = 0.0
    # Recompute Abs Difference if possible
    if all(c in daily_out.columns for c in ['Net Earnings', 'Bank Total']):
        daily_out['Abs Difference'] = (pd.to_numeric(daily_out['Net Earnings'], errors='coerce').fillna(0.0) -
                                       pd.to_numeric(daily_out['Bank Total'], errors='coerce').fillna(0.0)).abs()
    return daily_out

daily = build_daily_from_transactions(daily, transactions)

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'overview'
if 'selected_trip' not in st.session_state:
    st.session_state.selected_trip = None
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = None

# Navigation
def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()

def select_trip(trip_uuid):
    st.session_state.selected_trip = trip_uuid
    st.session_state.page = 'trip_detail'
    st.rerun()

def select_date(date):
    st.session_state.selected_date = date
    st.session_state.page = 'daily_detail'
    st.rerun()

# Sidebar navigation
with st.sidebar:
    st.title("📊 Navigation")
    if st.button("🏠 Overview", width='stretch'):
        go_to_page('overview')
    if st.button("📅 Daily Analysis", width='stretch'):
        go_to_page('daily')
    if st.button("🚗 Trip Explorer", width='stretch'):
        go_to_page('trips')
    if st.button("💰 Refund Tracker", width='stretch'):
        go_to_page('refunds')
    if st.button("📊 Analytics", width='stretch'):
        go_to_page('analytics')
    
    st.markdown("---")
    st.caption("Run `python process_new_month.py` to update")

# =============== OVERVIEW PAGE ===============
if st.session_state.page == 'overview':
    st.title("🏠 Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Metrics with fallbacks
    fallback_net = transactions['Net Earnings'].sum() if not transactions.empty else 0.0
    net_earnings = get_summary_metric(summary, 'Net Earnings', default=fallback_net)
    fallback_bank = daily['Bank Total'].sum() if 'Bank Total' in daily.columns else 0.0
    bank_total = get_summary_metric(summary, 'Total Bank Deposits', default=fallback_bank)
    pending = max(net_earnings - bank_total, 0.0)
    unchecked_refunds = len(refunds[refunds['Checked'] != 'Match']) if 'Checked' in refunds.columns else 0
    
    col1.metric("💵 Net Earnings", f"${net_earnings:,.2f}")
    col2.metric("🏦 Bank Deposits", f"${bank_total:,.2f}")
    col3.metric("⏳ Pending", f"${pending:,.2f}", delta=f"{(pending/net_earnings*100):.1f}%")
    col4.metric("⚠️ Unchecked Refunds", unchecked_refunds, 
                delta="Needs Review" if unchecked_refunds > 0 else "All Clear",
                delta_color="inverse")
    
    st.markdown("---")
    
    # Quick action cards
    st.subheader("🎯 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        large_gaps = daily[daily['Abs Difference'] > 100] if 'Abs Difference' in daily.columns else pd.DataFrame()
        st.metric("Large Discrepancies (>$100)", len(large_gaps))
        if st.button("📊 View Details", key="large_gaps"):
            go_to_page('daily')
    
    with col2:
        recent_trips = transactions.tail(20)
        st.metric("Recent Trips", len(transactions))
        if st.button("🚗 Explore Trips", key="explore_trips"):
            go_to_page('trips')
    
    with col3:
        refund_issues = refunds[refunds['Checked'] != 'Match'] if 'Checked' in refunds.columns else pd.DataFrame()
        st.metric("Refunds Needing Review", len(refund_issues))
        if st.button("💰 Review Refunds", key="review_refunds"):
            go_to_page('refunds')
    
    st.markdown("---")
    
    # Timeline visualization
    st.subheader("📈 Earnings Timeline")
    daily_sorted = daily.sort_values('Date') if 'Date' in daily.columns else daily
    
    if 'Net Earnings' in daily_sorted.columns or 'Bank Total' in daily_sorted.columns:
        fig = go.Figure()
        if 'Net Earnings' in daily_sorted.columns:
            fig.add_trace(go.Scatter(
                x=daily_sorted['Date'], 
                y=daily_sorted['Net Earnings'],
                mode='lines+markers',
                name='Net Earnings',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=6)
            ))
        if 'Bank Total' in daily_sorted.columns:
            fig.add_trace(go.Scatter(
                x=daily_sorted['Date'], 
                y=daily_sorted['Bank Total'],
                mode='lines+markers',
                name='Bank Deposits',
                line=dict(color='#2ca02c', width=2),
                marker=dict(size=6)
            ))
        fig.update_layout(
            hovermode='x unified',
            height=400,
            xaxis_title="Date",
            yaxis_title="Amount ($)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("Insufficient daily data to render timeline.")
    
    # Monthly breakdown
    st.subheader("📅 Monthly Summary")
    transactions['Month'] = transactions['Trip drop off time'].dt.to_period('M').astype(str)
    monthly = transactions.groupby('Month').agg({
        'Trip UUID': 'count',
        'Net Earnings': 'sum'
    }).reset_index()
    monthly.columns = ['Month', 'Trip Count', 'Net Earnings']
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(monthly, x='Month', y='Trip Count', 
                     title="Trips per Month",
                     color='Trip Count',
                     color_continuous_scale='Blues')
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        fig = px.bar(monthly, x='Month', y='Net Earnings', 
                     title="Earnings per Month",
                     color='Net Earnings',
                     color_continuous_scale='Greens')
        st.plotly_chart(fig, width='stretch')

# =============== DAILY ANALYSIS PAGE ===============
elif st.session_state.page == 'daily':
    st.title("📅 Daily Analysis")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        min_gap = st.number_input("Min Gap ($)", min_value=0, value=0, step=10)
    with col2:
        # Safe date range default
        if 'Date' in daily.columns and daily['Date'].notna().any():
            min_date = daily['Date'].min().date()
            max_date = daily['Date'].max().date()
            date_range = st.date_input("Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
        else:
            date_range = []
    with col3:
        sort_by = st.selectbox("Sort by", ["Date", "Abs Difference", "Net Earnings"])
    
    # Filter data
    base = daily.copy()
    if 'Abs Difference' not in base.columns and all(c in base.columns for c in ['Net Earnings', 'Bank Total']):
        base['Abs Difference'] = (base['Net Earnings'] - base['Bank Total']).abs()
    filtered = base[base['Abs Difference'] >= min_gap].copy() if 'Abs Difference' in base.columns else base.copy()
    if len(date_range) == 2:
        filtered = filtered[(filtered['Date'].dt.date >= date_range[0]) & 
                           (filtered['Date'].dt.date <= date_range[1])]
    
    filtered = filtered.sort_values(sort_by, ascending=(sort_by == 'Date'))
    
    st.metric("Days Shown", len(filtered), f"out of {len(daily)} total")
    
    # Visualization
    fig = px.scatter(filtered, x='Date', y='Abs Difference', 
                    size='Abs Difference',
                    color='Abs Difference',
                    hover_data=['Net Earnings', 'Bank Total'],
                    title=f"Daily Discrepancies (>= ${min_gap})",
                    color_continuous_scale='Reds')
    st.plotly_chart(fig, width='stretch')
    
    # Interactive table
    st.subheader("📋 Daily Details (Click for trip breakdown)")
    
    display_df = filtered[['Date', 'Net Earnings', 'Bank Total', 'Abs Difference']].copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
    display_df['Net Earnings'] = display_df['Net Earnings'].apply(lambda x: f"${x:,.2f}")
    display_df['Bank Total'] = display_df['Bank Total'].apply(lambda x: f"${x:,.2f}")
    display_df['Abs Difference'] = display_df['Abs Difference'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(display_df, width='stretch', height=400)

    # Manual selection of a date to drill down
    st.write("Select a date to view its trips:")
    selectable_dates = sorted(display_df['Date'].unique()) if not display_df.empty else []
    selected_date = st.selectbox("Daily Date", options=selectable_dates) if selectable_dates else None
    if selected_date and 'Trip drop off time' in transactions.columns:
        selected_dt = pd.to_datetime(selected_date).date()
        day_trips = transactions[transactions['Trip drop off time'].dt.date == selected_dt]
        if not day_trips.empty:
            st.subheader(f"🚗 Trips on {selected_date}")
            cols = [c for c in ['Trip drop off time', 'Net Earnings', 'Status', 'Reconciliation Status'] if c in day_trips.columns]
            st.dataframe(day_trips[cols], width='stretch')

# =============== TRIP EXPLORER PAGE ===============
elif st.session_state.page == 'trips':
    st.title("🚗 Trip Explorer")
    
    # Search and filters
    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("🔍 Search Trip UUID", "")
    with col2:
        status_filter = st.multiselect(
            "Status",
            options=transactions['Status'].unique(),
            default=transactions['Status'].unique()
        )
    with col3:
        recon_filter = st.multiselect(
            "Reconciliation Status",
            options=audit['Reconciliation Status'].unique(),
            default=audit['Reconciliation Status'].unique()
        )
    
    col1, col2 = st.columns(2)
    with col1:
        min_earnings = st.slider("Min Net Earnings", 0, int(transactions['Net Earnings'].max()), 0)
    with col2:
        sort_trips = st.selectbox("Sort by", ["Trip drop off time", "Net Earnings", "Status"])
    
    # Filter trips
    filtered_trips = transactions.copy()
    if search:
        filtered_trips = filtered_trips[filtered_trips['Trip UUID'].str.contains(search, case=False, na=False)]
    filtered_trips = filtered_trips[filtered_trips['Status'].isin(status_filter)]
    filtered_trips = filtered_trips[filtered_trips['Net Earnings'] >= min_earnings]
    
    # Merge with reconciliation status
    if not audit.empty and 'Trip UUID' in audit.columns and 'Reconciliation Status' in audit.columns:
        filtered_trips = filtered_trips.merge(
            audit[['Trip UUID', 'Reconciliation Status']], 
            on='Trip UUID', 
            how='left',
            suffixes=('', '_audit')
        )
    else:
        if 'Reconciliation Status' not in filtered_trips.columns:
            filtered_trips['Reconciliation Status'] = 'Unknown'
    filtered_trips = filtered_trips[filtered_trips['Reconciliation Status'].isin(recon_filter)]
    filtered_trips = filtered_trips.sort_values(sort_trips, ascending=False)
    
    st.metric("Trips Found", len(filtered_trips), f"out of {len(transactions)} total")
    
    # Trip cards with click actions
    st.subheader("📋 Trip List")
    
    for idx, trip in filtered_trips.head(50).iterrows():
        with st.expander(
            f"🚗 {trip['Trip drop off time'].strftime('%Y-%m-%d %H:%M')} - ${trip['Net Earnings']:.2f} - {trip['Reconciliation Status']}"
        ):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Trip Details**")
                st.write(f"UUID: `{trip['Trip UUID'][:16]}...`")
                st.write(f"Status: {trip['Status']}")
                st.write(f"Time: {trip['Trip drop off time']}")
            
            with col2:
                st.write("**Earnings Breakdown**")
                st.write(f"Fare: ${trip.get('Fare', 0):.2f}")
                st.write(f"Tip: ${trip.get('Tip', 0):.2f}")
                st.write(f"Net: ${trip['Net Earnings']:.2f}")
            
            with col3:
                st.write("**Reconciliation**")
                st.write(f"Status: {trip['Reconciliation Status']}")
                if trip.get('Refund', 0) != 0:
                    st.write(f"⚠️ Refund: ${trip['Refund']:.2f}")
                
                if st.button("📊 View Full Details", key=f"trip_{trip['Trip UUID']}"):
                    select_trip(trip['Trip UUID'])
    
    if len(filtered_trips) > 50:
        st.info(f"Showing first 50 of {len(filtered_trips)} trips. Narrow filters to see more.")

# =============== TRIP DETAIL PAGE ===============
elif st.session_state.page == 'trip_detail':
    if st.button("⬅️ Back to Trips"):
        go_to_page('trips')
    
    trip_uuid = st.session_state.selected_trip
    trip_rows = transactions[transactions['Trip UUID'] == trip_uuid]
    if trip_rows.empty:
        st.error("Trip not found in transactions")
        st.button("⬅️ Back to Trips")
        st.stop()
    trip_data = trip_rows.iloc[0]
    audit_data = audit[audit['Trip UUID'] == trip_uuid] if 'Trip UUID' in audit.columns else pd.DataFrame()
    
    st.title(f"🚗 Trip Details")
    st.caption(f"UUID: {trip_uuid}")
    
    # Overview
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Net Earnings", f"${trip_data['Net Earnings']:.2f}")
    col2.metric("Status", audit_data['Reconciliation Status'].iloc[0] if not audit_data.empty else "Unknown")
    col3.metric("Reconciliation", audit_data['Reconciliation Status'].iloc[0] if not audit_data.empty else "Unknown")
    col4.metric("Time", trip_data['Trip drop off time'].strftime('%Y-%m-%d %H:%M'))
    
    st.markdown("---")
    
    # Detailed breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Payment Breakdown")
        payment_data = {
            'Component': ['Fare', 'Tip', 'Refund', 'Incentive', 'Boost', 'Instant Pay Fees'],
            'Amount': [
                trip_data.get('Fare', 0),
                trip_data.get('Tip', 0),
                trip_data.get('Refund', 0),
                trip_data.get('Incentive', 0),
                trip_data.get('Boost', 0),
                -trip_data.get('Instant Pay Fees', 0)
            ]
        }
        payment_df = pd.DataFrame(payment_data)
        payment_df = payment_df[payment_df['Amount'] != 0]
        
        fig = px.bar(payment_df, x='Component', y='Amount', 
                     color='Amount',
                     color_continuous_scale=['red', 'yellow', 'green'],
                     title="Payment Components")
        st.plotly_chart(fig, width='stretch')
        
        st.dataframe(payment_df, width='stretch', hide_index=True)
    
    with col2:
        st.subheader("📋 Audit Trail")
        if not audit_data.empty:
            audit_info = audit_data.iloc[0]
            st.write(f"**Reconciliation Status:** {audit_info.get('Reconciliation Status', 'Unknown')}")
            
            if pd.notna(audit_info.get('Bank Deposit Date')):
                st.success(f"✓ Bank deposit on {audit_info['Bank Deposit Date']}")
            
            if pd.notna(audit_info.get('Receipt Refund Amount')) and audit_info['Receipt Refund Amount'] > 0:
                st.warning(f"⚠️ Refund: ${audit_info.get('Receipt Refund Amount', 0):.2f}")
            
            # Full audit details
            with st.expander("View Full Audit Data"):
                st.json(audit_info.to_dict())
        else:
            st.warning("No audit data found for this trip")

# =============== REFUND TRACKER PAGE ===============
elif st.session_state.page == 'refunds':
    st.title("💰 Refund Tracker")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        checked_filter = st.radio("Filter", ["All", "Unchecked Only", "Checked Only"])
    with col2:
        sort_options = [opt for opt in ["Date", "Refund Amount"] if opt in refunds.columns]
        date_sort = st.selectbox("Sort by", sort_options) if sort_options else None
    
    # Filter refunds
    filtered_refunds = refunds.copy()
    if checked_filter == "Unchecked Only":
        filtered_refunds = filtered_refunds[filtered_refunds['Checked'] != 'Match'] if 'Checked' in filtered_refunds.columns else filtered_refunds
    elif checked_filter == "Checked Only":
        filtered_refunds = filtered_refunds[filtered_refunds['Checked'] == 'Match'] if 'Checked' in filtered_refunds.columns else filtered_refunds
    
    if date_sort:
        filtered_refunds = filtered_refunds.sort_values(date_sort, ascending=False)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Refunds", len(refunds))
    if 'Checked' in refunds.columns:
        col2.metric("Unchecked", len(refunds[refunds['Checked'] != 'Match']))
    else:
        col2.metric("Unchecked", 0)
    if 'Refund Amount' in refunds.columns:
        col3.metric("Total Amount", f"${refunds['Refund Amount'].sum():.2f}")
    else:
        col3.metric("Total Amount", "$0.00")
    if not bank_refunds_enriched.empty:
        unmatched_bank = bank_refunds_enriched['Trip UUID'].isna().sum() if 'Trip UUID' in bank_refunds_enriched.columns else 0
        col4.metric("Bank Unmatched", unmatched_bank)
    else:
        col4.metric("Bank Unmatched", 0)
    
    # Visualization
    viz_cols = st.columns(2)
    with viz_cols[0]:
        if 'Checked' in refunds.columns and 'Refund Amount' in refunds.columns:
            refund_status = refunds.groupby('Checked')['Refund Amount'].sum().reset_index()
            fig = px.pie(refund_status, values='Refund Amount', names='Checked',
                         title="Refund Status Breakdown",
                         color_discrete_sequence=['#ff7f0e', '#2ca02c'])
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Refund data incomplete for visualization.")
    with viz_cols[1]:
        if not bank_refunds_enriched.empty and 'match_level' in bank_refunds_enriched.columns:
            lvl = bank_refunds_enriched.copy()
            lvl['match_level'] = lvl['match_level'].fillna('unmatched')
            match_counts = lvl.groupby('match_level')['Refund Amount'].sum().reset_index()
            fig = px.pie(match_counts, values='Refund Amount', names='match_level',
                         title="Bank Refund Match Levels")
            st.plotly_chart(fig, width='stretch')
        elif not bank_refunds_enriched.empty:
            st.info("Bank refund enrichment loaded, but match levels missing.")
        else:
            st.caption("Bank refund enrichment not loaded.")
    
    # Interactive refund list
    st.subheader(f"📋 Refund Details ({len(filtered_refunds)} items)")
    if not bank_refunds_enriched.empty:
        st.caption("Bank refund matches include Trip UUID/time when available")
    
    for idx, refund in filtered_refunds.iterrows():
        status_val = refund['Checked'] if 'Checked' in filtered_refunds.columns else ''
        status_icon = "✅" if status_val == 'Match' else "⚠️"
        date_str = refund['Date'].strftime('%Y-%m-%d') if 'Date' in filtered_refunds.columns and pd.notna(refund['Date']) else 'Unknown Date'
        amount_val = f"${refund['Refund Amount']:.2f}" if 'Refund Amount' in filtered_refunds.columns else "$0.00"
        with st.expander(f"{status_icon} {date_str} - {amount_val} - {status_val}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Refund Information**")
                if 'Date' in filtered_refunds.columns:
                    st.write(f"Date: {refund['Date']}")
                if 'Refund Amount' in filtered_refunds.columns:
                    st.write(f"Amount: ${refund['Refund Amount']:.2f}")
                if 'Checked' in filtered_refunds.columns:
                    st.write(f"Status: {status_val}")
                
                if pd.notna(refund.get('Pickup Address')):
                    st.write(f"Pickup: {refund['Pickup Address']}")
                if pd.notna(refund.get('Trip UUID')):
                    st.write(f"Trip UUID: {refund['Trip UUID']}")
                if 'Trip drop off time' in refund and pd.notna(refund.get('Trip drop off time')):
                    st.write(f"Trip Time: {refund['Trip drop off time']}")
            
            with col2:
                st.write("**Payment Match**")
                pay_val = refund.get('Payment Refund', 0)
                st.write(f"Payment Amount: ${pay_val:.2f}")
                if 'Refund Amount' in filtered_refunds.columns:
                    difference = refund['Refund Amount'] - pay_val
                    if abs(difference) > 0.01:
                        st.error(f"⚠️ Difference: ${difference:.2f}")
                    else:
                        st.success("✓ Amounts match")

# =============== ANALYTICS PAGE ===============
elif st.session_state.page == 'analytics':
    st.title("📊 Advanced Analytics")
    
    # Time-based analysis
    st.subheader("📈 Performance Trends")
    
    if 'Trip drop off time' in transactions.columns:
        transactions['Date'] = transactions['Trip drop off time'].dt.date
        transactions['Hour'] = transactions['Trip drop off time'].dt.hour
        transactions['DayOfWeek'] = transactions['Trip drop off time'].dt.day_name()
    else:
        transactions['Date'] = pd.NaT
        transactions['Hour'] = 0
        transactions['DayOfWeek'] = 'Unknown'
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Hourly distribution
        hourly = transactions.groupby('Hour').agg({
            'Trip UUID': 'count',
            'Net Earnings': 'mean'
        }).reset_index()
        hourly.columns = ['Hour', 'Trip Count', 'Avg Earnings']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hourly['Hour'],
            y=hourly['Trip Count'],
            name='Trip Count',
            yaxis='y',
            marker_color='lightblue'
        ))
        fig.add_trace(go.Scatter(
            x=hourly['Hour'],
            y=hourly['Avg Earnings'],
            name='Avg Earnings',
            yaxis='y2',
            line=dict(color='red', width=2)
        ))
        fig.update_layout(
            title="Trips by Hour of Day",
            xaxis=dict(title="Hour"),
            yaxis=dict(title="Trip Count"),
            yaxis2=dict(title="Avg Earnings ($)", overlaying='y', side='right'),
            hovermode='x unified'
        )
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Day of week analysis
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_stats = transactions.groupby('DayOfWeek').agg({
            'Trip UUID': 'count',
            'Net Earnings': 'sum'
        }).reindex(dow_order).reset_index()
        daily_stats.columns = ['Day', 'Trip Count', 'Total Earnings']
        
        fig = px.bar(daily_stats, x='Day', y='Total Earnings',
                     color='Trip Count',
                     title="Earnings by Day of Week",
                     color_continuous_scale='Greens')
        st.plotly_chart(fig, width='stretch')
    
    # Performance metrics
    st.subheader("🎯 Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Trip Earnings", f"${transactions['Net Earnings'].mean():.2f}")
    col2.metric("Median Trip Earnings", f"${transactions['Net Earnings'].median():.2f}")
    col3.metric("Max Single Trip", f"${transactions['Net Earnings'].max():.2f}")
    col4.metric("Total Trips", len(transactions))
    
    # Earnings distribution
    st.subheader("💵 Earnings Distribution")
    
    fig = px.histogram(transactions, x='Net Earnings', 
                       nbins=50,
                       title="Trip Earnings Distribution",
                       color_discrete_sequence=['#1f77b4'])
    fig.update_layout(
        xaxis_title="Net Earnings ($)",
        yaxis_title="Number of Trips",
        showlegend=False
    )
    st.plotly_chart(fig, width='stretch')
    
    # Bank unmatched quick view
    if not bank_refunds_enriched.empty:
        unmatched_rows = bank_refunds_enriched[bank_refunds_enriched['Trip UUID'].isna()] if 'Trip UUID' in bank_refunds_enriched.columns else pd.DataFrame()
        if not unmatched_rows.empty:
            st.markdown("---")
            st.subheader(f"⚠️ Bank Refunds Without UUID ({len(unmatched_rows)})")
            st.dataframe(unmatched_rows[['Date','Refund Amount','Pickup Address','match_level']].head(20), width='stretch')
            if len(unmatched_rows) > 20:
                st.caption("Showing first 20; download for full list.")

    # Export options
    st.markdown("---")
    st.subheader("📥 Export Data")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.download_button(
            "Download Complete Audit Trail",
            audit.to_csv(index=False),
            "audit_trail.csv",
            "text/csv"
        )
    with col2:
        st.download_button(
            "Download Daily Reconciliation",
            daily.to_csv(index=False),
            "daily_reconciliation.csv",
            "text/csv"
        )
    with col3:
        st.download_button(
            "Download Refund Status",
            refunds.to_csv(index=False),
            "refund_status.csv",
            "text/csv"
        )
    with col4:
        if not bank_refunds_enriched.empty:
            st.download_button(
                "Download Bank Refunds Enriched",
                bank_refunds_enriched.to_csv(index=False),
                "bank_refund_status_enriched.csv",
                "text/csv"
            )
        else:
            st.caption("Bank refund enrichment not available")

# Key metrics - Using multi-account reconciliation for accuracy
multi_account = safe_read('reports/four_way_reconciliation/multi_account_reconciliation.csv')

col1, col2, col3, col4 = st.columns(4)

# Get values from multi-account reconciliation (most accurate)
if not multi_account.empty:
    net_earnings = get_summary_metric(multi_account, 'Payments (Uber Records)', default=get_summary_metric(summary, 'Payments (Net Earnings) Total'))
    bank_total = get_summary_metric(multi_account, 'Total Deposits Received', default=get_summary_metric(summary, 'Total Bank Deposits (All)'))
    difference = get_summary_metric(multi_account, 'Final Unaccounted Gap', default=get_summary_metric(summary, 'Final Difference (Payments - Total)'))
else:
    net_earnings = get_summary_metric(summary, 'Payments (Net Earnings) Total')
    bank_total = get_summary_metric(summary, 'Total Bank Deposits (All)')
    difference = get_summary_metric(summary, 'Final Difference (Payments - Total)')

unchecked = get_summary_metric(summary, 'Unchecked Refunds', default=0)

col1.metric("Net Earnings", f"${net_earnings:,.2f}", help="Total earnings from completed trips")
col2.metric("Bank Deposits", f"${bank_total:,.2f}", help="Total actual deposits (all accounts)")
col3.metric("Final Gap", f"${difference:,.2f}", help="Difference after accounting for all deposits")
col4.metric("Unchecked Refunds", int(unchecked), help="Refunds not marked as paid")

# Action items
st.markdown("---")
st.subheader("⚠️ Action Items")

action_tabs = st.tabs(["Unchecked Refunds", "Large Discrepancies", "Daily Mismatches"])

with action_tabs[0]:
    unchecked_refunds = refunds[refunds['Paid'].isna()].copy()
    if len(unchecked_refunds) > 0:
        st.warning(f"{len(unchecked_refunds)} refunds need verification")
        st.dataframe(
            unchecked_refunds[['Date', 'Refund', 'Pickup Address']],
            use_container_width=True
        )
    else:
        st.success("All refunds verified")

with action_tabs[1]:
    daily['Date'] = pd.to_datetime(daily['Date'])
    daily['Abs Difference'] = daily['Difference'].abs()
    large_gaps = daily[daily['Abs Difference'] > 100].sort_values('Abs Difference', ascending=False)
    
    if len(large_gaps) > 0:
        st.warning(f"{len(large_gaps)} days with >$100 payment/bank difference")
        st.dataframe(
            large_gaps[['Date', 'Trips', 'Payment Total (Net)', 'Bank Total', 'Difference']].head(10),
            use_container_width=True
        )
        
        # Chart
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=large_gaps['Date'], y=large_gaps['Difference'], mode='markers', marker=dict(size=10, color='red')))
        fig.update_layout(title='Large Payment/Bank Discrepancies', xaxis_title='Date', yaxis_title='Difference ($)', height=300)
        st.plotly_chart(fig, width='stretch')
    else:
        st.success("No large discrepancies detected")

with action_tabs[2]:
    mismatches = daily[daily['Status'] == 'MISMATCH'].copy()
    st.info(f"{len(mismatches)}/{len(daily)} days have payment/bank timing differences")
    
    # Quick stats
    avg_diff = mismatches['Difference'].mean()
    st.metric("Average Daily Difference", f"${avg_diff:,.2f}")

# Quick export
st.markdown("---")
st.subheader("📥 Export Reports")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Download Audit Trail"):
        st.download_button(
            "Download CSV",
            audit.to_csv(index=False),
            "audit_trail.csv",
            "text/csv"
        )

with col2:
    if st.button("Download Daily Reconciliation"):
        st.download_button(
            "Download CSV",
            daily.to_csv(index=False),
            "daily_reconciliation.csv",
            "text/csv"
        )

with col3:
    if st.button("Download Refund Status"):
        st.download_button(
            "Download CSV",
            refunds.to_csv(index=False),
            "refund_status.csv",
            "text/csv"
        )

st.caption("Run `python process_new_month.py` to regenerate reports with new data")
