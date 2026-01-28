# Courier Business Analytics - Component Architecture

**Date:** January 28, 2026  
**Version:** 1.0.0  
**Status:** Production Ready

---

## 🏗️ System Overview

The Courier Analytics system is built on modular, reusable components that work together to provide comprehensive business intelligence. Each component has a single responsibility and can be used independently or as part of the integrated framework.

```
┌─────────────────────────────────────────────────────────────┐
│        UNIFIED ANALYSIS FRAMEWORK                           │
│        (courier_analytics.py)                               │
│                                                             │
│  Orchestrates all components, manages workflow              │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┼──────────┬───────────┬─────────────┐
        │          │          │           │             │
        ▼          ▼          ▼           ▼             ▼
    ┌────────┐ ┌────────┐ ┌────────┐ ┌───────────┐ ┌─────────────┐
    │ DATA   │ │EXPENSE │ │SCHEDULE│ │ SPENDING  │ │ PERFORMANCE │
    │ LOADER │ │CATEGORIZER│ANALYZER│ │ ANALYZER  │ │ ANALYZER    │
    └────────┘ └────────┘ └────────┘ └───────────┘ └─────────────┘
        │          │          │           │             │
        └──────────┴──────────┴───────────┴─────────────┘
                   │
                   ▼
           ┌──────────────────┐
           │ REPORT GENERATOR │
           └──────────────────┘
                   │
                   ▼
        Markdown Reports, Visualizations
```

---

## 📦 Component Details

### 1. **DataLoader** (`lib/data_loader.py`)

**Purpose:** Centralized data loading with caching

**Responsibilities:**
- Load trip data from consolidated CSV files
- Load payment data
- Load bank statements
- Load receipt/refund data
- Cache loaded data to avoid reloading
- Handle errors gracefully

**Key Methods:**
```python
loader = DataLoader()
trips = loader.load_trip_data()
bank = loader.load_bank_statements()
payments = loader.load_payment_data()
receipts = loader.load_receipts()
```

**Data Handled:**
- 1,077 trips (Aug-Dec 2025)
- 2,294 bank transactions
- Payment records
- Receipt data

---

### 2. **ExpenseCategorizer** (`lib/expense_categorizer.py`)

**Purpose:** Intelligent expense categorization into 17 categories

**Responsibilities:**
- Categorize transactions by merchant keywords
- Classify as reimbursable, personal, or unknown
- Generate category statistics
- Support custom category rules

**Categories:**
- Food & Dining (8 categories)
- Transportation (tolls, ride-share)
- Vehicle (gas, maintenance, EV charging)
- Personal (groceries, retail, subscriptions, utilities)
- Other (fitness, entertainment, alcohol)

**Key Methods:**
```python
categorizer = ExpenseCategorizer()
categorized_df = categorizer.analyze_dataframe(expenses_df)
category_key, category_type, description = categorizer.categorize("Raising Canes")
summary = categorizer.get_summary()  # Statistics
```

**Output:**
- DataFrame with added columns: Category, Type, Category_Description
- Summary statistics: totals by type, category counts

---

### 3. **ScheduleAnalyzer** (`lib/schedule_analyzer.py`)

**Purpose:** Analyze trip patterns to optimize work schedule

**Responsibilities:**
- Analyze trips by day of week
- Analyze trips by hour of day
- Identify peak earning hours
- Calculate efficiency metrics
- Generate optimal schedule recommendations

**Key Methods:**
```python
scheduler = ScheduleAnalyzer(trips_df)
by_day = scheduler.analyze_by_day()  # Day statistics
by_hour = scheduler.analyze_by_hour()  # Hourly statistics
peak_hours = scheduler.get_peak_hours()  # List: [18, 19, 20, 21, 22, 23]
recommendations = scheduler.get_optimal_schedule()  # Dict with targets
efficiency = scheduler.analyze_efficiency()  # $/mile, trip metrics
```

**Analysis Output:**
- Peak hours: 6 PM - 11 PM
- Optimal days: (Top 3 by earnings)
- Monthly target: $3,050
- Efficiency: $12.34/mile avg

---

### 4. **SpendingAnalyzer** (`lib/spending_analyzer.py`)

**Purpose:** Analyze spending patterns and correlations

