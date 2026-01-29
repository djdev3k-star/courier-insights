#!/usr/bin/env python3
"""
Import trip and expense data from CSV files into Supabase database.

This script reads CSV files from the data directories and imports them into
the Supabase database for the HustleReport React application.
"""

import os
import csv
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("VITE_SUPABASE_URL")
key = os.environ.get("VITE_SUPABASE_ANON_KEY")

if not url or not key:
    print("Error: VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY must be set in .env")
    exit(1)

supabase: Client = create_client(url, key)

def import_trips_from_csv(csv_path: str):
    """Import trip data from CSV file."""
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found, skipping trips import")
        return 0

    trips = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trip = {
                'pickup_time': row.get('pickup_time') or row.get('Pickup Time'),
                'dropoff_time': row.get('dropoff_time') or row.get('Dropoff Time'),
                'fare_amount': float(row.get('fare_amount') or row.get('Fare') or 0),
                'distance': float(row.get('distance') or row.get('Distance') or 0),
                'pickup_location': row.get('pickup_location') or row.get('Pickup Location', ''),
                'dropoff_location': row.get('dropoff_location') or row.get('Dropoff Location', ''),
                'status': row.get('status') or 'completed'
            }
            trips.append(trip)

    if trips:
        print(f"Importing {len(trips)} trips...")
        result = supabase.table('trips').insert(trips).execute()
        print(f"Successfully imported {len(trips)} trips")
        return len(trips)

    return 0

def import_expenses_from_csv(csv_path: str):
    """Import expense data from CSV file."""
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found, skipping expenses import")
        return 0

    expenses = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            expense = {
                'date': row.get('date') or row.get('Date') or row.get('Transaction Date'),
                'description': row.get('description') or row.get('Description', ''),
                'amount': abs(float(row.get('amount') or row.get('Amount') or 0)),
                'category': row.get('category') or row.get('Category', ''),
                'category_type': row.get('category_type') or row.get('Type', 'unknown'),
                'merchant': row.get('merchant') or row.get('Merchant', '')
            }
            expenses.append(expense)

    if expenses:
        print(f"Importing {len(expenses)} expenses...")
        result = supabase.table('expenses').insert(expenses).execute()
        print(f"Successfully imported {len(expenses)} expenses")
        return len(expenses)

    return 0

def update_analytics_summary():
    """Calculate and update analytics summary from imported data."""
    print("Calculating analytics summary...")

    trips_result = supabase.table('trips').select('*').execute()
    expenses_result = supabase.table('expenses').select('*').execute()

    trips = trips_result.data or []
    expenses = expenses_result.data or []

    total_trips = len(trips)
    total_earnings = sum(float(t.get('fare_amount', 0)) for t in trips)
    total_expenses = sum(float(e.get('amount', 0)) for e in expenses)

    months_in_analysis = 5
    current_monthly = total_earnings / months_in_analysis if months_in_analysis > 0 else 0

    analytics = {
        'total_trips': total_trips,
        'total_earnings': total_earnings,
        'total_expenses': total_expenses,
        'monthly_target': 3050,
        'current_monthly': current_monthly,
        'peak_hours': [18, 19, 20, 21, 22, 23],
        'optimal_days': ['Tuesday', 'Thursday', 'Friday', 'Saturday'],
        'last_updated': datetime.now().isoformat()
    }

    existing = supabase.table('analytics_summary').select('id').limit(1).execute()

    if existing.data:
        analytics_id = existing.data[0]['id']
        result = supabase.table('analytics_summary').update(analytics).eq('id', analytics_id).execute()
        print(f"Updated analytics summary: {total_trips} trips, ${total_earnings:.2f} earnings, ${total_expenses:.2f} expenses")
    else:
        result = supabase.table('analytics_summary').insert(analytics).execute()
        print(f"Created analytics summary: {total_trips} trips, ${total_earnings:.2f} earnings, ${total_expenses:.2f} expenses")

def main():
    """Main import function."""
    print("HustleReport Data Import Utility")
    print("=" * 50)

    trips_count = 0
    expenses_count = 0

    trips_paths = [
        'data/consolidated/trips/all_trips.csv',
        'data/consolidated/trips.csv',
        'data/trips.csv'
    ]

    for path in trips_paths:
        if os.path.exists(path):
            print(f"\nFound trips file: {path}")
            trips_count = import_trips_from_csv(path)
            break

    expense_paths = [
        'data/consolidated/expenses/all_expenses.csv',
        'data/consolidated/expenses.csv',
        'data/expenses.csv',
        'bank/consolidated_transactions.csv'
    ]

    for path in expense_paths:
        if os.path.exists(path):
            print(f"\nFound expenses file: {path}")
            expenses_count = import_expenses_from_csv(path)
            break

    if trips_count > 0 or expenses_count > 0:
        print("\n" + "=" * 50)
        update_analytics_summary()
        print("\n" + "=" * 50)
        print("Import complete!")
        print(f"Total imported: {trips_count} trips, {expenses_count} expenses")
    else:
        print("\nNo data files found. Please place CSV files in:")
        print("  - data/trips.csv")
        print("  - data/expenses.csv")

if __name__ == '__main__':
    main()
