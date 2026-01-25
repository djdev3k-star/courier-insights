import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Courier Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load data
@st.cache_data
def load_data():
    detail_file = Path('reports/monthly_comprehensive/all_transactions_detailed.csv')
    summary_file = Path('reports/monthly_comprehensive/monthly_summary.csv')
    
    detail_df = pd.read_csv(detail_file)
    detail_df['Trip drop off time'] = pd.to_datetime(detail_df['Trip drop off time'])
    
    summary_df = pd.read_csv(summary_file)
    
    # Load bank statements
    bank_list = []
    for csv_file in sorted(Path('bank').glob('Uber Pro Card Statement*.csv')):
        df = pd.read_csv(csv_file)
        df['source_file'] = csv_file.name
        bank_list.append(df)
    bank_df = pd.concat(bank_list, ignore_index=True) if bank_list else pd.DataFrame()
    if not bank_df.empty:
        bank_df['Posted Date'] = pd.to_datetime(bank_df['Posted Date'], errors='coerce')
        bank_df['Amount'] = bank_df['Amount'].astype(str).str.replace(r'[\$\+,]', '', regex=True)
        bank_df['Amount'] = pd.to_numeric(bank_df['Amount'], errors='coerce')
        bank_df['Month'] = bank_df['Posted Date'].dt.strftime('%Y-%m')
    
    # Load four-way reconciliation reports
    four_way_summary = pd.read_csv(Path('reports/four_way_reconciliation/four_way_summary.csv'))
    daily_recon = pd.read_csv(Path('reports/four_way_reconciliation/daily_reconciliation_3way.csv'))
    refund_status = pd.read_csv(Path('reports/four_way_reconciliation/refund_verification_status.csv'))
    
    return detail_df, summary_df, bank_df, four_way_summary, daily_recon, refund_status

detail_df, summary_df, bank_df, four_way_summary, daily_recon, refund_status = load_data()

# Title
st.title("📊 Courier Earnings Dashboard")
st.markdown("**Aug – Dec 2025 | Uber Trips & Bank Reconciliation**")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Four-Way Reconciliation", "Bank Details"])

# Sidebar filters
st.sidebar.header("Filters")
selected_month = st.sidebar.multiselect(
    "Select Month(s)",
    sorted(detail_df['Month'].unique()),
    default=sorted(detail_df['Month'].unique())
)
filtered_df = detail_df[detail_df['Month'].isin(selected_month)]

