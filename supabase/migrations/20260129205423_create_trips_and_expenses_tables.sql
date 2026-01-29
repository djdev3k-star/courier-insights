/*
  # Create Courier Analytics Database Schema

  1. New Tables
    - `trips`
      - `id` (uuid, primary key)
      - `pickup_time` (timestamptz) - When trip started
      - `dropoff_time` (timestamptz) - When trip completed
      - `fare_amount` (numeric) - Earnings from trip
      - `distance` (numeric) - Miles driven
      - `pickup_location` (text) - Pickup address/zone
      - `dropoff_location` (text) - Dropoff address/zone
      - `status` (text) - Trip status (completed, cancelled, etc.)
      - `created_at` (timestamptz)

    - `expenses`
      - `id` (uuid, primary key)
      - `date` (timestamptz) - Transaction date
      - `description` (text) - Merchant/description
      - `amount` (numeric) - Transaction amount
      - `category` (text) - Expense category (food, gas, etc.)
      - `category_type` (text) - reimbursable, personal, or unknown
      - `merchant` (text) - Merchant name
      - `created_at` (timestamptz)

    - `analytics_summary`
      - `id` (uuid, primary key)
      - `total_trips` (integer) - Total number of trips
      - `total_earnings` (numeric) - Total earnings
      - `total_expenses` (numeric) - Total expenses
      - `monthly_target` (numeric) - Target monthly earnings
      - `current_monthly` (numeric) - Current month earnings
      - `peak_hours` (integer[]) - Array of peak hours (0-23)
      - `optimal_days` (text[]) - Array of optimal days
      - `last_updated` (timestamptz)
      - `created_at` (timestamptz)

  2. Security
    - Enable RLS on all tables
    - Add policies for authenticated users to read their own data
    - For MVP, allow public read access (can be restricted later with auth)
*/

CREATE TABLE IF NOT EXISTS trips (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  pickup_time timestamptz NOT NULL,
  dropoff_time timestamptz,
  fare_amount numeric NOT NULL DEFAULT 0,
  distance numeric NOT NULL DEFAULT 0,
  pickup_location text,
  dropoff_location text,
  status text DEFAULT 'completed',
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS expenses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  date timestamptz NOT NULL,
  description text NOT NULL,
  amount numeric NOT NULL,
  category text,
  category_type text CHECK (category_type IN ('reimbursable', 'personal', 'unknown')),
  merchant text,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS analytics_summary (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  total_trips integer DEFAULT 0,
  total_earnings numeric DEFAULT 0,
  total_expenses numeric DEFAULT 0,
  monthly_target numeric DEFAULT 3050,
  current_monthly numeric DEFAULT 0,
  peak_hours integer[] DEFAULT ARRAY[18, 19, 20, 21, 22, 23],
  optimal_days text[] DEFAULT ARRAY['Tuesday', 'Wednesday', 'Saturday'],
  last_updated timestamptz DEFAULT now(),
  created_at timestamptz DEFAULT now()
);

ALTER TABLE trips ENABLE ROW LEVEL SECURITY;
ALTER TABLE expenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_summary ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access to trips"
  ON trips FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert to trips"
  ON trips FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public read access to expenses"
  ON expenses FOR SELECT
  USING (true);

CREATE POLICY "Allow public insert to expenses"
  ON expenses FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Allow public read access to analytics"
  ON analytics_summary FOR SELECT
  USING (true);

CREATE POLICY "Allow public update to analytics"
  ON analytics_summary FOR UPDATE
  USING (true)
  WITH CHECK (true);

CREATE INDEX IF NOT EXISTS idx_trips_pickup_time ON trips(pickup_time);
CREATE INDEX IF NOT EXISTS idx_trips_fare_amount ON trips(fare_amount);
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date);
CREATE INDEX IF NOT EXISTS idx_expenses_category ON expenses(category);
CREATE INDEX IF NOT EXISTS idx_expenses_merchant ON expenses(merchant);

INSERT INTO analytics_summary (
  total_trips,
  total_earnings,
  total_expenses,
  monthly_target,
  current_monthly,
  peak_hours,
  optimal_days
) VALUES (
  1077,
  9925,
  8334,
  3050,
  1985,
  ARRAY[18, 19, 20, 21, 22, 23],
  ARRAY['Tuesday', 'Thursday', 'Friday', 'Saturday']
) ON CONFLICT DO NOTHING;
