"""
Repository Health Check - Phase 9 Corrected System
Verifies all files load and work together without broken logic
"""

import sys
from pathlib import Path

print("\n" + "="*80)
print("REPOSITORY HEALTH CHECK - Phase 9 Corrected System")
print("="*80)

errors = []
warnings = []
success = []

# Test 1: Component Library Imports
print("\n1. Testing Component Library Imports...")
try:
    from lib import (
        DataLoader,
        ExpenseCategorizer,
        ScheduleAnalyzer,
        SpendingAnalyzer,
        PerformanceAnalyzer,
        ReportGenerator,
        DataModelReconciliation
    )
    success.append("✓ All lib components import successfully")
    print("   ✓ DataLoader")
    print("   ✓ ExpenseCategorizer")
    print("   ✓ ScheduleAnalyzer")
    print("   ✓ SpendingAnalyzer")
    print("   ✓ PerformanceAnalyzer (corrected)")
    print("   ✓ ReportGenerator")
    print("   ✓ DataModelReconciliation (new)")
except ImportError as e:
    errors.append(f"✗ Component import failed: {e}")
    print(f"   ✗ ERROR: {e}")

# Test 2: Data Loading
print("\n2. Testing Data Loading...")
try:
    from lib import DataLoader
    loader = DataLoader()
    
    trips = loader.load_trip_data()
    print(f"   ✓ Trips: {len(trips)} records")
    
    payments = loader.load_payment_data()
    print(f"   ✓ Payments: {len(payments)} records")
    
    bank = loader.load_bank_statements()
    print(f"   ✓ Bank: {len(bank)} transactions")
    
    receipts = loader.load_receipts()
    print(f"   ✓ Receipts: {len(receipts)} entries")
    
    success.append("✓ All data sources load successfully")
except Exception as e:
    errors.append(f"✗ Data loading failed: {e}")
    print(f"   ✗ ERROR: {e}")

# Test 3: Data Model Reconciliation
print("\n3. Testing Data Model Reconciliation...")
try:
    from lib import DataModelReconciliation
    
    reconciler = DataModelReconciliation()
    reconciler.load_all()
    
    # Test individual reconciliations
    r1 = reconciler.reconcile_trips_to_payments()
    r2 = reconciler.reconcile_payments_to_bank()
    r3 = reconciler.analyze_personal_spending()
    r4 = reconciler.analyze_receipts_vs_bank()
    
    if r1 and r2 and r3 and r4:
        success.append("✓ Data model reconciliation works")
        print("   ✓ Trips → Payments reconciliation")
        print("   ✓ Payments → Bank reconciliation")
        print("   ✓ Personal spending analysis")
        print("   ✓ Receipts vs Bank analysis")
    else:
        warnings.append("⚠ Some reconciliation methods returned empty")
        print("   ⚠ Some reconciliation methods returned empty results")
except Exception as e:
    errors.append(f"✗ Reconciliation failed: {e}")
    print(f"   ✗ ERROR: {e}")

# Test 4: Schedule Analysis
print("\n4. Testing Schedule Analysis...")
try:
    from lib import ScheduleAnalyzer, DataLoader
    
    loader = DataLoader()
    trips = loader.load_trip_data()
    
    analyzer = ScheduleAnalyzer(trips)
    by_day = analyzer.analyze_by_day()
    by_hour = analyzer.analyze_by_hour()
    optimal = analyzer.get_optimal_schedule()
    
    if len(by_day) > 0 and len(by_hour) > 0 and optimal:
        success.append("✓ Schedule analysis works")
        print(f"   ✓ By day analysis: {len(by_day)} days")
        print(f"   ✓ By hour analysis: {len(by_hour)} hours")
        print(f"   ✓ Optimal schedule calculated")
    else:
        warnings.append("⚠ Schedule analysis returned incomplete results")
except Exception as e:
    errors.append(f"✗ Schedule analysis failed: {e}")
    print(f"   ✗ ERROR: {e}")

# Test 5: Expense Categorization
print("\n5. Testing Expense Categorization...")
try:
    from lib import ExpenseCategorizer, DataLoader
    
    loader = DataLoader()
    bank = loader.load_bank_statements()
    
    categorizer = ExpenseCategorizer()
    categorized = categorizer.analyze_dataframe(
        bank, 
        'Description', 
        'Description'
    )
    
    if len(categorized) > 0:
        success.append("✓ Expense categorization works")
        print(f"   ✓ Categorized {len(categorized)} transactions")
        summary = categorizer.get_summary()
        print(f"   ✓ Summary generated: {len(summary['by_category'])} categories")
    else:
        warnings.append("⚠ Expense categorization returned no results")
