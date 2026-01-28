"""
Enhanced Reimbursement Reconciliation with Batch Detection

Cross-references:
1. Uber Payments - Individual refund transactions (Order Value + Toll)
2. Trips Data - Trip details (no refund amounts, just trip info)
3. Receipt Tracker - Manually tracked reimbursements
4. Bank Statements - Actual deposits (may be batched)

Key insight: Bank may receive ONE payment that equals MULTIPLE refunds combined
"""

import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from itertools import combinations

def load_all_payments():
    """Load all payment data including Order Value and Toll refunds"""
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    payments_path = base_path / 'data' / 'consolidated' / 'payments'
    
    all_payments = []
    
    for csv_file in sorted(payments_path.glob('*.csv')):
        df = pd.read_csv(csv_file)
        all_payments.append(df)
    
    combined = pd.concat(all_payments, ignore_index=True)
    
    # Parse date from vs reporting
    combined['Date'] = combined['vs reporting'].str.split(' -').str[0]
    combined['Date'] = pd.to_datetime(combined['Date'], errors='coerce')
    
    # Get refund columns
    refund_order_col = 'Paid to you:Trip balance:Refunds:Order Value'
    refund_toll_col = 'Paid to you:Trip balance:Refunds:Toll'
    
    # Filter for any refund > 0
    refunds = combined[
        (combined[refund_order_col] > 0) | (combined[refund_toll_col] > 0)
    ].copy()
    
    # Calculate total refund amount
    refunds['Refund_Amount'] = (
        refunds[refund_order_col].fillna(0) + 
        refunds[refund_toll_col].fillna(0)
    )
    
    # Add components
    refunds['Order_Refund'] = refunds[refund_order_col].fillna(0)
    refunds['Toll_Refund'] = refunds[refund_toll_col].fillna(0)
    
    return refunds[refunds['Date'].notna()]


def load_bank_statements():
    """Load bank statements and filter for incoming payments"""
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    bank_path = base_path / 'data' / 'bank'
    
    all_statements = []
    
    for csv_file in sorted(bank_path.glob('*.csv')):
        if 'Statement' in csv_file.name:
            df = pd.read_csv(csv_file)
            all_statements.append(df)
    
    combined = pd.concat(all_statements, ignore_index=True)
    
    # Parse dates and amounts
    combined['Posted Date'] = pd.to_datetime(combined['Posted Date'], errors='coerce')
    combined['Amount'] = pd.to_numeric(
        combined['Amount'].astype(str).str.replace('$', '').str.replace(',', ''), 
        errors='coerce'
    )
    
    # Only positive amounts (credits/deposits)
    deposits = combined[combined['Amount'] > 0].copy()
    
    return deposits


