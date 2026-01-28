"""
Reimbursement Reconciliation Report

Cross-references:
1. Uber Payments - What Uber claims they paid as reimbursements
2. Trips Data - Actual trip details
3. Receipt Tracker - Manually tracked reimbursements
4. Bank Statements - Actual money received

Generates itemized monthly report showing matches/mismatches across all sources.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

def load_payments_data():
    """Load all Uber payments data"""
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    payments_path = base_path / 'data' / 'consolidated' / 'payments'
    
    all_payments = []
    
    if payments_path.exists():
        for csv_file in sorted(payments_path.glob('*.csv')):
            df = pd.read_csv(csv_file)
            all_payments.append(df)
    
    if all_payments:
        combined = pd.concat(all_payments, ignore_index=True)
        # Convert date columns
        if 'Date' in combined.columns:
            combined['Date'] = pd.to_datetime(combined['Date'])
        if 'Transfer Date' in combined.columns:
            combined['Transfer Date'] = pd.to_datetime(combined['Transfer Date'])
        return combined
    
    return pd.DataFrame()


def load_trips_data():
    """Load all trips data"""
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    trips_path = base_path / 'data' / 'consolidated' / 'trips'
    
    all_trips = []
    
    if trips_path.exists():
        for csv_file in sorted(trips_path.glob('*.csv')):
            df = pd.read_csv(csv_file)
            all_trips.append(df)
    
    if all_trips:
        combined = pd.concat(all_trips, ignore_index=True)
        # Convert date columns
        if 'Date' in combined.columns:
            combined['Date'] = pd.to_datetime(combined['Date'])
        if 'Trip Date' in combined.columns:
            combined['Trip Date'] = pd.to_datetime(combined['Trip Date'])
        return combined
    
    return pd.DataFrame()


def load_receipt_tracker():
    """Load manually tracked receipts"""
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    receipt_file = base_path / 'data' / 'receipts' / 'Trip Receipts-Refund Tracker.csv'
    
    if receipt_file.exists():
        df = pd.read_csv(receipt_file)
        
        # Parse dates - try multiple formats
        date_cols = ['Date', 'Trip Date', 'Refund Date']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Get refund amounts
        if 'Refund Amount' in df.columns:
            df['Refund_Amount'] = pd.to_numeric(df['Refund Amount'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')
        elif 'Amount' in df.columns:
            df['Refund_Amount'] = pd.to_numeric(df['Amount'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')
        
        return df
    
    return pd.DataFrame()


def load_bank_statements():
    """Load bank statement data"""
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    bank_path = base_path / 'data' / 'bank'
    
    all_statements = []
    
    if bank_path.exists():
        for csv_file in sorted(bank_path.glob('*.csv')):
            if 'Statement' in csv_file.name:
                df = pd.read_csv(csv_file)
                all_statements.append(df)
    
    if all_statements:
        combined = pd.concat(all_statements, ignore_index=True)
        
        # Parse dates
        if 'Posted Date' in combined.columns:
            combined['Posted Date'] = pd.to_datetime(combined['Posted Date'], errors='coerce')
        if 'Transaction Date' in combined.columns:
            combined['Transaction Date'] = pd.to_datetime(combined['Transaction Date'], errors='coerce')
        
        # Parse amounts
        if 'Amount' in combined.columns:
            combined['Amount'] = pd.to_numeric(combined['Amount'].astype(str).str.replace('$', '').str.replace(',', ''), errors='coerce')
        
        return combined
    
    return pd.DataFrame()


def find_matching_trip(reimbursement_row, trips_df, payments_df, date_window=7, amount_tolerance=5.0):
    """Find matching trip for a reimbursement using multiple matching strategies"""
    if trips_df.empty or payments_df.empty:
        return None
    
    reimb_date = reimbursement_row.get('Date')
    reimb_amount = reimbursement_row.get('Amount', 0)
    
    if pd.isna(reimb_date):
        return None
    
    # Strategy 1: Match by Trip UUID from payments data
    # Find the payment record that has this reimbursement
    trip_uuid = None
    
    if 'Trip UUID' in payments_df.columns:
        # Find payment rows with matching refund amount and date
        refund_col = 'Paid to you:Trip balance:Refunds:Order Value'
        
        # Parse dates in payments
        date_col_payments = 'vs reporting' if 'vs reporting' in payments_df.columns else None
        if date_col_payments:
            payments_df_temp = payments_df.copy()
            payments_df_temp['Payment_Date'] = payments_df_temp[date_col_payments].str.split(' -').str[0]
            payments_df_temp['Payment_Date'] = pd.to_datetime(payments_df_temp['Payment_Date'], errors='coerce')
            
            # Find matching payment
            matching_payments = payments_df_temp[
                (payments_df_temp['Payment_Date'] >= reimb_date - timedelta(days=date_window)) &
                (payments_df_temp['Payment_Date'] <= reimb_date + timedelta(days=date_window)) &
                (payments_df_temp[refund_col] >= reimb_amount - amount_tolerance) &
                (payments_df_temp[refund_col] <= reimb_amount + amount_tolerance) &
                (payments_df_temp['Trip UUID'].notna())
            ]
            
            if not matching_payments.empty:
                trip_uuid = matching_payments.iloc[0]['Trip UUID']
    
    # Strategy 2: Search trips by Trip UUID if found
    if trip_uuid and 'Trip UUID' in trips_df.columns:
        trip_match = trips_df[trips_df['Trip UUID'] == trip_uuid]
        if not trip_match.empty:
            return trip_match.iloc[0].to_dict()
    
    # Strategy 3: Fallback to date-based matching within window
    date_col_trips = None
    if 'Trip request time' in trips_df.columns:
        date_col_trips = 'Trip request time'
    elif 'Trip drop off time' in trips_df.columns:
        date_col_trips = 'Trip drop off time'
    elif 'Date' in trips_df.columns:
        date_col_trips = 'Date'
    
    if date_col_trips:
        trips_df_temp = trips_df.copy()
        
        # Safely convert to datetime
        trips_df_temp['Trip_Date'] = pd.to_datetime(trips_df_temp[date_col_trips], errors='coerce')
        
        # Only keep rows with valid dates
        trips_df_temp = trips_df_temp[trips_df_temp['Trip_Date'].notna()]
        
        if not trips_df_temp.empty:
            nearby_trips = trips_df_temp[
                (trips_df_temp['Trip_Date'] >= reimb_date - timedelta(days=date_window)) &
                (trips_df_temp['Trip_Date'] <= reimb_date + timedelta(days=date_window))
            ]
            
            if not nearby_trips.empty:
                return nearby_trips.iloc[0].to_dict()
    
    return None


def find_matching_receipt(reimbursement_row, receipts_df, date_window=3, amount_tolerance=0.50):
    """Find matching receipt in tracker"""
    if receipts_df.empty:
        return None
    
    reimb_date = reimbursement_row.get('Date')
    reimb_amount = reimbursement_row.get('Amount', 0)
    
    if pd.isna(reimb_date):
        return None
    
    # Try different date columns
    date_col = None
    for col in ['Date', 'Trip Date', 'Refund Date']:
        if col in receipts_df.columns:
            date_col = col
            break
    
    if not date_col:
        return None
    
    # Find receipts within date window
    nearby_receipts = receipts_df[
        (receipts_df[date_col] >= reimb_date - timedelta(days=date_window)) &
        (receipts_df[date_col] <= reimb_date + timedelta(days=date_window))
    ]
    
    if nearby_receipts.empty:
        return None
    
    # Try to match by amount
    if 'Refund_Amount' in nearby_receipts.columns:
        amount_matches = nearby_receipts[
            (nearby_receipts['Refund_Amount'] >= reimb_amount - amount_tolerance) &
            (nearby_receipts['Refund_Amount'] <= reimb_amount + amount_tolerance)
        ]
        if not amount_matches.empty:
            return amount_matches.iloc[0].to_dict()
    
    # Return closest date match
    return nearby_receipts.iloc[0].to_dict()


def find_matching_bank_payment(reimbursement_row, bank_df, all_reimbursements=None, date_window=7, amount_tolerance=0.50):
    """Find matching bank payment with support for batched payments and delayed processing
    
    Strategies:
    1. Exact amount match within date window
    2. Look ahead (up to 30 days later) for delayed payments
    3. Batch matching - check if this amount is part of a larger deposit
    """
    if bank_df.empty:
        return None
    
    reimb_date = reimbursement_row.get('Date')
    reimb_amount = reimbursement_row.get('Amount', 0)
    
    if pd.isna(reimb_date):
        return None
    
    # Use Posted Date for bank
    if 'Posted Date' not in bank_df.columns:
        return None
    
    # Strategy 1: Standard exact amount matching within date window
    nearby_payments = bank_df[
        (bank_df['Posted Date'] >= reimb_date - timedelta(days=date_window)) &
        (bank_df['Posted Date'] <= reimb_date + timedelta(days=date_window)) &
        (bank_df['Amount'] > 0)
    ]
    
    if not nearby_payments.empty:
        amount_matches = nearby_payments[
            (nearby_payments['Amount'] >= reimb_amount - 0.50) &
            (nearby_payments['Amount'] <= reimb_amount + 0.50)
        ]
        
        if not amount_matches.empty:
            return amount_matches.iloc[0].to_dict()
    
    # Strategy 2: Look ahead for delayed payments (common for month-end processing)
    # Check if payment arrived later (up to 30 days)
    delayed_payments = bank_df[
        (bank_df['Posted Date'] > reimb_date + timedelta(days=date_window)) &
        (bank_df['Posted Date'] <= reimb_date + timedelta(days=30)) &
        (bank_df['Amount'] > 0)
    ]
    
    if not delayed_payments.empty:
        # Look for exact amount match in delayed payments
        delayed_matches = delayed_payments[
            (delayed_payments['Amount'] >= reimb_amount - 0.50) &
            (delayed_payments['Amount'] <= reimb_amount + 0.50)
        ]
        
        if not delayed_matches.empty:
            # Mark as delayed payment but still return match
            match = delayed_matches.iloc[0].to_dict()
            match['_is_delayed'] = True
            return match
    
    # Strategy 3: Batch payment matching
    # Check if this amount is part of a larger batch deposit
    if all_reimbursements is not None and not all_reimbursements.empty:
        # Look for larger deposits that could contain this amount
        batch_window_start = reimb_date - timedelta(days=2)
        batch_window_end = reimb_date + timedelta(days=35)  # Extended for batch processing
        
        potential_batches = bank_df[
            (bank_df['Posted Date'] >= batch_window_start) &
            (bank_df['Posted Date'] <= batch_window_end) &
            (bank_df['Amount'] > reimb_amount + 1.0)  # Larger than individual amount
        ]
        
        if not potential_batches.empty:
            # For each potential batch, calculate what reimbursements it could contain
            for _, batch_deposit in potential_batches.iterrows():
                batch_amount = batch_deposit['Amount']
                batch_date = batch_deposit['Posted Date']
                
                # Find all reimbursements from similar date that could fit in batch
                same_period_reimbs = all_reimbursements[
                    (all_reimbursements['Date'].dt.date <= batch_date.date()) &
                    (all_reimbursements['Date'].dt.date >= (batch_date - timedelta(days=14)).date())
                ].copy()
                
                if not same_period_reimbs.empty:
                    # Calculate sum and check if it's close to batch amount
                    sum_amount = same_period_reimbs['Amount'].sum()
                    
                    if abs(sum_amount - batch_amount) < 2.0:  # Within $2 tolerance for batch
                        # This could be our batch! Return the batch with marker
                        match = batch_deposit.to_dict()
                        match['_is_batch'] = True
                        match['_batch_count'] = len(same_period_reimbs)
                        return match
    
    return None


def reconcile_reimbursements():
    """Main reconciliation function"""
    
    print("=" * 80)
    print("REIMBURSEMENT RECONCILIATION REPORT")
    print("=" * 80)
    print()
    
    # Load all data sources
    print("Loading data sources...")
    payments_df = load_payments_data()
    trips_df = load_trips_data()
    receipts_df = load_receipt_tracker()
    bank_df = load_bank_statements()
    
    print(f"  Payments records: {len(payments_df)}")
    print(f"  Trips records: {len(trips_df)}")
    print(f"  Receipt tracker: {len(receipts_df)}")
    print(f"  Bank transactions: {len(bank_df)}")
    print()
    
    # Filter for reimbursements in payments
    if payments_df.empty:
        print("⚠ No payments data found")
        return
    
    # Find refund column
    refund_col = 'Paid to you:Trip balance:Refunds:Order Value'
    
    if refund_col not in payments_df.columns:
        print(f"⚠ Refund column not found: {refund_col}")
        print("Available columns:", payments_df.columns.tolist())
        return
    
    # Filter for transactions with positive refund values
    reimbursements = payments_df[payments_df[refund_col] > 0].copy()
    
    if reimbursements.empty:
        print("⚠ No reimbursement transactions found (refunds > 0)")
        return
    
    # Parse date from vs reporting column (format: "2025-09-01 22:49:20.154 -0500 CDT")
    if 'vs reporting' in reimbursements.columns:
        # Extract just the date/time part before the timezone
        reimbursements['Date'] = reimbursements['vs reporting'].str.split(' -').str[0]
        reimbursements['Date'] = pd.to_datetime(reimbursements['Date'], errors='coerce')
    else:
        print("⚠ No date column found in payments data")
        return
    
    # Standardize column names for processing
    reimbursements['Amount'] = reimbursements[refund_col]
    
    # Remove rows with invalid dates
    initial_count = len(reimbursements)
    reimbursements = reimbursements[reimbursements['Date'].notna()]
    if len(reimbursements) < initial_count:
        print(f"⚠ Removed {initial_count - len(reimbursements)} rows with invalid dates")
    
    print(f"Found {len(reimbursements)} reimbursement transactions from Uber payments")
    print()
    
    # Create reconciliation records
    reconciliation_records = []
    
    for idx, reimb in reimbursements.iterrows():
        record = {
            'Date': reimb.get('Date'),
            'Month': reimb.get('Date').strftime('%Y-%m') if pd.notna(reimb.get('Date')) else 'Unknown',
            'Uber_Amount': reimb.get('Amount', 0),
            'Description': reimb.get('Description', ''),
            'Trip_Match': 'No',
            'Receipt_Match': 'No',
            'Bank_Match': 'No',
            'Trip_Details': '',
            'Receipt_Amount': None,
            'Bank_Amount': None,
            'Bank_Date': None,
            'Status': 'Pending'
        }
        
        # Find matching trip
        trip_match = find_matching_trip(reimb, trips_df, payments_df)
        if trip_match:
            record['Trip_Match'] = 'Yes'
            # Try different column combinations for pickup/dropoff
            pickup = trip_match.get('Pickup address', trip_match.get('Pickup', ''))
            dropoff = trip_match.get('Drop off address', trip_match.get('Dropoff', ''))
            if pickup and dropoff:
                record['Trip_Details'] = f"{pickup[:30]} → {dropoff[:30]}"
            else:
                record['Trip_Details'] = trip_match.get('Trip UUID', 'Trip found')
        
        # Find matching receipt
        receipt_match = find_matching_receipt(reimb, receipts_df)
        if receipt_match:
            record['Receipt_Match'] = 'Yes'
            record['Receipt_Amount'] = receipt_match.get('Refund_Amount')
        
        # Find matching bank payment (pass all reimbursements for batch detection)
        bank_match = find_matching_bank_payment(reimb, bank_df, reimbursements)
        if bank_match:
            record['Bank_Match'] = 'Yes'
            record['Bank_Amount'] = bank_match.get('Amount')
            record['Bank_Date'] = bank_match.get('Posted Date')
            
            # Note if this is a batch or delayed payment
            if bank_match.get('_is_batch'):
                record['Status'] = f"Received (Batched with {bank_match.get('_batch_count')} items)"
            elif bank_match.get('_is_delayed'):
                record['Status'] = 'Received (Delayed payment)'
            else:
                record['Status'] = 'Received'
        else:
            # Determine status without bank match
            if record['Receipt_Match'] == 'Yes':
                record['Status'] = 'Tracked - Not Received'
            else:
                record['Status'] = 'Not Tracked'
        
        reconciliation_records.append(record)
    
    # Create DataFrame
    reconciliation_df = pd.DataFrame(reconciliation_records)
    
    # Sort by date
    reconciliation_df = reconciliation_df.sort_values('Date')
    
    # Export detailed report
    output_file = 'reimbursement_reconciliation.csv'
    reconciliation_df.to_csv(output_file, index=False)
    print(f"✓ Exported detailed reconciliation: {output_file}")
    print()
    
    # Display summary by month
    print("=" * 80)
    print("MONTHLY SUMMARY")
    print("=" * 80)
    
    for month in sorted(reconciliation_df['Month'].unique()):
        month_data = reconciliation_df[reconciliation_df['Month'] == month]
        
        uber_total = month_data['Uber_Amount'].sum()
        bank_total = month_data[month_data['Bank_Match'] == 'Yes']['Bank_Amount'].sum()
        
        print(f"\n{month}:")
        print(f"  Uber Claims: ${uber_total:,.2f} ({len(month_data)} transactions)")
        print(f"  Bank Received: ${bank_total:,.2f} ({len(month_data[month_data['Bank_Match'] == 'Yes'])} payments)")
        print(f"  Difference: ${uber_total - bank_total:,.2f}")
        print(f"  ")
        print(f"  Trip Match: {len(month_data[month_data['Trip_Match'] == 'Yes'])}/{len(month_data)}")
        print(f"  Receipt Match: {len(month_data[month_data['Receipt_Match'] == 'Yes'])}/{len(month_data)}")
        print(f"  Bank Match: {len(month_data[month_data['Bank_Match'] == 'Yes'])}/{len(month_data)}")
    
    # Overall summary
    print("\n" + "=" * 80)
    print("OVERALL SUMMARY")
    print("=" * 80)
    
    total_uber = reconciliation_df['Uber_Amount'].sum()
    total_bank = reconciliation_df[reconciliation_df['Bank_Match'] == 'Yes']['Bank_Amount'].sum()
    
    print(f"\nTotal Uber Claims: ${total_uber:,.2f}")
    print(f"Total Bank Received: ${total_bank:,.2f}")
    print(f"Total Difference: ${total_uber - total_bank:,.2f}")
    print()
    print(f"Trip Matches: {len(reconciliation_df[reconciliation_df['Trip_Match'] == 'Yes'])}/{len(reconciliation_df)}")
    print(f"Receipt Matches: {len(reconciliation_df[reconciliation_df['Receipt_Match'] == 'Yes'])}/{len(reconciliation_df)}")
    print(f"Bank Matches: {len(reconciliation_df[reconciliation_df['Bank_Match'] == 'Yes'])}/{len(reconciliation_df)}")
    
    # Status breakdown
    print("\nStatus Breakdown:")
    for status in reconciliation_df['Status'].unique():
        count = len(reconciliation_df[reconciliation_df['Status'] == status])
        print(f"  {status}: {count}")
    
    return reconciliation_df


if __name__ == '__main__':
    df = reconcile_reimbursements()
