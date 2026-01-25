# Courier Insights: Complete Data Pipeline Architecture

## Overview
Your app is a **3-stage data processing system**:

```
RAW DATA (User Inputs)
    ↓
[ANALYSIS SCRIPTS - Processing & Reconciliation]
    ↓
REPORTS (Processed/Reconciled Data)
    ↓
[COURIER_INSIGHTS.PY - Interactive Dashboard]
    ↓
USER INTERFACE (7 Pages of Analytics)
```

---

## Stage 1: RAW DATA (What User Provides)

### File Structure Required:
```
courier/
├── trips/
│   ├── 20250801-20250831-trip_activity-Derrick_James.csv
│   ├── 20250901-20250930-trip_activity-Derrick_James.csv
│   └── ... (monthly trip exports from Uber)
│
├── data/consolidated/trips/
│   └── trip_activity_*.csv (consolidated trip files)
│
├── data/consolidated/payments/
│   └── payment_activity_*.csv (consolidated payment files)
│
├── bank/
│   ├── bank_statement_*.csv (monthly bank statements)
│   └── refund_status.csv (tracked receipts/refunds)
│
├── payments/
│   ├── 20250801-20250831-payments_order-Derrick_James.csv
│   ├── 20250901-20250930-payments_order-Derrick_James.csv
│   └── ... (monthly payment exports from Uber)
```

### Source Data Details:

#### 1. **Uber Trip Activity** (Monthly downloads)
```csv
Trip drop off time, Trip distance, Trip status, Pickup address, Drop off address, ...
2025-08-28 12:12:56, 12.89, completed, Raising Cane's (12320 Lake June Road)..., ...
```
- **From**: Uber Driver app → Statements → Trip History
- **Contains**: Distance, pickup/dropoff locations, times, service type
- **Used for**: Base earnings, location analysis, schedule optimization

#### 2. **Uber Payment Activity** (Monthly downloads)
```csv
vs reporting, Paid to you:Your earnings:Fare:Fare, Paid to you:Your earnings:Tip, ...
2025-08-28 CDT, 3.16, 6.9, ...
```
- **From**: Uber Driver app → Statements → Payment History
- **Contains**: Fare breakdown (Fare, Tip, Incentive, Boost, Refunds, etc.)
- **Used for**: Earnings reconciliation, refund tracking, payment analysis

#### 3. **Bank Statements** (Monthly bank downloads)
```csv
Date, Description, Amount, Balance
2025-08-28, Uber App Payout, 250.00, 5000.00
2025-08-28, Amazon Purchase, -45.99, 4954.01
```
- **From**: Your bank (Chase, BOA, etc.)
- **Contains**: All transactions (Uber deposits + personal spending)
- **Used for**: Bank reconciliation, deposit tracking

#### 4. **Refund Receipts/Tracker** (Manual spreadsheet or export)
```csv
Trip UUID, Date, Refund Amount, Issue Type, Status
a1b2c3d4-e5f6-7890-abcd-ef1234567890, 2025-08-15, 5.00, Customer Complaint, Resolved
```
- **From**: Manual tracking + Uber dispute history
- **Contains**: Trip UUID, refund reason, status
- **Used for**: Refund verification, dispute forensics

---

## Stage 2: ANALYSIS SCRIPTS (Processing & Reconciliation)

### Script 1: `audit_trail_export.py`
**Purpose**: Create unified audit trail with all data sources merged

**Input**: 
- Trip data + Payment data + Bank data + Refund data

**Output**: 
- `reports/audit_trail/complete_audit_trail.csv` (1045 rows, all columns)

**What it does**:
1. Loads all monthly trip files → consolidates into one
2. Loads all monthly payment files → consolidates into one
3. Merges trips + payments by Trip UUID
4. Adds bank deposit dates by matching amounts/times
5. Adds refund status by Trip UUID
6. Calculates Net Earnings = Fare + Tip + Incentive + Boost - Refund - Fees

