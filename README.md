# Courier Insights Dashboard

## Overview

**Courier Insights** is a purpose-built analytics dashboard for delivery drivers and couriers to analyze their earnings, identify payment issues, optimize routes, and hunt for refund opportunities.

The app processes **monthly bank statements, Uber trip activity, Uber payment history, and refund receipts** to provide actionable insights across 7 interactive pages.

**Current Data**: 5 months (Aug 2025 – Dec 2025), 1,045 completed trips, $10,823.44 total earnings, fully reconciled.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.14+ (with venv)
- Uber monthly data exports (trip activity, payment activity)
- Bank statement CSV
- Refund receipt tracker

### Installation

```bash
# Clone the repo
git clone <repo-url>
cd courier

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run courier_insights.py
```

The dashboard opens at `http://localhost:8506`

---

## 📊 Features (7 Pages)

### 🏠 **Opportunity Finder** (Home)
- Active alerts (refunds, low-pay trips, high-pay trips)
- Top 10 best & worst trips
- Most efficient trips ($/mile)
- Quick wins to replicate

### 📍 **Location Intelligence**
- Top cities with average earnings
- Best restaurants by payout & tips
- Zip code heat map
- City-zip detailed breakdown
- Earnings distribution by location

### ⏰ **Schedule Optimizer**
- Hourly earnings analysis (best hours to work)
- Day-of-week performance
- Trip volume trends
- Optimal schedule recommendations

### 🛣️ **Mileage Efficiency**
- Overall $/mile tracking
- Monthly efficiency trend
- Trip distance distribution
- Short vs long trip comparison
- Efficiency score (1-10)

### ⚠️ **Anomaly Detection**
- Refund tracking & analysis
- Low-pay trip detection
- Zero earnings flags
- Bank reconciliation status
- Payment issue dashboard

### 🔍 **Dispute Forensics**
- Search by filter or Trip ID
- Full details with pickup/dropoff addresses
- Export options:
  - Full details CSV
  - Trip IDs only (for Uber support)
  - Summary report
- Issue breakdown charts

### 📊 **Trends & Forecast**
- Monthly earnings trend
- Month-over-month comparison
- Change metrics (earnings %, trip count %, tips %)
- 3-month earnings projection

---

## 📁 Project Structure

```
courier/
├── courier_insights.py          # Main Streamlit dashboard
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── analysis/                    # Data processing scripts
│   ├── audit_trail_export.py
│   ├── uber_only_reconciliation.py
│   ├── monthly_comprehensive_report.py
│   └── four_way_reconciliation.py
│
├── data/
│   └── consolidated/            # Cleaned/consolidated data
│       ├── trips/               # Trip activity CSVs
│       └── payments/            # Payment activity CSVs
│
├── bank/                        # Bank statements & refund tracking
│   ├── bank_statement_*.csv
│   └── refund_status.csv
│
├── reports/                     # Generated reports (pre-processed data)
│   ├── audit_trail/
│   ├── monthly_comprehensive/
│   └── four_way_reconciliation/
│
└── docs/
    ├── README.md (this file)
    ├── DATA_PIPELINE_ARCHITECTURE.md
    └── QUICK_START.md
```

---

## 🔄 Data Pipeline

### Inputs (User provides monthly)
1. **Uber Trip Activity** → `data/consolidated/trips/`
2. **Uber Payment Activity** → `data/consolidated/payments/`
3. **Bank Statement** → `bank/`
4. **Refund Receipts** → `bank/refund_status.csv`

### Processing
Run analysis scripts to consolidate, clean, and reconcile:
```bash
python analysis/audit_trail_export.py
python analysis/uber_only_reconciliation.py
python analysis/monthly_comprehensive_report.py
python analysis/four_way_reconciliation.py
```

### Outputs (In `reports/`)
- Complete audit trail (all data merged)
- Monthly reconciliation
- 4-way reconciliation (Trips ↔ Payments ↔ Bank ↔ Receipts)
- Refund verification

### Dashboard
```bash
streamlit run courier_insights.py
```

Dashboard loads from `reports/` and displays all insights interactively.

---

## 🎯 Key Metrics (Persistent Sidebar)

All 7 pages display:
- **YTD Earnings** - Total money made
- **YTD Miles** - Total distance driven
- **$/Mile** - Efficiency ratio
- **Trip Count** - Total deliveries
- **Refund Rate** - % of refunded trips
- **Refund Count** - # of refunded trips

