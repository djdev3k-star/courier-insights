# Getting Started with Modular Components

**Quick Reference for Using the New Component Architecture**

---

## 🚀 Quick Start

### Option 1: Full Integrated Analysis (Easiest)

```bash
cd lib
python courier_analytics.py
```

This runs the complete analysis workflow using all components.

---

### Option 2: Use Individual Components

#### Load Data
```python
from lib import DataLoader

loader = DataLoader()
trips = loader.load_trip_data()        # 1,077 trips
bank = loader.load_bank_statements()   # 2,294 transactions
payments = loader.load_payment_data()
receipts = loader.load_receipts()
```

#### Categorize Expenses
```python
from lib import ExpenseCategorizer

categorizer = ExpenseCategorizer()
categorized = categorizer.analyze_dataframe(bank)

# Get summary
summary = categorizer.get_summary()
print(f"Reimbursable: ${summary['reimbursable']:.2f}")
print(f"Personal: ${summary['personal']:.2f}")
```

#### Analyze Schedule
```python
from lib import ScheduleAnalyzer

scheduler = ScheduleAnalyzer(trips)
peak_hours = scheduler.get_peak_hours()           # [18, 19, 20, 21, 22, 23]
recommendations = scheduler.get_optimal_schedule()
print(f"Monthly Target: ${recommendations['estimated_monthly_target']}")
```

#### Analyze Spending Patterns
```python
from lib import SpendingAnalyzer

spender = SpendingAnalyzer(bank, trips)
by_day = spender.analyze_by_day_of_week()
merchants = spender.identify_high_spending_merchants(10)
```

#### Compare Performance
```python
from lib import PerformanceAnalyzer

perf = PerformanceAnalyzer(trips, bank)
adherence = perf.analyze_schedule_adherence(
    optimal_days=['Tuesday', 'Wednesday', 'Saturday'],
    peak_hours=[18, 19, 20, 21, 22, 23]
)
print(f"Grade: {adherence['grade']}")
print(f"Adherence: {adherence['overall_adherence_percent']:.1f}%")
```

#### Generate Reports
```python
from lib import ReportGenerator

gen = ReportGenerator()
header = gen.generate_header("My Report", "Subtitle")
schedule_report = gen.generate_schedule_optimization_report(schedule_data)
```

---

### Option 3: Unified Framework

```python
from lib import CourierAnalytics

# Initialize
analytics = CourierAnalytics()

# Run complete analysis
results = analytics.run_full_analysis()

# Or run individual analyses
schedule_analyzer = analytics.analyze_schedule()
expenses, categorizer = analytics.analyze_expenses()
spending = analytics.analyze_spending_patterns()
performance = analytics.analyze_performance(
    optimal_days=['Tuesday', 'Wednesday', 'Saturday'],
    peak_hours=[18, 19, 20, 21, 22, 23]
)
```

---

## 📊 Component Capabilities

### DataLoader
```
✓ Load trip data
✓ Load payment data
✓ Load bank statements
✓ Load receipts
✓ Automatic caching
✓ Error handling
```

### ExpenseCategorizer
```
✓ 17 expense categories
✓ Reimbursable/Personal classification
✓ Merchant keyword matching
✓ Summary statistics
✓ Category breakdown
```

### ScheduleAnalyzer
```
✓ Daily analysis (by day of week)
✓ Hourly analysis
✓ Peak hour identification
✓ Efficiency metrics ($/mile, per trip)
✓ Schedule recommendations
✓ Inefficient hour detection
```

### SpendingAnalyzer
```
✓ Daily spending patterns
✓ Hourly spending patterns
✓ Merchant analysis (top spenders)
✓ Category breakdown
✓ Trip correlation
✓ Anomaly detection
```

### PerformanceAnalyzer
```
✓ Schedule adherence grade (A-F)
✓ Earnings vs target comparison
✓ Spending vs target comparison
✓ Merchant-specific analysis
✓ Savings potential calculation
```

### ReportGenerator
```
✓ Markdown formatting
✓ Table generation
✓ Header/section creation
✓ Metric formatting
✓ Multiple report types
```

---

## 🔄 Data Flow Example

```python
# 1. Load data
loader = DataLoader()
trips = loader.load_trip_data()
bank = loader.load_bank_statements()

# 2. Categorize expenses
categorizer = ExpenseCategorizer()
categorized = categorizer.analyze_dataframe(bank)
expense_summary = categorizer.get_summary()

# 3. Analyze schedule
scheduler = ScheduleAnalyzer(trips)
peak_hours = scheduler.get_peak_hours()
recommendations = scheduler.get_optimal_schedule()

# 4. Analyze spending
spender = SpendingAnalyzer(categorized, trips)
spending_by_day = spender.analyze_by_day_of_week()
merchants = spender.identify_high_spending_merchants()

# 5. Analyze performance
perf = PerformanceAnalyzer(trips, categorized)
adherence = perf.analyze_schedule_adherence(
    recommendations['optimal_days'],
    recommendations['peak_hours']
)
earnings = perf.analyze_earnings(3050)
spending = perf.analyze_spending_control(811)

# 6. Generate report
gen = ReportGenerator()
report = gen.generate_performance_report(adherence, earnings, spending)
print(report)
```

