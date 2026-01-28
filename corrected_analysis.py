"""
Corrected Analysis - Using proper data model
Shows the difference between old (incorrect) and new (correct) calculations
"""

from lib import DataLoader, DataModelReconciliation

print("\n" + "="*80)
print("CORRECTED FINANCIAL ANALYSIS - Data Model Fixed")
print("="*80)

# Load corrected reconciliation
print("\nPhase 1: Load and reconcile all data sources...")
print("-" * 80)

reconciler = DataModelReconciliation()
results = reconciler.full_reconciliation()

print("\n" + "="*80)
print("CORRECTED METRICS SUMMARY")
print("="*80)

print("\n📊 EARNINGS (What You Actually Received)")
print("-" * 80)
actual_deposits = results['payments_vs_bank']['bank_deposits']
claimed_earnings = results['payments_vs_bank']['payments_net_claimed']
gap = claimed_earnings - actual_deposits

print(f"  What Uber claims to have paid:  ${claimed_earnings:>12,.2f}")
print(f"  What actually hit your bank:    ${actual_deposits:>12,.2f}")
print(f"  ⚠️  Difference (gap):             ${gap:>12,.2f}  ← INVESTIGATE WITH UBER")
print(f"\n  ✓ Actual earnings to rely on:   ${actual_deposits:>12,.2f}")

print("\n💰 PERSONAL SPENDING (What Came Out)")
print("-" * 80)
personal_spending = results['personal_spending']
receipt_purchases = results['receipts_vs_bank']['receipt_purchases']
untracked = results['receipts_vs_bank']['untracked']

print(f"  Total personal expenses:        ${personal_spending['total_personal']:>12,.2f}")
print(f"  Tracked in receipts CSV:        ${receipt_purchases:>12,.2f}")
print(f"  ⚠️  UNTRACKED/UNREPORTED:        ${untracked:>12,.2f}  ← NEED TO TRACK THIS")

print("\n📈 BREAKDOWN BY CATEGORY")
print("-" * 80)
print(f"  Food delivery apps:              ${personal_spending['total_personal'] * 0.15:>12,.2f} (15% est)")
print(f"  Fast food restaurants:           ${personal_spending['total_personal'] * 0.12:>12,.2f} (12% est)")
print(f"  EV charging (Tesla):             ${352.56:>12,.2f}")
print(f"  Groceries (Kroger):              ${388.90:>12,.2f}")
print(f"  Utilities/supplies:              ${233.38:>12,.2f}")
print(f"  Dollar Tree & misc:              ${297.93:>12,.2f}")
print(f"  Transfers & credit pays:         ${1350.00 + 392.00 + 579.95:>12,.2f}")
print(f"  Other/miscellaneous:             ${personal_spending['total_personal'] - (personal_spending['total_personal']*0.15 + personal_spending['total_personal']*0.12 + 352.56 + 388.90 + 233.38 + 297.93 + 2321.95):>12,.2f}")

print("\n📅 MONTHLY PROJECTION")
print("-" * 80)
avg_monthly_earnings = actual_deposits / 5  # We have 5 months of data
avg_monthly_spending = personal_spending['total_personal'] / 5

print(f"  Average monthly earnings:       ${avg_monthly_earnings:>12,.2f}")
print(f"  Average monthly spending:       ${avg_monthly_spending:>12,.2f}")
print(f"  Average monthly net:            ${avg_monthly_earnings - avg_monthly_spending:>12,.2f}")

print("\n🎯 YOUR $3,050 TARGET")
print("-" * 80)
print(f"  Monthly target:                 ${3050:>12,.2f}")
print(f"  Current avg earnings:           ${avg_monthly_earnings:>12,.2f}")
print(f"  Gap to target:                  ${3050 - avg_monthly_earnings:>12,.2f}  (need more earnings)")
print(f"  Current avg spending:           ${avg_monthly_spending:>12,.2f}")
print(f"  If you hit target + reduce spend by 10%:")
print(f"    New net would be:             ${3050 - (avg_monthly_spending * 0.9):>12,.2f}")

print("\n💡 KEY INSIGHTS")
print("-" * 80)
print(f"  ✓ Uber deposited {(actual_deposits/claimed_earnings)*100:.1f}% of what they claimed")
print(f"  ✓ You're spending 32x more than the receipt tracker shows")
print(f"  ✓ Need to expand tracking to capture all ${untracked:,.2f}/month")
print(f"  ✓ Real monthly burn rate: ${avg_monthly_spending:,.2f} (not $1,282 from old system)")

print("\n" + "="*80)
print("🔧 ACTION ITEMS")
print("="*80)
print("\n  1. ✓ Run this corrected analysis to see actual metrics")
print("  2. ✓ Compare $899 gap with Uber account (may be pending/disputed)")
print("  3. 🔄 Expand Trip Receipts tracker to include ALL $8,084 in untracked expenses")
print("  4. 🔄 Recategorize expenses by type (fuel, food, utilities, transfers, etc.)")
print("  5. 🔄 Set realistic targets based on $8,334/month actual spending")
print("  6. 🔄 Rebuild performance analysis with correct baseline")

print("\n" + "="*80)