---

## 🐛 Troubleshooting

### Dashboard won't start
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Run with correct Python path (adjust path to your virtual environment)
python -m streamlit run courier_insights.py
```

### Data not loading
- Check that CSV files are in correct folders (`data/consolidated/`, `bank/`)
- Verify file names match expected pattern (dates, company names)
- See `DATA_PIPELINE_ARCHITECTURE.md` for detailed file structure

### Missing columns error
- Run analysis scripts first to generate `reports/`
- Dashboard loads from preprocessed report files, not raw data

---

## 📋 Required CSV Formats

### Uber Trip Activity
```csv
Trip drop off time,Trip UUID,Pickup address,Drop off address,Trip distance,Trip status,...
2025-08-28 12:12:56,abc123,Raising Cane's (12320...), 75180,12.89,completed,...
```

### Uber Payment Activity
```csv
vs reporting,Paid to you:Your earnings:Fare:Fare,Paid to you:Your earnings:Tip,...
2025-08-28 CDT,3.16,6.9,...
```

### Bank Statement
```csv
Date,Description,Amount,Balance
2025-08-28,Uber App Payout,250.00,5000.00
```

### Refund Receipts
```csv
Trip UUID,Date,Refund Amount,Issue Type,Status
abc123,2025-08-15,5.00,Customer Complaint,Resolved
```

---

## 📊 Current Reconciliation Status

✅ **Complete & Verified**
- All 1,045 trips matched to payments
- Bank deposits reconciled (excluding personal transactions)
- Multi-account transfers tracked ($636.35)
- Final gap: $263.57 (2.44% variance - acceptable for processing delays)

See `reports/four_way_reconciliation/multi_account_reconciliation.csv` for details.

---

## 🛠️ Development

### Adding new pages to dashboard
Edit `courier_insights.py`:
1. Add new option to `page` radio selector
2. Create new `elif page == "..."` block
3. Use existing data from `load_data()` function
4. Add to sidebar navigation

### Modifying analysis logic
Edit scripts in `analysis/` folder:
1. Update data processing logic
2. Run script to regenerate `reports/`
3. Dashboard automatically loads updated data

### Creating new reports
1. Create new Python script in `analysis/`
2. Input: Load from `data/consolidated/` or existing reports
3. Output: Save to `reports/<category>/`
4. Dashboard can load via `safe_read()` function

---

## 📝 Notes

- **Data Privacy**: All personal data (addresses, amounts) is stored locally only
- **No Cloud Sync**: Reports are local files, not uploaded anywhere
- **Reconciliation**: Uses Trip UUID as primary key to match trips ↔ payments ↔ bank deposits
- **Timezone Handling**: Strips CDT/CST from timestamps before parsing to avoid datetime errors
- **Bank Filtering**: Automatically excludes personal transactions (filters for "Uber App Payout")

---

## 🤝 Contributing

Ideas for enhancements:
- [ ] Customer rating integration (if available from Uber)
- [ ] Gas/mileage deduction calculator
- [ ] Tax summary report
- [ ] Scheduled report exports (email weekly summary)
- [ ] Real-time alerts (SMS for high-pay trips)
- [ ] Multi-platform support (Uber Eats, DoorDash integration)

---

## 📞 Support

For issues:
1. Check `DATA_PIPELINE_ARCHITECTURE.md` for complete data flow
2. Verify all CSV files are in correct locations
3. Run analysis scripts to regenerate reports
4. Check terminal for specific error messages

---

## 📄 License

Personal use project. Feel free to modify and extend for your courier business.

---

**Last Updated**: January 2026  
**Current Data**: August 2025 – December 2025  
**Status**: ✅ Production Ready

---

## How to Regenerate Reports

```bash
python analysis/comprehensive_monthly_report.py
```

This recreates all files in `reports/monthly_comprehensive/`.

---

## Data Quality Notes

✓ **Trip-to-Payment Reconciliation**: 100% (0 unpaid trips)  
✓ **Payment Records**: 4,011 transactions across 1,045 unique trips  
✓ **Bank Deposits**: 2,294 transactions (deposits + charges)  
✓ **Date Coverage**: Aug 1 – Dec 31, 2025 (5 months)

Monthly payment-to-bank differences are due to:
- Bank deposit batching (single bank deposit may include multiple payment dates)
- Processing delays (transactions post on different dates than payment date)
- Pending deposits (amounts not yet cleared to bank)
