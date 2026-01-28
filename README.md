# 📊 Courier Business Analytics System

## Quick Access
**🌐 Open `index.html` in your browser for easy navigation of all reports and tools**

---

## 📁 Repository Structure

```
courier/
├── index.html                      # Main navigation dashboard (START HERE!)
│
├── docs/                           # All documentation and reports
│   ├── START_HERE.md              # Getting started guide
│   ├── QUICK_START.md             # Quick reference
│   ├── ACTUAL_VS_RECOMMENDED_REPORT.md       # ⚠️ Performance analysis
│   ├── SCHEDULE_OPTIMIZATION_PLAN.md         # Optimal work schedule
│   ├── SCHEDULE_SPENDING_CORRELATION_REPORT.md # Spending patterns
│   ├── UNCATEGORIZED_MERCHANT_ANALYSIS_REPORT.md # Deep merchant analysis
│   ├── EXPENSE_REPORT.md          # Financial breakdown
│   ├── SCHEDULE_QUICK_REFERENCE.md # One-page cheat sheet
│   ├── DASHBOARD_GUIDE.md         # Dashboard usage
│   ├── DEPLOYMENT_GUIDE.md        # Deployment instructions
│   ├── DATA_INTEGRITY_REPORT.md   # Data validation
│   └── ...                        # Other guides and reports
│
├── scripts/                        # Python analysis scripts
│   ├── expense_analyzer.py        # Expense categorization
│   ├── schedule_optimizer.py      # Schedule optimization
│   ├── deep_merchant_analysis.py  # Merchant type analysis
│   ├── actual_vs_recommended_analysis.py  # Performance comparison
│   ├── schedule_spending_correlation.py   # Spending correlations
│   ├── uncategorized_analysis.py  # Uncategorized expense review
│   ├── dashboard.py               # Streamlit dashboard
│   └── ...                        # Other analysis tools
│
├── reports/                        # Generated reports and exports
│   ├── expense_report_*.csv       # Expense data exports
│   ├── reimbursable_expenses_*.csv # Business expenses
│   ├── personal_expenses_*.csv    # Personal spending
│   ├── uncategorized_*.csv        # Uncategorized analysis
│   └── dashboards/                # HTML reports
│
├── data/                          # Source data
│   ├── consolidated/
│   │   ├── trips/                 # Trip activity data
│   │   └── payments/              # Payment data
│   ├── raw/                       # Original data files
│   └── geocoded_addresses.csv     # Location data
│
├── bank/                          # Bank statements
│   └── Uber Pro Card Statement_*.csv
│
├── analysis/                      # Specialized analysis modules
│   ├── comprehensive_monthly_report.py
│   ├── four_way_reconciliation.py
│   └── ...
│
├── visualizations/                # Visual assets
│   ├── SCHEDULE_VISUAL_GUIDE.txt
│   └── JTechLogistics_Logo.svg
│
└── README.md                      # This file
```

---

## 🎯 Key Findings Summary

### Performance Analysis (Aug-Dec 2025)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Schedule Adherence | 100% optimal hours | 33.3% | ❌ F Grade |
| Monthly Spending | $811 | $1,282 | ❌ $471 over |
| Raising Canes | $0 | $138/month | ❌ Complete failure |
| Peak Hour Usage | 6-11 PM focus | 41.4% | ❌ Low |

**Savings Potential:** $470/month = **$5,640/year** with optimization

---

## 🚀 Quick Start

### 1. View Main Dashboard
```bash
# Open in browser
start index.html
```

### 2. Run Expense Analysis
```bash
cd scripts
python expense_analyzer.py
```

### 3. Generate Performance Report
```bash
cd scripts
python actual_vs_recommended_analysis.py
```

### 4. View Interactive Dashboard
```bash
cd scripts
streamlit run dashboard.py
```

---

## 📊 Most Important Reports

1. **[Actual vs. Recommended](docs/ACTUAL_VS_RECOMMENDED_REPORT.md)** - ⚠️ READ FIRST
   - Performance grade: F (33.3%)
   - $2,353 wasted over 5 months
   - Working 67% during inefficient hours

2. **[Schedule Optimization](docs/SCHEDULE_OPTIMIZATION_PLAN.md)**
   - Optimal work hours by day
   - Target: $3,050/month
   - Peak hours: 6-11 PM

3. **[Spending Correlation](docs/SCHEDULE_SPENDING_CORRELATION_REPORT.md)**
   - 72% of spending at pickup locations
   - Raising Canes: $814 total ($30/visit)
   - Meal prep saves $470/month

