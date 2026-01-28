# Interactive Dashboard Guide

## Launch Dashboard
```bash
python -m streamlit run insights_dashboard.py
```

## Navigation

Use the sidebar to navigate between 5 main pages:

### 🏠 Overview
**What it shows:**
- 4 key metrics: Net Earnings, Bank Deposits, Pending Amount, Unchecked Refunds
- Quick action cards with clickable buttons to drill into details
- Earnings timeline chart (payments vs bank deposits over time)
- Monthly breakdown (trip count and earnings per month)

**How to use:**
- Review metrics at the top for overall health
- Click "View Details" / "Explore Trips" / "Review Refunds" to jump to specific pages
- Hover over charts to see exact values
- Zoom in/out on timeline to focus on specific periods

---

### 📅 Daily Analysis
**What it shows:**
- Filterable daily reconciliation data
- Scatter plot of discrepancies by date (sized by amount)
- Interactive table of daily payment vs bank comparisons

**Interactive features:**
- **Min Gap ($)**: Set threshold to show only days with large gaps (e.g., 100)
- **Date Range**: Pick start/end dates to focus analysis
- **Sort by**: Order by Date, Gap Amount, or Net Earnings
- **Click rows**: Select a day in the table to see all trips from that day

**Use cases:**
- Find days with largest payment/bank timing differences
- Track down specific date ranges for accounting
- Export filtered data for records

---

### 🚗 Trip Explorer
**What it shows:**
- Searchable, filterable list of all trips
- Expandable cards showing trip details
- Full trip drill-down with payment breakdown

**Interactive features:**
- **Search UUID**: Type partial UUID to find specific trips
- **Status filter**: Multi-select trip status (Completed, etc.)
- **Reconciliation filter**: Show only Bank Matched, Refund Tracked, etc.
- **Min Earnings slider**: Hide small trips, focus on large ones
- **Sort options**: Order by time, earnings, or status

**Expandable trip cards:**
Each card shows:
- Date/time and net earnings in header
- **Expand** to see:
  - Trip UUID, status, timestamp
  - Earnings breakdown (fare, tip, net)
  - Reconciliation status
  - Refund alerts if applicable
- **"View Full Details" button**: Opens complete trip detail page

**Trip detail page:**
- Payment component breakdown (bar chart + table)
- Full audit trail with bank matching info
- Refund tracking if applicable
- Raw JSON data view

**Pagination:**
- Shows first 50 trips matching filters
- Narrow filters to see different trips
- Message shown if >50 results

---

### 💰 Refund Tracker
**What it shows:**
- All refunds from receipts tracker
- Verification status (Match vs unchecked)
- Comparison with payment system refunds

**Interactive features:**
- **Filter**: View All / Unchecked Only / Checked Only
- **Sort**: By date or refund amount
- **Expandable cards**: Click each refund to see:
  - Date, amount, status, pickup address
  - Payment system refund amount
  - Difference calculation (alerts if mismatch)
  - Match verification status

**Metrics displayed:**
- Total refund count
- Number unchecked (needs review)
- Total refund dollar amount

**Pie chart:**
- Visual breakdown of checked vs unchecked refunds
- Color-coded for quick assessment

**Use cases:**
- Verify refunds match between systems
- Track down unchecked refunds needing review
- Export refund status for records

---

### 📊 Analytics
**What it shows:**
- Time-based performance analysis
- Earnings distribution
- Export all reports

**Hourly performance chart:**
- Dual-axis: Bar chart (trip count) + Line (average earnings)
- See which hours are busiest and most profitable
- Hover to see exact values

**Day of week analysis:**
- Bar chart showing total earnings per day
- Color intensity shows trip count
- Identify best/worst days

**Performance metrics:**
- Average trip earnings
- Median trip earnings
- Maximum single trip
- Total trip count

**Earnings distribution histogram:**
- 50 bins showing spread of trip values
- See if most trips cluster around certain amounts
- Identify outliers

**Export buttons:**
- Download Complete Audit Trail (CSV)
- Download Daily Reconciliation (CSV)
- Download Refund Status (CSV)

---

## Key Interactive Features

### 1. Click Navigation
- Click metric cards on Overview → Jump to detail pages
- Click trip cards → Expand to see breakdown
- Click "View Full Details" → Open complete trip page
- Click "Back to Trips" → Return from detail pages

### 2. Filters & Search
- **Text input**: Search trips by UUID
- **Multi-select dropdowns**: Filter by multiple statuses
- **Sliders**: Set numeric thresholds
- **Date pickers**: Focus on specific date ranges
- **Radio buttons**: Toggle between view modes
- **Sort dropdowns**: Reorder data dynamically

### 3. Expandable Sections
- **Trip cards**: Click to expand, see payment breakdown
- **Refund cards**: Click to expand, compare amounts
- **"View Full" buttons**: Drill into complete details
- **Expander sections**: Show/hide JSON data

### 4. Charts & Visualizations
- **Hover tooltips**: See exact values without clicking
- **Zoom/Pan**: Click and drag on charts
- **Reset zoom**: Double-click charts
- **Download**: Camera icon saves chart as PNG
- **Color coding**: Red (problems), Green (good), Blue (neutral)

### 5. Data Export
- **Download buttons**: Export filtered/full data as CSV
- **Opens in browser**: Save or open in Excel
- **Preserves filters**: Exports what you see

---

## Workflow Examples

### Monthly Review (2 minutes)
1. Open Overview → Check metrics
2. If "Unchecked Refunds" > 0 → Click "Review Refunds"
3. Review each unchecked refund → Verify amounts
4. Click "Daily Analysis" → Check for large gaps
5. Export audit trail for records

### Find Specific Trip
1. Go to Trip Explorer
2. Type partial UUID in search
3. Or filter by date range + status
4. Click trip card → Expand
5. Click "View Full Details" for complete info

### Investigate Discrepancy
1. Go to Daily Analysis
2. Set "Min Gap ($)" to 100
3. Look at scatter plot for outliers
4. Click a day in table
5. See all trips from that day
6. Cross-reference with bank statement

### Verify Refunds
1. Go to Refund Tracker
2. Select "Unchecked Only"
3. Expand each refund card
4. Check if amounts match
5. Mark verified refunds in tracker spreadsheet
6. Re-run pipeline to update status

---

## Tips for Power Users

1. **Use keyboard**: Tab through filters, Enter to apply
2. **Bookmark views**: Copy URL with filters applied (Streamlit preserves state)
3. **Chain filters**: Combine search + status + earnings for precise results
4. **Watch the metrics**: Top cards show filtered counts
5. **Export often**: Save snapshots before changing filters
6. **Check daily**: New data? Re-run pipeline, refresh dashboard

---

## Troubleshooting

**Dashboard won't load:**
- Run `python process_new_month.py` first to generate reports
- Check that all CSV files exist in reports/ folders

**Data looks wrong:**
- Clear cache: Click "Clear cache" in Streamlit menu (☰)
- Re-run pipeline: `python process_new_month.py`
- Check source CSV files for issues

**Charts not interactive:**
- Ensure you have `plotly` installed
- Try refreshing the browser
- Check console for JavaScript errors

**Can't find a trip:**
- Try partial UUID (first 8-10 characters)
- Check date filters aren't excluding it
- Verify trip exists in source CSV

---

## Keyboard Shortcuts

- `C` - Clear cache
- `R` - Rerun app
- `S` - Open settings
- `/` - Focus search
- `Esc` - Close modals

---

**Questions?** Check reports/ folders for raw CSV data to cross-reference.