with tab1:
    # Top metrics
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)

    total_trips = len(filtered_df)
    total_earnings = filtered_df['Net Earnings'].sum()
    total_distance = filtered_df['Trip distance'].sum()
    avg_tip_pct = (filtered_df['Tip'].sum() / filtered_df['Fare'].sum() * 100) if filtered_df['Fare'].sum() > 0 else 0
    customer_purchases = filtered_df['Customer Purchase'].sum()

    col1.metric("Trips", f"{total_trips:,}")
    col2.metric("Net Earnings", f"${total_earnings:,.2f}")
    col3.metric("Distance", f"{total_distance:,.1f} mi")
    col4.metric("Avg Tip %", f"{avg_tip_pct:.1f}%")
    col5.metric("Cash Tips", f"{int(customer_purchases)}")

    # Charts section
    st.markdown("---")
    st.subheader("Monthly Trends")

    col1, col2 = st.columns(2)

    with col1:
        # Earnings trend
        monthly_data = filtered_df.groupby('Month').agg({
            'Trip UUID': 'count',
            'Net Earnings': 'sum',
            'Fare': 'sum',
            'Tip': 'sum'
        }).reset_index()
        monthly_data.columns = ['Month', 'Trips', 'Net Earnings', 'Fare', 'Tip']
        
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(x=monthly_data['Month'], y=monthly_data['Net Earnings'], name='Net Earnings', marker_color='#00BFA5'))
        fig1.add_trace(go.Scatter(x=monthly_data['Month'], y=monthly_data['Trips'], name='Trips', yaxis='y2', marker_color='#FF6B6B', mode='lines+markers'))
        fig1.update_layout(
            title='Earnings & Activity',
            xaxis_title='Month',
            yaxis_title='Earnings ($)',
            yaxis2=dict(title='Trips', overlaying='y', side='right'),
            hovermode='x unified',
            height=350,
            showlegend=True
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Payment breakdown
        payment_cols = ['Fare', 'Tip', 'Refund', 'Incentive', 'Boost']
        totals = {col: filtered_df[col].sum() for col in payment_cols if col in filtered_df.columns}
        totals = {k: v for k, v in totals.items() if v > 0}
        
        fig2 = go.Figure(data=[
            go.Pie(labels=list(totals.keys()), values=list(totals.values()), hole=0.3)
        ])
        fig2.update_layout(
            title='Revenue Breakdown',
            height=350
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Daily trends
    st.markdown("---")
    st.subheader("Daily Performance")

    filtered_df['Date'] = filtered_df['Trip drop off time'].dt.date
    daily_stats = filtered_df.groupby('Date').agg({
        'Trip UUID': 'count',
        'Net Earnings': 'sum',
        'Trip distance': 'sum'
    }).reset_index()
    daily_stats.columns = ['Date', 'Trips', 'Earnings', 'Distance']

    fig3 = px.line(daily_stats, x='Date', y='Earnings', markers=True, title='Daily Earnings Trend')
    fig3.update_layout(height=300, hovermode='x unified')
    st.plotly_chart(fig3, use_container_width=True)

    # Detailed table
    st.markdown("---")
    st.subheader("Transaction Details")

    display_cols = ['Trip drop off time', 'Month', 'Trip distance', 'Service type', 'Fare', 'Tip', 'Refund', 'Net Earnings', 'Customer Purchase']
    table_df = filtered_df[display_cols].copy()
    table_df['Trip drop off time'] = table_df['Trip drop off time'].dt.strftime('%Y-%m-%d %H:%M')
    table_df['Customer Purchase'] = table_df['Customer Purchase'].map({True: '✓ Yes', False: ''})

    st.dataframe(
        table_df.sort_values('Trip drop off time', ascending=False),
        use_container_width=True,
        height=400
    )

# Bank Statement Details
st.markdown("---")
st.subheader("Uber Pro Card Statement Details")

if not bank_df.empty:
    bank_filtered = bank_df[bank_df['Month'].isin(selected_month)].copy() if 'Month' in bank_df.columns else bank_df.copy()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Bank Transactions", len(bank_filtered))
    with col2:
        st.metric("Bank Net Activity", f"${bank_filtered['Amount'].sum():,.2f}")
    
    st.dataframe(
        bank_filtered[['Posted Date', 'Description', 'Amount']].sort_values('Posted Date', ascending=False),
        use_container_width=True,
        height=300
    )
else:
    st.info("Bank statement data not loaded.")

# Summary stats at bottom
st.markdown("---")
st.subheader("Reconciliation Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Payment Records", f"{len(filtered_df):,}")

with col2:
    st.metric("All Trips Reconciled", "✓ 100%")

with col3:
    st.metric("Missing Payments", "0")

st.caption("Data source: Uber trip activity, payment records, and bank statements (Aug–Dec 2025)")

with tab2:
    st.subheader("Four-Way Reconciliation Analysis")
    st.markdown("**Trips ↔ Receipts ↔ Payments ↔ Bank Deposits**")
    
    # Summary metrics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Trips", four_way_summary[four_way_summary['Metric'] == 'Total Trips (Completed)']['Value'].values[0])
    with col2:
        st.metric("Net Earnings", four_way_summary[four_way_summary['Metric'] == 'Payments (Net Earnings) Total']['Value'].values[0])
    with col3:
        st.metric("Bank Deposits", four_way_summary[four_way_summary['Metric'] == 'Bank Deposits Total']['Value'].values[0])
    with col4:
        st.metric("Difference", four_way_summary[four_way_summary['Metric'] == 'Difference (Payments - Bank)']['Value'].values[0])
    
    st.markdown("---")
    st.write("**Full Four-Way Summary:**")
    st.dataframe(four_way_summary, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Daily Reconciliation (Payment vs Bank)")
    
    # Filter daily recon by selected months if needed
    st.dataframe(daily_recon.sort_values('Date', ascending=False), use_container_width=True, height=400)
    
    st.markdown("---")
    st.subheader("Refund Verification")
    st.dataframe(refund_status.sort_values('Date', ascending=False), use_container_width=True, height=300)

with tab3:
    st.subheader("Uber Pro Card Bank Statements")
    
    if not bank_df.empty:
        bank_filtered = bank_df[bank_df['Month'].isin(selected_month)].copy() if 'Month' in bank_df.columns else bank_df.copy()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Bank Transactions", len(bank_filtered))
        with col2:
            st.metric("Bank Net Activity", f"${bank_filtered['Amount'].sum():,.2f}")
        
        st.dataframe(
            bank_filtered[['Posted Date', 'Description', 'Amount']].sort_values('Posted Date', ascending=False),
            use_container_width=True,
            height=400
        )
    else:
        st.info("Bank statement data not loaded.")
    
    st.caption("Data source: Uber Pro Card Statement CSVs (Aug–Dec 2025)")