---

## 📈 Key Metrics

### Schedule Optimization
- **Peak Hours:** 18:00 - 23:00 (6 PM - 11 PM)
- **Optimal Days:** Tuesday, Wednesday, Saturday
- **Monthly Target:** $3,050
- **Current Achievement:** 33.3% (F Grade)

### Expense Breakdown
- **Total Analyzed:** 2,294 transactions
- **Reimbursable:** $1,158 (18.1%)
- **Personal:** $5,250 (81.9%)
- **Top Merchant:** Raising Canes ($814)

### Performance vs Targets
- **Schedule Adherence:** 33.3% (F)
- **Monthly Earnings:** $1,282 vs $3,050 target (-$1,768)
- **Monthly Spending:** $1,282 vs $811 target (+$471)
- **Savings Potential:** $5,640/year

---

## 🔗 Integration with Existing Scripts

All original scripts continue to work:
- ✓ `expense_analyzer.py` - Still functional
- ✓ `schedule_optimizer.py` - Still functional
- ✓ `dashboard.py` - Still functional
- ✓ All existing reports - Preserved
- ✓ All calculations - Unchanged

**New components can be used alongside existing scripts or gradually replace them.**

---

## 💡 Common Patterns

### Pattern 1: Quick Summary
```python
from lib import CourierAnalytics

analytics = CourierAnalytics()
results = analytics.run_full_analysis()
```

### Pattern 2: Focused Analysis
```python
from lib import ScheduleAnalyzer, DataLoader

loader = DataLoader()
scheduler = ScheduleAnalyzer(loader.load_trip_data())
print(scheduler.get_peak_hours())
```

### Pattern 3: Custom Workflow
```python
from lib import *

# Load once
loader = DataLoader()
trips = loader.load_trip_data()
bank = loader.load_bank_statements()

# Reuse across components
for component in [ScheduleAnalyzer(trips), SpendingAnalyzer(bank, trips)]:
    component.analyze()  # or individual methods
```

### Pattern 4: Export Results
```python
from lib import ReportGenerator

gen = ReportGenerator()
report_md = gen.generate_schedule_optimization_report(schedule_data)

# Save to file
with open('reports/generated_report.md', 'w') as f:
    f.write(report_md)
```

---

## 🛠️ Customization

### Custom Categories
```python
categorizer = ExpenseCategorizer()
# Add custom rules
categorizer.CATEGORIES['custom'] = {
    'keywords': ['my_keyword'],
    'type': 'personal',
    'description': 'My Category'
}
```

### Custom Time Windows
```python
scheduler = ScheduleAnalyzer(trips)
# Get peak hours at different percentile
peak_85 = scheduler.get_peak_hours(threshold_percentile=85)
peak_90 = scheduler.get_peak_hours(threshold_percentile=90)
```

### Custom Merchants
```python
spender = SpendingAnalyzer(bank, trips)
raising_canes = spender.identify_high_spending_merchants(
    top_n=20
).filter('Raising Canes')
```

---

## 📚 Full Documentation

For detailed documentation, see:
- [COMPONENT_ARCHITECTURE.md](COMPONENT_ARCHITECTURE.md) - Complete architecture guide
- Component docstrings in `lib/*.py` files
- [README.md](../README.md) - Overall project guide

---

## ✅ Verification Checklist

- [ ] Can import components: `from lib import DataLoader`
- [ ] Data loads correctly: 1,077 trips, 2,294 transactions
- [ ] Schedule analysis shows peak hours: 18-23
- [ ] Expense summary totals match
- [ ] Performance grade calculates correctly
- [ ] Reports generate in markdown format
- [ ] All existing scripts still work
- [ ] No data has been modified or lost

---

## 🚀 Next Steps

1. **Explore Components** - Try each component individually
2. **Run Full Analysis** - Use CourierAnalytics to run everything
3. **Integrate Gradually** - Replace one script at a time
4. **Build Custom Tools** - Create specialized analyses using components
5. **Automate Workflow** - Schedule regular analysis runs

---

**Components Ready to Use! 🎉**

All calculations, functions, and data preserved. Zero breaking changes. Full backward compatibility with existing scripts.
