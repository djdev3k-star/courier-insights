# 🗺️ Repository Sitemap

## Directory Structure Overview

```
📦 courier/
│
├── 🌐 index.html ⭐ START HERE - Navigation Dashboard
├── 📖 README.md - Complete documentation
│
├── 📂 docs/ ━━━━━━━━━━━━━━━━━━━━━━━━━ All Reports & Documentation
│   ├── 🎯 ACTUAL_VS_RECOMMENDED_REPORT.md ⚠️ PRIORITY #1
│   │   └── Performance: F Grade (33.3%), $471/month overspending
│   │
│   ├── 📅 SCHEDULE_OPTIMIZATION_PLAN.md
│   │   └── Target: $3,050/month, Peak: 6-11 PM
│   │
│   ├── 💰 SCHEDULE_SPENDING_CORRELATION_REPORT.md
│   │   └── 72% spending at pickup locations, Save $470/month
│   │
│   ├── 🔍 UNCATEGORIZED_MERCHANT_ANALYSIS_REPORT.md
│   │   └── $3,982 analyzed, $2,876 at work locations
│   │
│   ├── 💵 EXPENSE_REPORT.md
│   │   └── $1,158 reimbursable vs $5,250 personal
│   │
│   ├── ⚡ SCHEDULE_QUICK_REFERENCE.md
│   │   └── One-page cheat sheet
│   │
│   ├── 🚀 QUICK_START.md
│   ├── 📖 START_HERE.md
│   ├── 📊 DASHBOARD_GUIDE.md
│   ├── 🚢 DEPLOYMENT_GUIDE.md
│   ├── ✅ DATA_INTEGRITY_REPORT.md
│   └── 📋 Other documentation files
│
├── 📂 scripts/ ━━━━━━━━━━━━━━━━━━━━━━━ Python Analysis Tools
│   ├── 💳 expense_analyzer.py
│   │   └── Categorizes transactions → 3 CSV exports
│   │
│   ├── ⏰ schedule_optimizer.py
│   │   └── Finds optimal work hours by day/time
│   │
│   ├── 🏪 deep_merchant_analysis.py
│   │   └── Business type categorization + trip cross-reference
│   │
│   ├── 📊 actual_vs_recommended_analysis.py
│   │   └── Compares actual behavior vs optimal plan
│   │
│   ├── 🔗 schedule_spending_correlation.py
│   │   └── Correlates spending with restaurant pickups
│   │
│   ├── ❓ uncategorized_analysis.py
│   │   └── Analyzes $3,982 uncategorized spending
│   │
│   ├── 📈 dashboard.py (Streamlit)
│   ├── 🔄 process_new_month.py
│   ├── 🗺️ pre_geocode_addresses.py
│   └── Other utility scripts
│
├── 📂 reports/ ━━━━━━━━━━━━━━━━━━━━━━━ Generated Output Files
│   ├── expense_report_20260128_134248.csv (31.9 KB)
│   │   └── All 2,294 transactions with categories
│   │
│   ├── reimbursable_expenses_20260128.csv (6.4 KB)
│   │   └── Business expenses only: $1,158
│   │
│   ├── personal_expenses_20260128.csv (25.5 KB)
│   │   └── Personal spending only: $5,250
│   │
│   ├── uncategorized_analysis_detailed.csv (42.8 KB)
│   │   └── 218 transactions analyzed by merchant type
│   │
│   ├── uncategorized_potential_business_expenses.csv (38.7 KB)
│   │   └── $2,876 at pickup locations
│   │
│   ├── 📂 dashboards/
│   │   └── HTML report files
│   │
│   ├── 📂 audit_trail/
│   ├── 📂 four_way_reconciliation/
│   ├── 📂 monthly_comprehensive/
│   └── 📂 refund_lag/
│
├── 📂 data/ ━━━━━━━━━━━━━━━━━━━━━━━━━━ Source Data
│   ├── 📂 consolidated/
│   │   ├── 📂 trips/ ⭐
│   │   │   ├── 202508-FULL-trip_activity-.csv (32 trips)
│   │   │   ├── 202509-FULL-trip_activity-.csv (280 trips)
│   │   │   ├── 202510-FULL-trip_activity-.csv (422 trips)
│   │   │   ├── 202511-FULL-trip_activity-.csv (132 trips)
│   │   │   └── 202512-FULL-trip_activity-.csv (211 trips)
│   │   │       └── Total: 1,077 trips
│   │   │
│   │   └── 📂 payments/
│   │
│   ├── 📂 raw/
│   │   ├── 📂 trips/
│   │   └── 📂 payments/
│   │
│   ├── 📂 receipts/
│   │   └── Trip Receipts-Refund Tracker.csv
│   │
│   └── geocoded_addresses.csv
│
├── 📂 bank/ ━━━━━━━━━━━━━━━━━━━━━━━━━ Bank Statements
│   ├── Uber Pro Card Statement_ Aug 2025.csv
│   ├── Uber Pro Card Statement_ Sep 2025.csv
│   ├── Uber Pro Card Statement_ Oct 2025.csv
│   ├── Uber Pro Card Statement_ Nov 2025.csv
│   └── Uber Pro Card Statement_ Dec 2025.csv
│       └── Total: 2,294 transactions analyzed
│
├── 📂 analysis/ ━━━━━━━━━━━━━━━━━━━━━ Specialized Analysis
│   ├── comprehensive_monthly_report.py
│   ├── four_way_reconciliation.py
│   ├── bank_refund_match.py
│   ├── customer_purchase_reconciliation.py
│   ├── refund_lag_report.py
│   ├── uber_only_reconciliation.py
│   └── README.md
│
├── 📂 visualizations/ ━━━━━━━━━━━━━━━ Visual Assets
│   ├── SCHEDULE_VISUAL_GUIDE.txt
│   └── JTechLogistics_Logo.svg
│
├── 📂 trips/ ━━━━━━━━━━━━━━━━━━━━━━━━ (Legacy folder)
│
└── 📂 Other
    ├── .venv/ - Python virtual environment
    ├── __pycache__/ - Python cache
    ├── .streamlit/ - Streamlit config
    ├── requirements.txt
    ├── netlify.toml
    └── run_app.bat
```

