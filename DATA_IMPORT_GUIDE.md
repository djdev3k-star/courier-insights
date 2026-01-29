# HustleReport Data Import Guide

## Quick Start

Your HustleReport application is now fully integrated with Supabase and ready to use real data!

## Database Setup ✓

The following tables have been created:
- **trips** - Stores all courier trip data
- **expenses** - Stores all expense transactions
- **analytics_summary** - Stores pre-calculated analytics

## Current Status

The database is empty and ready for data import. You have two options:

### Option 1: Import from CSV Files (Recommended)

If you have trip and expense data in CSV format:

1. Install Python dependencies:
   ```bash
   pip install python-dotenv supabase
   ```

2. Place your CSV files in the project:
   - `data/trips.csv` - Trip data with columns: pickup_time, dropoff_time, fare_amount, distance, pickup_location, dropoff_location
   - `data/expenses.csv` - Expense data with columns: date, description, amount, category, merchant

3. Run the import script:
   ```bash
   python scripts/import_data_to_supabase.py
   ```

### Option 2: Using the Application Directly

The app works with static fallback data if no database records exist, so you can:

1. Start the dev server:
   ```bash
   npm run dev
   ```

2. Visit http://localhost:3000

3. The app will show static data from your analysis reports

## Features Now Available

### 1. Real-Time Dashboard
- Loads actual trip and expense data from Supabase
- Displays real calculations based on your data
- Automatic fallback to static data if database is empty

### 2. Live Expense Tracking
- Fetches expenses from database
- Shows actual spending breakdown
- Calculates merchant totals dynamically

### 3. Analytics Edge Function
The analytics edge function provides:
- **GET /analytics** - API status and available endpoints
- **POST /analytics/refresh** - Recalculate analytics summary from all data

To refresh analytics:
```bash
curl -X POST https://YOUR_PROJECT.supabase.co/functions/v1/analytics/refresh \
  -H "Authorization: Bearer YOUR_ANON_KEY"
```

### 4. Data Import Utility
Location: `scripts/import_data_to_supabase.py`

Features:
- Imports trips from CSV
- Imports expenses from CSV
- Automatically calculates analytics summary
- Updates existing records if re-run
- Handles multiple CSV formats

## Environment Variables

Your `.env` file should contain:
```
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_anon_key
```

These are automatically available to:
- React app (via Vite)
- Python import scripts (via python-dotenv)
- Edge functions (auto-configured by Supabase)

## Next Steps

1. **Import Your Data** - Run the import script if you have CSV files
2. **Start the App** - `npm run dev` to see your live dashboard
3. **Explore Reports** - All pages now load real data from Supabase
4. **Refresh Analytics** - Call the edge function to update calculations

## Troubleshooting

### App shows loading spinner forever
- Check that `.env` has correct Supabase credentials
- Verify database has at least one record in analytics_summary table

### Import script fails
- Ensure CSV files exist in expected locations
- Check CSV column names match expected format
- Verify `.env` file has VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY

### No data showing in app
- Database is empty - either import CSV data or app will show fallback data
- Check browser console for errors
- Verify Supabase project is active and RLS policies are set

## Architecture

```
┌─────────────────┐
│   React App     │
│  (Vite + React  │
│   + Tailwind)   │
└────────┬────────┘
         │
         │ @supabase/supabase-js
         │
┌────────▼────────┐
│   Supabase DB   │
│  - trips table  │
│  - expenses     │
│  - analytics    │
└────────┬────────┘
         │
┌────────▼────────┐
│  Edge Functions │
│   /analytics    │
│  (data refresh) │
└─────────────────┘
```

## Data Model

### Trips Table
- pickup_time (timestamptz)
- dropoff_time (timestamptz)
- fare_amount (numeric)
- distance (numeric)
- pickup_location (text)
- dropoff_location (text)
- status (text)

### Expenses Table
- date (timestamptz)
- description (text)
- amount (numeric)
- category (text)
- category_type (reimbursable | personal | unknown)
- merchant (text)

### Analytics Summary Table
- total_trips (integer)
- total_earnings (numeric)
- total_expenses (numeric)
- monthly_target (numeric)
- current_monthly (numeric)
- peak_hours (integer[])
- optimal_days (text[])
- last_updated (timestamptz)

## Support

For issues or questions:
1. Check browser console for errors
2. Verify Supabase dashboard shows tables
3. Test edge function directly via Supabase dashboard
4. Check that RLS policies allow read access