**Responsibilities:**
- Analyze spending by day of week
- Analyze spending by hour
- Identify high-spending merchants
- Correlate spending with trip activity
- Generate spending summaries

**Key Methods:**
```python
spender = SpendingAnalyzer(expenses_df, trips_df)
by_day = spender.analyze_by_day_of_week()
by_hour = spender.analyze_by_hour()
merchants = spender.identify_high_spending_merchants(top_n=10)
correlation = spender.correlate_with_trips()
summary = spender.get_spending_summary()
```

**Findings:**
- Highest spending: Sundays/Saturdays
- Raising Canes: $814 total, 27 visits
- 72% spending at pickup locations
- Correlation with restaurant pickups

---

### 5. **PerformanceAnalyzer** (`lib/performance_analyzer.py`)

**Purpose:** Compare actual performance against recommendations

**Responsibilities:**
- Analyze schedule adherence
- Compare earnings vs targets
- Compare spending vs targets
- Calculate performance grade (A-F)
- Estimate savings potential

**Key Methods:**
```python
perf = PerformanceAnalyzer(trips_df, expenses_df)
adherence = perf.analyze_schedule_adherence(optimal_days, peak_hours)
earnings = perf.analyze_earnings(target=3050)
spending = perf.analyze_spending_control(target=811)
savings = perf.calculate_savings_potential()
```

**Metrics:**
- Schedule Grade: F (33.3% adherence)
- Earnings: $1,282/month vs $3,050 target (-$1,768)
- Spending: $1,282/month vs $811 target (+$471 over)
- Annual savings potential: $5,640

---

### 6. **ReportGenerator** (`lib/report_generator.py`)

**Purpose:** Generate formatted reports from analysis results

**Responsibilities:**
- Generate markdown reports
- Format tables and metrics
- Create section headers
- Support multiple report types

**Key Methods:**
```python
gen = ReportGenerator()
schedule_md = gen.generate_schedule_optimization_report(data)
expense_md = gen.generate_expense_report(summary, merchants)
performance_md = gen.generate_performance_report(adherence, earnings, spending)
header = gen.generate_header("Report Title", "Subtitle")
section = gen.generate_section("Section Name", "Content")
```

---

### 7. **CourierAnalytics (Unified Framework)** (`lib/courier_analytics.py`)

**Purpose:** Orchestrate all components into cohesive workflow

**Responsibilities:**
- Initialize all components
- Manage data loading
- Coordinate analysis workflow
- Provide high-level API
- Run complete analysis

**Key Methods:**
```python
analytics = CourierAnalytics()
analytics.load_all_data()
analyzer = analytics.analyze_schedule()
categorized, categorizer = analytics.analyze_expenses()
spending = analytics.analyze_spending_patterns()
perf = analytics.analyze_performance(optimal_days, peak_hours)
results = analytics.run_full_analysis()  # Complete workflow
```

---

## 🔄 Data Flow

```
1. DATA LOADING
   ├─ Load trips.csv (1,077 records)
   ├─ Load payments.csv
   └─ Load bank statements.csv (2,294 transactions)

2. EXPENSE ANALYSIS
   ├─ Categorize transactions (17 categories)
   ├─ Calculate totals by type
   └─ Identify uncategorized items

3. SCHEDULE ANALYSIS
   ├─ Group trips by day/hour
   ├─ Calculate earnings statistics
   ├─ Identify peak hours
   └─ Generate recommendations

4. SPENDING ANALYSIS
   ├─ Correlate with trips
   ├─ Identify patterns
   └─ Highlight high-spending merchants

5. PERFORMANCE ANALYSIS
   ├─ Compare to recommendations
   ├─ Calculate adherence grade
   ├─ Estimate savings potential
   └─ Generate report

6. REPORT GENERATION
   ├─ Create markdown reports
   ├─ Format tables/metrics
   └─ Export to files
```

---

## 🎯 Usage Examples

### Example 1: Quick Analysis
```python
from lib import CourierAnalytics

analytics = CourierAnalytics()
results = analytics.run_full_analysis()
```

### Example 2: Component-Based Analysis
```python
from lib import DataLoader, ScheduleAnalyzer, ExpenseCategorizer

loader = DataLoader()
trips = loader.load_trip_data()
bank = loader.load_bank_statements()

# Analyze schedule
scheduler = ScheduleAnalyzer(trips)
peak_hours = scheduler.get_peak_hours()

# Categorize expenses
categorizer = ExpenseCategorizer()
categorized = categorizer.analyze_dataframe(bank)
summary = categorizer.get_summary()
```