---

## 🎯 Quick Navigation Paths

### For Daily Use
```
Start Here: index.html
Quick Reference: docs/SCHEDULE_QUICK_REFERENCE.md
Check Performance: docs/ACTUAL_VS_RECOMMENDED_REPORT.md
```

### For Analysis
```
Run Expense Analysis: scripts/expense_analyzer.py
Check Results: reports/expense_report_*.csv
Review Categorization: reports/uncategorized_analysis_detailed.csv
```

### For Optimization
```
Read Schedule: docs/SCHEDULE_OPTIMIZATION_PLAN.md
Compare Performance: docs/ACTUAL_VS_RECOMMENDED_REPORT.md
See Spending Patterns: docs/SCHEDULE_SPENDING_CORRELATION_REPORT.md
```

---

## 📊 Data Flow

```
Bank Statements (bank/)
    ↓
expense_analyzer.py (scripts/)
    ↓
Expense Reports (reports/)
    ↓
Read via index.html

Trip Data (data/consolidated/trips/)
    ↓
schedule_optimizer.py (scripts/)
    ↓
Schedule Plan (docs/)
    ↓
Read via index.html

Both Combined
    ↓
actual_vs_recommended_analysis.py (scripts/)
    ↓
Performance Report (docs/)
    ↓
Action Items!
```

---

## 🎯 File Priority Ranking

### ⭐⭐⭐ CRITICAL (Read These First)
1. `index.html` - Navigation hub
2. `docs/ACTUAL_VS_RECOMMENDED_REPORT.md` - Your performance grade
3. `docs/SCHEDULE_OPTIMIZATION_PLAN.md` - How to work optimally
4. `docs/SCHEDULE_SPENDING_CORRELATION_REPORT.md` - Why you overspend

### ⭐⭐ IMPORTANT (Review Weekly)
5. `docs/EXPENSE_REPORT.md` - Financial breakdown
6. `docs/UNCATEGORIZED_MERCHANT_ANALYSIS_REPORT.md` - Spending analysis
7. `docs/SCHEDULE_QUICK_REFERENCE.md` - Daily cheat sheet
8. `reports/expense_report_*.csv` - Latest spending data

### ⭐ REFERENCE (As Needed)
9. All other docs/
10. Generated reports in reports/
11. Scripts for regenerating analysis

---

## 🔍 Finding Specific Information

### "How much did I spend on restaurants?"
→ `docs/EXPENSE_REPORT.md` (Dining section)
→ `reports/personal_expenses_*.csv` (filter Category)

### "What are my optimal work hours?"
→ `docs/SCHEDULE_OPTIMIZATION_PLAN.md`
→ `docs/SCHEDULE_QUICK_REFERENCE.md`

### "How much can I save?"
→ `docs/ACTUAL_VS_RECOMMENDED_REPORT.md` (Bottom line section)
→ Answer: $470/month = $5,640/year

### "Where is all my data?"
→ `data/consolidated/trips/` (trip data)
→ `bank/` (bank statements)
→ `reports/` (processed outputs)

### "What's my biggest problem?"
→ `docs/ACTUAL_VS_RECOMMENDED_REPORT.md`
→ Answer: Working wrong hours (67% inefficient) + Raising Canes ($138/month)

---

## 📱 Mobile-Friendly Files

These files render well on mobile:
- `index.html` - Responsive design
- `README.md` - Basic markdown
- `docs/SCHEDULE_QUICK_REFERENCE.md` - One page

These are better on desktop:
- Large CSV files in `reports/`
- Detailed analysis reports
- Python scripts

---

## 🆘 Lost? Start Here

1. Open `index.html` in browser
2. Click "Start Here" button
3. Read `docs/START_HERE.md`
4. Follow the guide step by step

---

**Repository organized on:** January 28, 2026  
**Total files:** 100+  
**Total folders:** 12 main directories  
**Size:** ~150 MB (including data)