**Example Output**:
```
Trip UUID, Trip drop off time, Pickup address, Net Earnings, Refund, Payment Date, Bank Deposit Date
a1b2c3d4-e5f6-7890-abcd-ef1234567890, 2025-08-28, Restaurant X, 12.34, 0.00, 2025-08-28, 2025-08-29
```

### Script 2: `uber_only_reconciliation.py`
**Purpose**: Reconcile Uber to bank deposits (excluding personal transactions)

**Input**: 
- Trip data + Payment data + Bank data

**Output**: 
- `reports/four_way_reconciliation/four_way_summary.csv`
- `reports/four_way_reconciliation/multi_account_reconciliation.csv`

**What it does**:
1. Sums all Uber payments (earnings from all trips)
2. Filters bank transactions to only "Uber App Payout" (excludes personal purchases)
3. Compares total earnings to total deposits
4. Calculates gap (explains processing delays, transfers, etc.)
5. Tracks deposits to multiple accounts if applicable

**Example Output**:
```
Metric, Value
Total Earnings (Uber), $10,823.44
Total Bank Deposits (Uber only), $9,923.52
Other Accounts, $636.35
Gap, $263.57
Status, 2.44% variance (acceptable)
```

### Script 3: `monthly_comprehensive_report.py`
**Purpose**: Detailed breakdown by month, trip type, payment type

**Input**: 
- Trip data + Payment data + Refund data

**Output**: 
- `reports/monthly_comprehensive/all_transactions_detailed.csv`

**What it does**:
1. Groups transactions by month, service type, payment type
2. Calculates refund rate, tip rate, average earnings
3. Extracts city/zip/restaurant info from addresses
4. Creates clean, analysis-ready dataset

**Example Output**:
```
Trip drop off time, Month, Trip UUID, Pickup address, Net Earnings, Restaurant, Pickup City, Pickup Zip
2025-08-28 12:12:56, 2025-08, a1b2c3d4, Raising Cane's..., 26.20, Raising Cane's, Balch Springs, 75180
```

### Script 4: `four_way_reconciliation.py`
**Purpose**: Final reconciliation comparing all data sources

**Input**: 
- Trips vs Payments vs Bank vs Receipts

**Output**: 
- `reports/four_way_reconciliation/daily_reconciliation_3way.csv`

**What it does**:
1. Compares daily trips to daily payments (do counts match?)
2. Compares daily payments to daily bank deposits (do amounts match?)
3. Flags discrepancies (missing trips, overpayments, etc.)
4. Validates refund receipts against Uber records

**Example Output**:
```
Date, Trips, Payments, Bank Deposit, Status
2025-08-28, 15, 15, Match, BANK_MATCHED
2025-08-29, 12, 12, Match, BANK_MATCHED
2025-08-30, 18, 18, No Deposit, PENDING
```

---

## Stage 3: REPORTS (Processed Data Ready for Dashboard)

```
reports/
├── audit_trail/
│   └── complete_audit_trail.csv ← All data sources merged
│
├── monthly_comprehensive/
│   └── all_transactions_detailed.csv ← Clean transaction data
│
└── four_way_reconciliation/
    ├── four_way_summary.csv ← Summary metrics
    ├── multi_account_reconciliation.csv ← Multi-account tracking
    ├── daily_reconciliation_3way.csv ← Daily reconciliation
    └── refund_verification_status.csv ← Refund tracking
```

**Key Advantage**: Reports are **pre-processed and cleaned**, so the dashboard doesn't need to do heavy lifting.

---

## Stage 4: COURIER_INSIGHTS.PY (Dashboard)

### Data Loading:
```python
transactions = read('reports/monthly_comprehensive/all_transactions_detailed.csv')
audit = read('reports/audit_trail/complete_audit_trail.csv')
refunds = read('reports/four_way_reconciliation/refund_verification_status.csv')
multi_account = read('reports/four_way_reconciliation/multi_account_reconciliation.csv')
```

### Processing:
- Extracts city/zip/restaurant from addresses
- Calculates $/mile, refund rates, efficiency metrics
- Groups by hour, day, location, restaurant