4. **[Expense Report](docs/EXPENSE_REPORT.md)**
   - $1,158 reimbursable
   - $5,250 personal
   - Detailed category breakdown

---

## 🛠️ Analysis Tools

### Core Scripts

| Script | Purpose | Output |
|--------|---------|--------|
| `expense_analyzer.py` | Categorize bank transactions | 3 CSV files |
| `schedule_optimizer.py` | Find optimal work hours | Schedule plan |
| `deep_merchant_analysis.py` | Analyze by merchant type | Detailed CSV |
| `actual_vs_recommended_analysis.py` | Performance comparison | Console report |
| `schedule_spending_correlation.py` | Correlate spending patterns | Analysis report |

### Specialized Tools

- `dashboard.py` - Interactive Streamlit dashboard
- `process_new_month.py` - Monthly data processing
- `pre_geocode_addresses.py` - Location geocoding
- Analysis folder - Reconciliation and audit tools

---

## 📈 Data Files

### Input Data
- **Trip Data:** `data/consolidated/trips/*.csv` (1,077 trips)
- **Bank Statements:** `bank/Uber Pro Card Statement_*.csv`
- **Receipts:** `data/receipts/Trip Receipts-Refund Tracker.csv`

### Generated Reports
- **Expense Reports:** `reports/expense_report_*.csv`
- **Reimbursable:** `reports/reimbursable_expenses_*.csv`
- **Personal:** `reports/personal_expenses_*.csv`
- **Uncategorized:** `reports/uncategorized_*.csv`

---

## 🎯 Action Items (Priority Order)

### CRITICAL (Do This Week)
- [ ] Read [Actual vs. Recommended Report](docs/ACTUAL_VS_RECOMMENDED_REPORT.md)
- [ ] Stop working after 11 PM (shift to 6-10 PM)
- [ ] Eliminate Raising Canes ($138/month waste)

### HIGH (Do This Month)
- [ ] Follow [Schedule Optimization Plan](docs/SCHEDULE_OPTIMIZATION_PLAN.md)
- [ ] Meal prep for Sat/Sun (busiest days)
- [ ] Pack snacks for late-night shifts
- [ ] Track daily spending (target $900/month)

### ONGOING
- [ ] Monitor adherence to optimal schedule
- [ ] Review spending weekly
- [ ] Run monthly performance analysis

---

## 💰 Financial Impact

### Current State (Aug-Dec 2025)
- Monthly earnings: ~$3,000 (estimated)
- Monthly spending: $1,282
- Net income: ~$1,718

### With Optimization
- Monthly earnings: $3,050 (optimized schedule)
- Monthly spending: $811 (following plan)
- Net income: $2,239
- **Improvement: +$521/month (+30%)**

---

## 🔧 Setup & Installation

### Requirements
```bash
python 3.14+
pip install pandas numpy streamlit plotly
```

### First Time Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run initial analysis
cd scripts
python expense_analyzer.py
python schedule_optimizer.py
```

---

## 📱 Navigation Tips

- **Use `index.html`** - Visual navigation of all reports
- **Press `/`** in index.html to search
- **Start with** `docs/START_HERE.md` for context
- **Check** `docs/QUICK_START.md` for daily reference

---

## 🆘 Troubleshooting

### Scripts not running?
```bash
# Check Python path
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Reports missing?
```bash
# Regenerate all reports
cd scripts
python expense_analyzer.py
python actual_vs_recommended_analysis.py
```

### Dashboard not loading?
```bash
cd scripts
streamlit run dashboard.py --server.port 8501
```

---

## 📝 Notes

- All analysis based on Aug-Dec 2025 data
- Currency: USD
- Location: Dallas, TX area
- Business: Uber/food delivery courier

---

## 🔄 Monthly Workflow

1. Process new month: `python scripts/process_new_month.py`
2. Run expense analysis: `python scripts/expense_analyzer.py`
3. Generate performance comparison: `python scripts/actual_vs_recommended_analysis.py`
4. Review reports in `reports/` folder
5. Update targets based on findings

---

## 📞 Support

For questions or issues, refer to:
- `docs/DASHBOARD_GUIDE.md` - Dashboard usage
- `docs/DEPLOYMENT_GUIDE.md` - Setup help
- `docs/DATA_INTEGRITY_REPORT.md` - Data validation

---

**Last Updated:** January 28, 2026  
**Analysis Period:** August - December 2025  
**Total Trips:** 1,077  
**Total Expenses:** $6,408