def load_receipt_tracker():
    """Load manually tracked receipts"""
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    receipt_file = base_path / 'data' / 'receipts' / 'Trip Receipts-Refund Tracker.csv'
    
    if not receipt_file.exists():
        return pd.DataFrame()
    
    df = pd.read_csv(receipt_file)
    
    # Parse dates
    for col in ['Date', 'Trip Date', 'Refund Date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Get refund amounts
    if 'Refund Amount' in df.columns:
        df['Refund_Amount'] = pd.to_numeric(
            df['Refund Amount'].astype(str).str.replace('$', '').str.replace(',', ''), 
            errors='coerce'
        )
    
    return df


def find_batched_refunds(refunds_df, target_amount, target_date, date_window=7, tolerance=0.50):
    """
    Find combinations of refunds that sum to a bank deposit amount
    This handles cases where Uber batches multiple refunds into one payment
    """
    # Get refunds within date window
    nearby_refunds = refunds_df[
        (refunds_df['Date'] >= target_date - timedelta(days=date_window)) &
        (refunds_df['Date'] <= target_date + timedelta(days=date_window))
    ]
    
    if nearby_refunds.empty:
        return None
    
    # Try to find exact match first
    exact_matches = nearby_refunds[
        (nearby_refunds['Refund_Amount'] >= target_amount - tolerance) &
        (nearby_refunds['Refund_Amount'] <= target_amount + tolerance)
    ]
    
    if not exact_matches.empty:
        return {'type': 'single', 'refunds': [exact_matches.iloc[0].to_dict()]}
    
    # Try combinations of 2-5 refunds
    for combo_size in range(2, min(6, len(nearby_refunds) + 1)):
        for combo_indices in combinations(range(len(nearby_refunds)), combo_size):
            combo_refunds = nearby_refunds.iloc[list(combo_indices)]
            combo_sum = combo_refunds['Refund_Amount'].sum()
            
            if abs(combo_sum - target_amount) <= tolerance:
                return {
                    'type': 'batch',
                    'refunds': combo_refunds.to_dict('records'),
                    'combo_sum': combo_sum
                }
    
    return None


def reconcile_with_batching():
    """Enhanced reconciliation with batch detection"""
    
    print("=" * 80)
    print("ENHANCED REIMBURSEMENT RECONCILIATION WITH BATCH DETECTION")
    print("=" * 80)
    print()
    
    # Load all data
    print("Loading data sources...")
    refunds_df = load_all_payments()
    bank_df = load_bank_statements()
    receipts_df = load_receipt_tracker()
    
    print(f"  Refund transactions: {len(refunds_df)}")
    print(f"  Bank deposits: {len(bank_df)}")
    print(f"  Receipt tracker: {len(receipts_df)}")
    print()
    
    total_refunds = refunds_df['Refund_Amount'].sum()
    print(f"Total Uber Refunds: ${total_refunds:,.2f}")
    print(f"  Order Value: ${refunds_df['Order_Refund'].sum():,.2f}")
    print(f"  Toll: ${refunds_df['Toll_Refund'].sum():,.2f}")
    print()
    
    # Track matched refunds
    matched_refund_ids = set()
    reconciliation = []
    
    # Filter bank for likely Uber payments
    uber_keywords = ['uber', 'eats', 'technologies', 'pending']
    bank_uber = bank_df[
        bank_df['Description'].astype(str).str.lower().str.contains('|'.join(uber_keywords), na=False)
    ]
    
    print(f"Bank deposits mentioning Uber: {len(bank_uber)}")
    print()
    
    print("=" * 80)
    print("ANALYZING BANK DEPOSITS FOR BATCH PAYMENTS")
    print("=" * 80)
    print()
    
    for _, bank_deposit in bank_uber.iterrows():
        deposit_date = bank_deposit['Posted Date']
        deposit_amount = bank_deposit['Amount']
        deposit_desc = bank_deposit['Description']
        
        # Create a copy of refunds not yet matched
        unmatched_refunds = refunds_df[
            ~refunds_df.index.isin(matched_refund_ids)
        ].copy()
        
        # Try to find matching refunds (single or batched)
        match_result = find_batched_refunds(
            unmatched_refunds, 
            deposit_amount, 
            deposit_date,
            date_window=10
        )
        
        if match_result:
            record = {
                'Bank_Date': deposit_date,
                'Bank_Amount': deposit_amount,
                'Bank_Description': deposit_desc,
                'Match_Type': match_result['type'],
                'Refund_Count': len(match_result['refunds']),
                'Refund_Details': match_result['refunds']
            }
            
            # Mark refunds as matched
            for refund in match_result['refunds']:
                # Find the index in original dataframe
                matching_idx = refunds_df[
                    (refunds_df['Date'] == refund['Date']) &
                    (refunds_df['Refund_Amount'] == refund['Refund_Amount'])
                ].index
                matched_refund_ids.update(matching_idx)
            
            reconciliation.append(record)
            
            # Display
            month = deposit_date.strftime('%Y-%m')
            match_type = "BATCH" if match_result['type'] == 'batch' else "SINGLE"
            print(f"{month} | {match_type:6} | Bank: ${deposit_amount:7.2f} | {len(match_result['refunds'])} refunds")
            
            for refund in match_result['refunds']:
                refund_date = pd.to_datetime(refund['Date']).strftime('%m/%d')
                print(f"         └─ {refund_date} | ${refund['Refund_Amount']:6.2f} | {refund.get('Description', '')[:40]}")
            
            print()
    
    # Summary
    print("=" * 80)
    print("RECONCILIATION SUMMARY")
    print("=" * 80)
    print()
    
    total_matched_amount = sum(r['Bank_Amount'] for r in reconciliation)
    batch_count = sum(1 for r in reconciliation if r['Match_Type'] == 'batch')
    single_count = sum(1 for r in reconciliation if r['Match_Type'] == 'single')
    
    print(f"Total Bank Deposits Matched: ${total_matched_amount:,.2f}")
    print(f"Total Uber Refunds Claimed: ${total_refunds:,.2f}")
    print(f"Difference: ${total_matched_amount - total_refunds:,.2f}")
    print()
    print(f"Single Matches: {single_count}")
    print(f"Batch Matches: {batch_count}")
    print(f"Total Refunds Matched: {len(matched_refund_ids)} of {len(refunds_df)}")
    print()
    
    # Unmatched refunds
    unmatched_refunds = refunds_df[~refunds_df.index.isin(matched_refund_ids)]
    if not unmatched_refunds.empty:
        print(f"⚠ UNMATCHED REFUNDS: {len(unmatched_refunds)} (${unmatched_refunds['Refund_Amount'].sum():,.2f})")
        print("\nUnmatched refunds by month:")
        for month in sorted(unmatched_refunds['Date'].dt.to_period('M').unique()):
            month_unmatched = unmatched_refunds[unmatched_refunds['Date'].dt.to_period('M') == month]
            print(f"  {month}: {len(month_unmatched)} refunds, ${month_unmatched['Refund_Amount'].sum():.2f}")
    
    # Export results
    export_df = pd.DataFrame(reconciliation)
    export_df.to_json('reimbursement_batch_analysis.json', orient='records', date_format='iso', indent=2)
    print(f"\n✓ Exported detailed analysis: reimbursement_batch_analysis.json")
    
    return reconciliation, matched_refund_ids


if __name__ == '__main__':
    reconcile_with_batching()