### Display:
- 7-page interactive dashboard
- Real-time calculations
- Export options

---

## How It Works: Complete User Flow

### Month 1: Setup & First Run
```
1. User downloads from Uber:
   - August 2025 Trip Activity CSV
   - August 2025 Payment Activity CSV

2. User gets bank statement:
   - August 2025 from their bank

3. User tracks refunds:
   - Manually or from Uber dispute history

4. User places all files in courier/ folder structure

5. User runs analysis scripts:
   python analysis/audit_trail_export.py
   python analysis/uber_only_reconciliation.py
   python analysis/monthly_comprehensive_report.py
   python analysis/four_way_reconciliation.py

6. Scripts generate reports/ folder with cleaned data

7. User launches dashboard:
   streamlit run courier_insights.py

8. Dashboard loads from reports/ and displays all 7 pages
```

### Month 2+: Recurring Monthly Process
```
1. Download new Uber reports (Sept 2025 data)
2. Get new bank statement
3. Place in appropriate folders
4. Run analysis scripts (they append/consolidate automatically)
5. Refresh dashboard (automatically loads new data)
6. All historical data persists + new month added
```

---

## Why This Architecture Works

### ✅ **Separation of Concerns**
- Raw data stays raw (not modified)
- Analysis layer is independent of display
- Dashboard can change without touching data processing

### ✅ **Scalability**
- New months just get added to folders
- Scripts automatically consolidate all months
- Dashboard handles any number of months

### ✅ **Auditability**
- Every step is logged (what's being read, calculated, output)
- Reports are CSVs (human-readable, can be opened in Excel)
- Easy to verify calculations

### ✅ **Recovery**
- If dashboard breaks, reports still exist
- If analysis script fails, raw data untouched
- Can re-run specific script without affecting others

### ✅ **Extensibility**
- New analysis scripts can be added without touching existing ones
- New dashboard pages load from existing reports
- Can add new data sources (gas prices, customer reviews, etc.)

---

## To Make It Fully Automated

For a user who wants zero friction, create a **data_intake.py** script:

```python
"""
Automated Data Intake & Processing Pipeline
Drop files in input/ folder, run once, dashboard updates
"""

import os
import shutil
from pathlib import Path

# 1. Move files from input/ to proper locations
def organize_inputs():
    input_dir = Path('input')
    
    for file in input_dir.glob('*trip_activity*.csv'):
        shutil.copy(file, f'data/consolidated/trips/{file.name}')
    
    for file in input_dir.glob('*payment_activity*.csv'):
        shutil.copy(file, f'data/consolidated/payments/{file.name}')
    
    for file in input_dir.glob('*bank*.csv'):
        shutil.copy(file, f'bank/{file.name}')
    
    for file in input_dir.glob('*refund*.csv'):
        shutil.copy(file, 'bank/refund_status.csv')

# 2. Run all analysis scripts
def run_analysis():
    os.system('python analysis/audit_trail_export.py')
    os.system('python analysis/uber_only_reconciliation.py')
    os.system('python analysis/monthly_comprehensive_report.py')
    os.system('python analysis/four_way_reconciliation.py')

# 3. Start dashboard
def start_dashboard():
    os.system('streamlit run courier_insights.py')

if __name__ == '__main__':
    organize_inputs()
    run_analysis()
    start_dashboard()
```

**Usage**:
```
1. Create input/ folder
2. Dump CSVs into input/
3. python data_intake.py
4. Dashboard opens automatically with processed data
```

---

## Current State of Your Data

✅ **Complete**: You have all 4 data sources
✅ **Processed**: All analysis scripts are running successfully
✅ **Reconciled**: Multi-account reconciliation shows $263.57 gap (2.44% acceptable)
✅ **Delivered**: Dashboard displays all insights from processed data

The system is **fully operational**. A new user just needs to:
1. Export Uber trip & payment activity (monthly)
2. Get bank statement
3. Track refunds
4. Run the scripts
5. Open the dashboard

Done!
