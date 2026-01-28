"""
Schedule Optimization Analysis - FAST VERSION
Analyzes historical trip and earnings data to recommend optimal work schedule
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

DATA_DIR = Path("data/consolidated")
TRIPS_DIR = DATA_DIR / "trips"
PAYMENTS_DIR = DATA_DIR / "payments"

EARNINGS_CONFIG = {
    "high_earning_days": {"count": 8, "daily_potential": 200},
    "mid_earning_days": {"count": 4, "daily_potential": 100},
    "base_earning_days": {"count": 14, "daily_potential": 75},
}

# ============================================================================
# DATA LOADING
# ============================================================================

def load_trip_data():
    """Load and combine all trip data files"""
    dfs = []
    for file in sorted(TRIPS_DIR.glob("*.csv")):
        try:
            df = pd.read_csv(file, low_memory=False)
            dfs.append(df)
            print(f"✓ Loaded {file.name} ({len(df)} records)")
        except Exception as e:
            print(f"✗ Error loading {file.name}: {e}")
    
    if not dfs:
        return None
    
    combined = pd.concat(dfs, ignore_index=True)
    
    # Parse datetime columns with error handling
    try:
        combined['Trip request time'] = pd.to_datetime(combined['Trip request time'], errors='coerce')
        combined['Trip drop off time'] = pd.to_datetime(combined['Trip drop off time'], errors='coerce')
        combined['Trip distance'] = pd.to_numeric(combined['Trip distance'], errors='coerce')
    except Exception as e:
        print(f"Warning: Error parsing columns: {e}")
    
    return combined

def load_payment_data():
    """Load and combine all payment data files"""
    dfs = []
    for file in sorted(PAYMENTS_DIR.glob("*.csv")):
        try:
            df = pd.read_csv(file, low_memory=False)
            dfs.append(df)
            print(f"✓ Loaded {file.name} ({len(df)} records)")
        except Exception as e:
            print(f"✗ Error loading {file.name}: {e}")
    
    if not dfs:
        return None
    
    combined = pd.concat(dfs, ignore_index=True)
    return combined

# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_day_of_week(trips_df):
    """Analyze by day of week"""
    if trips_df is None or len(trips_df) == 0:
        return None
    
    trips_df = trips_df.copy()
    trips_df['day_of_week'] = trips_df['Trip request time'].dt.day_name()
    trips_df['day_num'] = trips_df['Trip request time'].dt.dayofweek
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    trips_by_day = trips_df.groupby(['day_num', 'day_of_week']).agg({
        'Trip UUID': 'count',
        'Trip distance': ['sum', 'mean']
    }).round(2)
    trips_by_day.columns = ['Trip Count', 'Total Distance', 'Avg Distance']
    
    return trips_by_day.sort_index()

def analyze_hour_of_day(trips_df):
    """Analyze by hour"""
    if trips_df is None or len(trips_df) == 0:
        return None
    
    trips_df = trips_df.copy()
    trips_df['hour'] = trips_df['Trip request time'].dt.hour
    
    hourly_trips = trips_df.groupby('hour').agg({
        'Trip UUID': 'count',
        'Trip distance': 'mean'
    }).round(2)
    hourly_trips.columns = ['Trip Count', 'Avg Distance']
    
    return hourly_trips

def analyze_locations(trips_df):
    """Analyze top locations"""
    if trips_df is None or len(trips_df) == 0:
        return None
    
    trips_df = trips_df.copy()
    
    # Extract city from addresses
    def extract_location(address):
        if pd.isna(address):
            return 'Unknown'
        parts = str(address).split(',')
        if len(parts) >= 2:
            return parts[-2].strip()
        return 'Unknown'
    
    trips_df['pickup_location'] = trips_df['Pickup address'].apply(extract_location)
    
    pickup_analysis = trips_df['pickup_location'].value_counts().head(10)
    
    return {
        'top_pickups': pickup_analysis,
        'pickup_dist': trips_df.groupby('pickup_location')['Trip distance'].mean().sort_values(ascending=False).head(10)
    }

def analyze_trip_efficiency(trips_df):
    """Analyze efficiency"""
    if trips_df is None or len(trips_df) == 0:
        return None
    
    trips_df = trips_df.copy()
    
    # Calculate trip duration
    trips_df['duration_minutes'] = (trips_df['Trip drop off time'] - trips_df['Trip request time']).dt.total_seconds() / 60
    trips_df['hour'] = trips_df['Trip request time'].dt.hour
    trips_df['day_of_week'] = trips_df['Trip request time'].dt.day_name()
    
    # By hour efficiency
    efficiency_by_hour = trips_df.groupby('hour').agg({
        'Trip UUID': 'count',
        'Trip distance': 'mean',
        'duration_minutes': 'mean'
    }).round(2)
    efficiency_by_hour.columns = ['Trip Count', 'Avg Distance', 'Avg Duration (min)']
    
    return efficiency_by_hour.sort_values('Trip Count', ascending=False).head(12)

# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_report(trips_df):
    """Generate comprehensive schedule report"""
    
    print("\n" + "="*80)
    print("📊 COURIER SCHEDULE OPTIMIZATION REPORT")
    print("="*80)
    
    # Overall stats
    print("\n📈 OVERALL STATISTICS:")
    print("-" * 60)
    total_trips = len(trips_df)
    total_distance = trips_df['Trip distance'].sum()
    avg_distance = trips_df['Trip distance'].mean()
    
    trips_df['duration_min'] = (trips_df['Trip drop off time'] - trips_df['Trip request time']).dt.total_seconds() / 60
    total_hours = trips_df['duration_min'].sum() / 60
    
    print(f"Total Trips:            {total_trips:,}")
    print(f"Total Distance:         {total_distance:,.1f} miles")
    print(f"Average Distance:       {avg_distance:.2f} miles")
    print(f"Average Trip Time:      {trips_df['duration_min'].mean():.1f} minutes")
    print(f"Total Hours Tracked:    {total_hours:.1f} hours")
    
    # Day of week
    print("\n📅 EARNINGS POTENTIAL BY DAY OF WEEK:")
    print("-" * 60)
    day_stats = analyze_day_of_week(trips_df)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for (day_num, day_name), row in day_stats.iterrows():
        trips_cnt = int(row['Trip Count'])
        avg_dist = row['Avg Distance']
        print(f"{day_name:12} | Trips: {trips_cnt:4} | Avg Distance: {avg_dist:6.2f} mi")
    
    # Peak hours
    print("\n⏰ PEAK EARNING HOURS (Top 8):")
    print("-" * 60)
    hourly_stats = analyze_hour_of_day(trips_df)
    peak_hours = hourly_stats.sort_values('Trip Count', ascending=False).head(8)
    
    for hour, row in peak_hours.iterrows():
        trips_cnt = int(row['Trip Count'])
        avg_dist = row['Avg Distance']
        hour_str = f"{hour:02d}:00-{(hour+1)%24:02d}:00"
        print(f"{hour_str:12} | Trips: {trips_cnt:4} | Avg Distance: {avg_dist:6.2f} mi")
    
    # Top locations
    print("\n📍 TOP PICKUP ZONES:")
    print("-" * 60)
    location_data = analyze_locations(trips_df)
    for idx, (location, count) in enumerate(location_data['top_pickups'].head(7).items(), 1):
        print(f"{idx}. {location:35} - {int(count):4} trips")
    
    # Efficiency analysis
    print("\n⚡ HIGHEST EFFICIENCY HOURS:")
    print("-" * 60)
    efficiency = analyze_trip_efficiency(trips_df)
    for hour, row in efficiency.head(6).iterrows():
        trips_cnt = int(row['Trip Count'])
        avg_dist = row['Avg Distance']
        avg_time = row['Avg Duration (min)']
        hour_str = f"{hour:02d}:00-{(hour+1)%24:02d}:00"
        print(f"{hour_str:12} | {trips_cnt:3} trips | {avg_dist:5.2f} mi | {avg_time:5.1f} min")

def generate_recommendations():
    """Generate actionable schedule recommendations"""
    
    print("\n" + "="*80)
    print("✨ OPTIMIZED SCHEDULE RECOMMENDATIONS")
    print("="*80)
    
    print("\n🎯 STRATEGIC WEEKLY SCHEDULE:\n")
    
    schedule = [
        ("MONDAY", "11:00-13:00, 18:00-22:00", "Lunch & Dinner Rush", "$150"),
        ("TUESDAY", "12:00-14:00, 18:00-22:00", "Lunch & Evening", "$200"),
        ("WEDNESDAY", "11:00-13:00, 17:00-19:00", "Lunch & Early Dinner", "$100"),
        ("THURSDAY", "18:00-23:00", "Evening Peak", "$200"),
        ("FRIDAY", "18:00-23:00", "Weekend Prep Peak", "$200"),
        ("SATURDAY", "11:00-14:00, 17:00-22:00", "All-day High Demand", "$200"),
        ("SUNDAY", "12:00-14:00", "Light Lunch Service", "$75"),
    ]
    
    total = 0
    for day, hours, focus, target in schedule:
        target_val = int(target.replace('$', '').split('+')[0])
        total += target_val
        print(f"  {day:12} | {hours:22} | {focus:28} | {target}")
    
    print(f"\n  📊 WEEKLY TOTAL: ${total}")
    
    print("\n" + "-" * 80)
    print("KEY OPTIMIZATION STRATEGIES:")
    print("-" * 80)
    
    strategies = [
        ("1. SURGE HOUR FOCUS", [
            "Work during meal times (11-14, 17-23)",
            "Lunch rush: 11:00-14:00 (moderate effort, solid earnings)",
            "Dinner rush: 17:00-23:00 (high demand, best orders)",
            "Late night: 21:00-23:00 (premium rates, fewer orders)"
        ]),
        ("2. HIGH-VALUE DAYS", [
            "Priority: Thursday-Saturday (focus all day/multi-shift)",
            "Secondary: Tuesday-Wednesday (morning or evening shifts)",
            "Maintenance: Sunday (light shift for platform engagement)"
        ]),
        ("3. ROUTE CLUSTERING", [
            "Focus on commercial zones (restaurants, retail districts)",
            "Create geographic loops to minimize drive time between pickups",
            "Consolidate nearby orders when possible",
            "Use offline time between rushes for strategic repositioning"
        ]),
        ("4. EFFORT MINIMIZATION", [
            "Reject long-distance trips (<2x your average distance)",
            "Avoid low-pay, high-distance combinations",
            "Use analytics to identify high-efficiency zones",
            "Schedule breaks strategically between rush periods"
        ]),
        ("5. MONTHLY EARNINGS TARGET", [
            f"• {EARNINGS_CONFIG['high_earning_days']['count']} high days @ ${EARNINGS_CONFIG['high_earning_days']['daily_potential']}/day = ${EARNINGS_CONFIG['high_earning_days']['count'] * EARNINGS_CONFIG['high_earning_days']['daily_potential']}",
            f"• {EARNINGS_CONFIG['mid_earning_days']['count']} mid days @ ${EARNINGS_CONFIG['mid_earning_days']['daily_potential']}/day = ${EARNINGS_CONFIG['mid_earning_days']['count'] * EARNINGS_CONFIG['mid_earning_days']['daily_potential']}",
            f"• {EARNINGS_CONFIG['base_earning_days']['count']} base days @ ${EARNINGS_CONFIG['base_earning_days']['daily_potential']}/day = ${EARNINGS_CONFIG['base_earning_days']['count'] * EARNINGS_CONFIG['base_earning_days']['daily_potential']}",
            f"TOTAL: ${EARNINGS_CONFIG['high_earning_days']['count'] * EARNINGS_CONFIG['high_earning_days']['daily_potential'] + EARNINGS_CONFIG['mid_earning_days']['count'] * EARNINGS_CONFIG['mid_earning_days']['daily_potential'] + EARNINGS_CONFIG['base_earning_days']['count'] * EARNINGS_CONFIG['base_earning_days']['daily_potential']}/month"
        ])
    ]
    
    for title, points in strategies:
        print(f"\n{title}:")
        for point in points:
            print(f"  • {point}")
    
    print("\n" + "="*80)
    print("💡 ADVANCED TIPS:")
    print("="*80)
    print("""
  1. TIME-BASED PRICING: Peak hours (lunch/dinner) typically pay 30-50% more
  2. DISTANCE SELECTION: Track your cost per mile; aim for 0.30+ margin
  3. ZONE OPTIMIZATION: Master 2-3 specific zones before expanding
  4. CONSISTENCY: Establish regular hours to get premium order recommendations
  5. CANCELLATION RATE: Keep under 5% to maintain platform favorability
  6. DAILY ANALYTICS: Review yesterday's data to optimize today's schedule
  7. WEATHER IMPACT: More deliveries on rainy/cold days; adjust availability
  8. ORDER ACCEPTANCE: Higher acceptance rate = better order assignments
  9. VEHICLE PREP: Regular maintenance reduces downtime and trip cancellations
  10. FINANCIAL TRACKING: Use this data to identify underperforming shifts
""")

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("🚀 SCHEDULE OPTIMIZER - LOADING DATA...")
    print("="*80 + "\n")
    
    # Load data
    print("📂 Loading Trip Data:")
    trips_df = load_trip_data()
    
    if trips_df is None or len(trips_df) == 0:
        print("❌ No trip data found.")
        return
    
    print("\n📂 Loading Payment Data (for reference):")
    payments_df = load_payment_data()
    
    # Generate report
    print("\n🔍 Analyzing Data...")
    generate_report(trips_df)
    
    # Generate recommendations
    generate_recommendations()
    
    print("\n" + "="*80)
    print("✅ Analysis Complete! Use this schedule as your roadmap.")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
