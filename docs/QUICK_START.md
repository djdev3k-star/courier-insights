# Courier Reconciliation - Quick Start

## For New Monthly Data

1. **Add CSV files** to these folders:
   - `data/consolidated/trips/` - Trip activity CSVs
   - `data/consolidated/payments/` - Payment records CSVs
   - `bank/` - Uber Pro Card statements

2. **Run automated pipeline:**
   ```bash
   python process_new_month.py
   ```
   This generates all 3 reports automatically.

3. **View insights:**
   ```bash
   python -m streamlit run insights_dashboard.py
   ```
   Shows actionable items only (refunds to check, large discrepancies, export buttons).

---

## What Gets Created

### Reports (Auto-generated)
- `reports/monthly_comprehensive/` - Transaction details, monthly summaries
- `reports/four_way_reconciliation/` - Cross-validation of all 4 data sources
- `reports/audit_trail/` - Complete trip-to-bank linkage

### Dashboards
- `insights_dashboard.py` - **Recommended** - Action items only
- `dashboard.py` - Full detailed view (legacy)

---

## Monthly Workflow

1. Download new CSVs from Uber
2. Drop files into folders (overwrite old ones)
3. Run: `python process_new_month.py`
4. Check: `python -m streamlit run insights_dashboard.py`
5. Review action items (unchecked refunds, large gaps)
6. Export reports as needed

Done in < 2 minutes.