except Exception as e:
    errors.append(f"✗ Expense categorization failed: {e}")
    print(f"   ✗ ERROR: {e}")

# Test 6: Performance Analysis (Corrected)
print("\n6. Testing Performance Analysis (Corrected)...")
try:
    from lib import PerformanceAnalyzer, DataLoader
    
    loader = DataLoader()
    trips = loader.load_trip_data()
    bank = loader.load_bank_statements()
    
    analyzer = PerformanceAnalyzer(trips, None, bank)
    
    # Test corrected earnings analysis
    earnings = analyzer.analyze_earnings(target_monthly=3050)
    
    # Test corrected spending analysis
    spending = analyzer.analyze_spending_control(target_monthly=1500)
    
    if earnings and spending and 'error' not in earnings and 'error' not in spending:
        success.append("✓ Performance analysis works (corrected)")
        print(f"   ✓ Earnings analysis: ${earnings.get('monthly_average', 0):,.2f}/mo")
        print(f"   ✓ Spending analysis: ${spending.get('monthly_average', 0):,.2f}/mo")
    else:
        warnings.append("⚠ Performance analysis returned errors or incomplete data")
        print(f"   ⚠ Earnings: {earnings}")
        print(f"   ⚠ Spending: {spending}")
except Exception as e:
    errors.append(f"✗ Performance analysis failed: {e}")
    print(f"   ✗ ERROR: {e}")

# Test 7: Corrected Analysis Scripts
print("\n7. Testing Corrected Analysis Scripts...")
script_tests = [
    ('corrected_analysis.py', 'Corrected analysis'),
    ('generate_corrected_report.py', 'Report generator'),
    ('analysis/four_way_reconciliation_CORRECTED.py', 'Four-way reconciliation'),
]

for script_path, script_name in script_tests:
    path = Path(script_path)
    if path.exists():
        success.append(f"✓ {script_name} exists")
        print(f"   ✓ {script_name}: {script_path}")
    else:
        warnings.append(f"⚠ {script_name} not found")
        print(f"   ⚠ {script_name} not found at {script_path}")

# Test 8: Documentation Files
print("\n8. Testing Documentation Files...")
doc_tests = [
    ('QUICK_REFERENCE_PHASE9.md', 'Quick reference'),
    ('CALCULATION_ERROR_REPORT.md', 'Error report'),
    ('DATA_MODEL_CORRECTION_SUMMARY.md', 'Correction summary'),
    ('PHASE_9_COMPLETE.md', 'Phase 9 completion'),
    ('PHASE_9_INDEX.md', 'File index'),
]

for doc_path, doc_name in doc_tests:
    path = Path(doc_path)
    if path.exists():
        success.append(f"✓ {doc_name} exists")
        print(f"   ✓ {doc_name}")
    else:
        warnings.append(f"⚠ {doc_name} not found")
        print(f"   ⚠ {doc_name} not found")

# Summary
print("\n" + "="*80)
print("HEALTH CHECK SUMMARY")
print("="*80)

print(f"\n✓ SUCCESS: {len(success)} checks passed")
for s in success[:5]:  # Show first 5
    print(f"   {s}")
if len(success) > 5:
    print(f"   ... and {len(success) - 5} more")

if warnings:
    print(f"\n⚠ WARNINGS: {len(warnings)} issues")
    for w in warnings:
        print(f"   {w}")

if errors:
    print(f"\n✗ ERRORS: {len(errors)} critical issues")
    for e in errors:
        print(f"   {e}")
else:
    print("\n✗ ERRORS: None")

# Overall status
print("\n" + "="*80)
if len(errors) == 0:
    if len(warnings) == 0:
        print("STATUS: ✓ PERFECT - All systems operational")
    else:
        print(f"STATUS: ⚠ GOOD - {len(warnings)} warnings (non-critical)")
else:
    print(f"STATUS: ✗ ISSUES - {len(errors)} errors need attention")
print("="*80)

# Exit code
sys.exit(len(errors))
