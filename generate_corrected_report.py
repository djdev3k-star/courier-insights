"""
Complete Corrected Business Report
Generates comprehensive report using corrected data model
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / 'lib'))

from data_model_reconciliation import DataModelReconciliation
from data_loader import get_loader
from schedule_analyzer import ScheduleAnalyzer

print("\n" + "="*80)
print("COMPLETE CORRECTED COURIER BUSINESS REPORT")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Load data
loader = get_loader()
trips_df = loader.load_trip_data()

# Run corrected reconciliation
print("\nPhase 1: Data Model Reconciliation")
print("-" * 80)
reconciler = DataModelReconciliation()
results = reconciler.full_reconciliation()

# Extract corrected metrics
payments_vs_bank = results.get('payments_vs_bank', {})
personal_spending = results.get('personal_spending', {})
receipts_vs_bank = results.get('receipts_vs_bank', {})

actual_earnings = payments_vs_bank.get('bank_deposits', 0)
actual_spending = personal_spending.get('total_personal', 0)
earnings_gap = payments_vs_bank.get('difference', 0)
spending_untracked = receipts_vs_bank.get('untracked', 0)

# Monthly averages (5 months)
monthly_earnings = actual_earnings / 5
monthly_spending = actual_spending / 5
monthly_net = monthly_earnings - monthly_spending

# Schedule analysis
print("\nPhase 2: Schedule Optimization")
print("-" * 80)
schedule_analyzer = ScheduleAnalyzer(trips_df)
schedule_report = schedule_analyzer.get_detailed_report()

optimal_days = schedule_report['recommendations']['optimal_days']
peak_hours = schedule_report['recommendations']['peak_hours']
target_monthly = schedule_report['recommendations']['estimated_monthly_target']

print(f"✓ Optimal days: {', '.join(optimal_days)}")
print(f"✓ Peak hours: {peak_hours[0]}-{peak_hours[-1]}")
print(f"✓ Target monthly: ${target_monthly:,.2f}")

# Generate report
print("\n" + "="*80)
print("FINANCIAL SUMMARY (Corrected Data Model)")
print("="*80)

print("\n📊 EARNINGS (5 months)")
print("-" * 80)
print(f"  Uber claimed paid:       ${payments_vs_bank.get('payments_net_claimed', 0):>12,.2f}")
print(f"  Actually deposited:      ${actual_earnings:>12,.2f}")
print(f"  Gap (investigate):       ${abs(earnings_gap):>12,.2f}  {'⚠️' if abs(earnings_gap) > 100 else '✓'}")
print(f"\n  Monthly average:         ${monthly_earnings:>12,.2f}")

print("\n💰 SPENDING (5 months)")
print("-" * 80)
print(f"  Total personal expenses: ${actual_spending:>12,.2f}")
print(f"  Tracked in receipts:     ${receipts_vs_bank.get('receipt_purchases', 0):>12,.2f}")
print(f"  Untracked (need to add): ${spending_untracked:>12,.2f}  {'⚠️' if spending_untracked > 1000 else '✓'}")
print(f"\n  Monthly average:         ${monthly_spending:>12,.2f}")

print("\n📈 NET INCOME")
print("-" * 80)
print(f"  Total net (5 months):    ${actual_earnings - actual_spending:>12,.2f}")
print(f"  Monthly average net:     ${monthly_net:>12,.2f}")

print("\n🎯 PERFORMANCE VS TARGET")
print("-" * 80)
target = 3050
earnings_vs_target = monthly_earnings - target
spending_target = 1500
spending_vs_target = monthly_spending - spending_target

print(f"  Earnings target:         ${target:>12,.2f}/month")
print(f"  Actual earnings:         ${monthly_earnings:>12,.2f}/month")
print(f"  Gap:                     ${earnings_vs_target:>12,.2f}  {'✓ Exceeding' if earnings_vs_target > 0 else '⚠️ Below target'}")
print(f"\n  Spending target:         ${spending_target:>12,.2f}/month")
print(f"  Actual spending:         ${monthly_spending:>12,.2f}/month")
print(f"  Over/(Under):            ${spending_vs_target:>12,.2f}  {'⚠️ Overspending' if spending_vs_target > 0 else '✓ Under budget'}")

if monthly_net > 0:
    months_to_target = (target * 12) / monthly_net if monthly_net > 0 else 999
    print(f"\n  At current net (${monthly_net:,.2f}/mo):")
    print(f"    Annual net income:     ${monthly_net * 12:>12,.2f}")
    print(f"    To hit $3,050 target:  Increase earnings by ${abs(earnings_vs_target):,.2f}/month")

print("\n📅 SCHEDULE PERFORMANCE")
print("-" * 80)
print(f"  Total trips:             {len(trips_df):>12,}")
print(f"  Optimal days:            {', '.join(optimal_days)}")
print(f"  Peak hours:              {peak_hours[0]}-{peak_hours[-1]}")

# Top spending categories
print("\n💳 TOP SPENDING CATEGORIES")
print("-" * 80)
top_merchants = personal_spending.get('top_merchants', [])
if 'personal_spending' in results and len(top_merchants) > 0:
    print("  (See detailed breakdown in reconciliation output)")
else:
    print("  Tesla Supercharger, Kroger, WWW.HYPERFUEL.COM, Dollar Tree, etc.")
    print("  Run: python lib/data_model_reconciliation.py for details")

print("\n" + "="*80)
print("RECOMMENDATIONS")
print("="*80)

print("\n1. INVESTIGATE EARNINGS GAP")
if abs(earnings_gap) > 100:
    print(f"   ⚠️  Uber claims ${abs(earnings_gap):,.2f} more than deposited")
    print("   → Check your Uber Eats account for pending/disputed payments")

print("\n2. EXPAND RECEIPT TRACKING")
if spending_untracked > 1000:
    print(f"   ⚠️  ${spending_untracked:,.2f} of spending is untracked")
    print("   → Add all personal expenses to Trip Receipts tracker")
    print("   → Categorize: fuel, groceries, food, utilities, transfers")

print("\n3. INCREASE EARNINGS")
if monthly_earnings < target:
    print(f"   ⚠️  Currently earning ${monthly_earnings:,.2f}, need ${target:,.2f}")
    print(f"   → Need ${abs(earnings_vs_target):,.2f} more per month")
    print(f"   → Work during peak hours: {peak_hours[0]}-{peak_hours[-1]}")
    print(f"   → Focus on optimal days: {', '.join(optimal_days)}")

print("\n4. CONTROL SPENDING")
if monthly_spending > spending_target:
    print(f"   ⚠️  Spending ${monthly_spending:,.2f}, target ${spending_target:,.2f}")
    print(f"   → Reduce by ${abs(spending_vs_target):,.2f}/month")
    print("   → Focus on discretionary categories (food, utilities)")

print("\n" + "="*80)
print("NEXT STEPS")
print("="*80)
print("\n  1. Run: python corrected_analysis.py")
print("  2. Run: python lib/data_model_reconciliation.py")
print("  3. Update Trip Receipts CSV with untracked expenses")
print("  4. Set up expense categorization system")
print("  5. Monitor monthly against corrected baseline")

print("\n" + "="*80)
print(f"Report complete. All metrics use corrected data model.")
print("="*80)
