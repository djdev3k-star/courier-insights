"""
Automated Monthly Processing Pipeline
Run this script with new trip/payment/bank CSVs to generate all reports
"""
import sys
from pathlib import Path
import subprocess

def main():
    print("=" * 80)
    print("AUTOMATED COURIER RECONCILIATION PIPELINE")
    print("=" * 80)
    
    # Check data exists
    trips = list(Path('data/consolidated/trips').glob('*.csv'))
    payments = list(Path('data/consolidated/payments').glob('*.csv'))
    bank = list(Path('bank').glob('*.csv'))
    
    if not trips or not payments or not bank:
        print("\n[ERROR] Missing data files:")
        print(f"  Trips: {len(trips)} files")
        print(f"  Payments: {len(payments)} files")
        print(f"  Bank: {len(bank)} files")
        print("\nPlace CSV files in:")
        print("  - data/consolidated/trips/")
        print("  - data/consolidated/payments/")
        print("  - bank/")
        sys.exit(1)
    
    print(f"\n[OK] Found data:")
    print(f"  Trips: {len(trips)} files")
    print(f"  Payments: {len(payments)} files")
    print(f"  Bank: {len(bank)} files")
    
    # Run reports
    scripts = [
        ('Monthly Comprehensive Report', 'analysis/comprehensive_monthly_report.py'),
        ('Four-Way Reconciliation', 'analysis/four_way_reconciliation.py'),
        ('Audit Trail Export', 'analysis/audit_trail_export.py'),
        ('Refund Lag Report', 'analysis/refund_lag_report.py'),
        ('Bank Refund Enrichment', 'analysis/bank_refund_match.py')
    ]
    
    for name, script in scripts:
        print(f"\n[RUNNING] {name}...")
        try:
            exec(open(script, encoding='utf-8').read())
            print(f"[OK] {name} complete")
        except Exception as e:
            print(f"[ERROR] {name} failed: {e}")
    
    print("\n" + "=" * 80)
    print("PIPELINE COMPLETE")
    print("=" * 80)
    print("\nReports available in:")
    print("  - reports/monthly_comprehensive/")
    print("  - reports/four_way_reconciliation/")
    print("  - reports/audit_trail/")
    print("  - reports/refund_lag/")
    print("  - bank/bank_refund_status_enriched.csv")
    print("\nTo view dashboard: python -m streamlit run dashboard.py")

if __name__ == '__main__':
    main()