### Example 3: Custom Analysis
```python
from lib import SpendingAnalyzer, PerformanceAnalyzer

spender = SpendingAnalyzer(bank, trips)
by_day = spender.analyze_by_day_of_week()
merchants = spender.identify_high_spending_merchants()

perf = PerformanceAnalyzer(trips, bank)
adherence = perf.analyze_schedule_adherence(['Tuesday', 'Wednesday'], [18, 19, 20])
```

---

## 🔧 Integration with Existing Scripts

All original scripts maintain full functionality. Components can be:
- **Used independently** - Each component works standalone
- **Integrated gradually** - Replace one script at a time
- **Combined with existing code** - Mix old and new approaches

### Backward Compatibility
✓ All existing reports still generate  
✓ All calculations preserved  
✓ No data loss or breaking changes  
✓ Can run alongside new components  

---

## 📊 Analysis Results Summary

| Component | Input | Output | Purpose |
|-----------|-------|--------|---------|
| DataLoader | CSV files | DataFrames | Centralized data access |
| ExpenseCategorizer | Bank transactions | Categorized expenses | Spending classification |
| ScheduleAnalyzer | Trip data | Peak hours, recommendations | Optimize work schedule |
| SpendingAnalyzer | Expenses + trips | Patterns, correlations | Understand spending behavior |
| PerformanceAnalyzer | Trips + expenses | Grades, comparisons | Measure vs targets |
| ReportGenerator | Analysis results | Markdown reports | Formatted output |

---

## 🚀 Next Steps

### Phase 1: Component Adoption
- [ ] Replace expense_analyzer.py with ExpenseCategorizer
- [ ] Replace schedule_optimizer.py with ScheduleAnalyzer
- [ ] Integrate existing reports with ReportGenerator

### Phase 2: Workflow Enhancement
- [ ] Create unified CLI tool using CourierAnalytics
- [ ] Add automated report generation on schedule
- [ ] Build dashboard using components

### Phase 3: Advanced Features
- [ ] Machine learning for anomaly detection
- [ ] Predictive spending forecasts
- [ ] Route optimization recommendations
- [ ] Customer segmentation analysis

---

## 📝 Files Structure

```
lib/
├── __init__.py                    # Package initialization
├── data_loader.py                 # DataLoader component
├── expense_categorizer.py         # ExpenseCategorizer component
├── schedule_analyzer.py           # ScheduleAnalyzer component
├── spending_analyzer.py           # SpendingAnalyzer component
├── performance_analyzer.py        # PerformanceAnalyzer component
├── report_generator.py            # ReportGenerator component
└── courier_analytics.py           # Unified framework

scripts/
├── (All existing scripts preserved)
└── use_components_example.py      # Example usage file

reports/
├── (All existing reports preserved)
└── (New reports from components)

data/
├── (All source data preserved)
└── (Cached data from loader)
```

---

## ⚙️ Configuration

No configuration needed - components use sensible defaults and auto-detect data paths.

To customize:
```python
analytics = CourierAnalytics(base_path='/custom/path')
loader = DataLoader('/custom/path')
```

---

## 🐛 Troubleshooting

**Issue:** "Module not found" error
- **Solution:** Ensure lib/ folder is in Python path or use: `sys.path.insert(0, 'lib')`

**Issue:** Data not loading
- **Solution:** Check file paths in data/ and bank/ folders match expected structure

**Issue:** Empty analysis results
- **Solution:** Verify data has required columns (Pickup Time, Fare Amount, Description, etc.)

---

## 📞 Support

For questions about:
- **Data loading:** See DataLoader docstrings
- **Categorization:** See ExpenseCategorizer.CATEGORIES
- **Analysis methods:** See individual component documentation
- **Integration:** See CourierAnalytics class

All components include comprehensive docstrings and type hints.

---

**Architecture designed for:**
✅ Modularity - Each component independent  
✅ Reusability - Use in multiple contexts  
✅ Testability - Easy to unit test  
✅ Maintainability - Clear responsibilities  
✅ Extensibility - Easy to add features  
✅ Backward compatibility - Works with existing code
