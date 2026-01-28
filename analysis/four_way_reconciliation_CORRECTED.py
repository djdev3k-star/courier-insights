"""
CORRECTED Four-Way Reconciliation
Uses proper data model: Trips (metadata), Payments (claims), Bank (actual), Receipts (refunds)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))

from data_model_reconciliation import DataModelReconciliation

print("\n" + "="*80)
print("CORRECTED FOUR-WAY RECONCILIATION")
print("="*80)
print("\nThis uses the corrected data model:")
print("  • Trips table = Trip metadata (count, timing, locations)")
print("  • Payments table = What Uber CLAIMS to have paid")
print("  • Bank (Uber Pro) = What ACTUALLY was deposited")
print("  • Receipts = Customer purchases expecting refunds")
print("\n" + "="*80)

# Run corrected reconciliation
reconciler = DataModelReconciliation()
results = reconciler.full_reconciliation()

print("\n" + "="*80)
print("SUMMARY")
print("="*80)

# Extract key metrics
trips_vs_payments = results.get('trips_vs_payments', {})
payments_vs_bank = results.get('payments_vs_bank', {})
personal_spending = results.get('personal_spending', {})
receipts_vs_bank = results.get('receipts_vs_bank', {})

print("\n1. EARNINGS RECONCILIATION")
print(f"   Payments claimed:  ${payments_vs_bank.get('payments_net_claimed', 0):>12,.2f}")
print(f"   Bank deposits:     ${payments_vs_bank.get('bank_deposits', 0):>12,.2f}")
print(f"   Gap:               ${abs(payments_vs_bank.get('difference', 0)):>12,.2f}  {'✓' if abs(payments_vs_bank.get('difference', 0)) < 10 else '⚠️ INVESTIGATE'}")

print("\n2. SPENDING RECONCILIATION")
print(f"   Receipt tracker:   ${receipts_vs_bank.get('receipt_purchases', 0):>12,.2f}")
print(f"   Bank personal:     ${receipts_vs_bank.get('bank_personal', 0):>12,.2f}")
print(f"   Untracked:         ${receipts_vs_bank.get('untracked', 0):>12,.2f}  {'✓' if receipts_vs_bank.get('untracked', 0) < 100 else '⚠️ NEED TO TRACK'}")

print("\n3. MONTHLY AVERAGES (5 months data)")
avg_earnings = payments_vs_bank.get('bank_deposits', 0) / 5
avg_spending = personal_spending.get('total_personal', 0) / 5
avg_net = avg_earnings - avg_spending

print(f"   Earnings/month:    ${avg_earnings:>12,.2f}")
print(f"   Spending/month:    ${avg_spending:>12,.2f}")
print(f"   Net/month:         ${avg_net:>12,.2f}")

print("\n4. VS YOUR $3,050 TARGET")
target = 3050
gap = target - avg_earnings
print(f"   Target:            ${target:>12,.2f}")
print(f"   Actual:            ${avg_earnings:>12,.2f}")
print(f"   Gap:               ${gap:>12,.2f}  {'✓ EXCEEDING' if gap < 0 else '⚠️ NEED MORE EARNINGS'}")

print("\n" + "="*80)
print("STATUS: Reconciliation complete with corrected data model")
print("="*80)
