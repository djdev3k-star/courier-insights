"""
Actual vs. Recommended Analysis
Compares what the optimization plan recommended vs. what actually happened
Shows gaps between optimal behavior and actual behavior
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# ============================================================================
# LOAD DATA
# ============================================================================

def load_trips():
    """Load all trip data"""
    trips_dir = Path('c:/Users/dj-dev/Documents/courier/data/consolidated/trips')
    
    dfs = []
    for csv in sorted(trips_dir.glob('*.csv')):
        df = pd.read_csv(csv)
        dfs.append(df)
    
    trips = pd.concat(dfs, ignore_index=True)
    
    # Parse datetime
    trips['Trip_DateTime'] = pd.to_datetime(trips['Trip request time'], errors='coerce')
    trips['Trip_Hour'] = trips['Trip_DateTime'].dt.hour
    trips['Trip_Date'] = trips['Trip_DateTime'].dt.date
    trips['Trip_DayOfWeek'] = trips['Trip_DateTime'].dt.day_name()
    trips['Trip_Month'] = trips['Trip_DateTime'].dt.month
    
    return trips

def load_expenses():
    """Load expense data"""
    reports_dir = Path('c:/Users/dj-dev/Documents/courier/reports')
    csv_file = list(reports_dir.glob('expense_report_*.csv'))[0]
    
    expenses = pd.read_csv(csv_file)
    expenses['Date'] = pd.to_datetime(expenses['Date'])
    expenses['DayOfWeek'] = expenses['Date'].dt.day_name()
    expenses['Month'] = expenses['Date'].dt.month
    
    return expenses

# ============================================================================
# OPTIMAL RECOMMENDATIONS (from SCHEDULE_OPTIMIZATION_PLAN.md)
# ============================================================================

RECOMMENDED_SCHEDULE = {
    'Monday': {
        'hours': '11AM-1PM, 6PM-10PM',
        'total_hours': 6,
        'target_earnings': 150,
        'optimal_hours': [11, 12, 18, 19, 20, 21]
    },
    'Tuesday': {
        'hours': '12PM-2PM, 6PM-10PM',
        'total_hours': 6,
        'target_earnings': 200,
        'optimal_hours': [12, 13, 18, 19, 20, 21]
    },
    'Wednesday': {
        'hours': '11AM-1PM, 5PM-7PM',
        'total_hours': 4,
        'target_earnings': 100,
        'optimal_hours': [11, 12, 17, 18]
    },
    'Thursday': {
        'hours': '6PM-11PM',
        'total_hours': 5,
        'target_earnings': 200,
        'optimal_hours': [18, 19, 20, 21, 22]
    },
    'Friday': {
        'hours': '6PM-11PM',
        'total_hours': 5,
        'target_earnings': 200,
        'optimal_hours': [18, 19, 20, 21, 22]
    },
    'Saturday': {
        'hours': '12PM-2PM, 6PM-10PM',
        'total_hours': 6,
        'target_earnings': 200,
        'optimal_hours': [12, 13, 18, 19, 20, 21]
    },
    'Sunday': {
        'hours': '11AM-1PM, 5PM-9PM',
        'total_hours': 6,
        'target_earnings': 175,
        'optimal_hours': [11, 12, 17, 18, 19, 20]
    }
}

# Peak recommended hours: 6PM-11PM (18-22)
PEAK_HOURS = [18, 19, 20, 21, 22]

# Spending recommendations
SPENDING_RECOMMENDATIONS = {
    'avoid_raising_canes': True,
    'meal_prep_weekend': True,
    'pack_snacks_late_night': True,
    'reduce_convenience_stores': True,
    'target_spending': 811  # After optimization from $1,281
}

# ============================================================================
# ANALYSIS
# ============================================================================

def analyze_schedule_adherence(trips):
    """Compare actual work hours to recommended schedule"""
    
    print("=" * 100)
    print("SCHEDULE ADHERENCE ANALYSIS")
    print("=" * 100)
    print("\nComparing actual work patterns vs. recommended optimal schedule\n")
    
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    results = []
    
    for day in dow_order:
        recommended = RECOMMENDED_SCHEDULE[day]
        actual_trips = trips[trips['Trip_DayOfWeek'] == day]
        
        # Count trips during recommended hours
        optimal_trips = actual_trips[actual_trips['Trip_Hour'].isin(recommended['optimal_hours'])]
        non_optimal_trips = actual_trips[~actual_trips['Trip_Hour'].isin(recommended['optimal_hours'])]
        
        # Calculate efficiency
        total_trips = len(actual_trips)
        optimal_count = len(optimal_trips)
        non_optimal_count = len(non_optimal_trips)
        
        if total_trips > 0:
            optimal_pct = (optimal_count / total_trips) * 100
        else:
            optimal_pct = 0
        
        results.append({
            'Day': day,
            'Recommended Hours': recommended['hours'],
            'Total Trips': total_trips,
            'Optimal Hour Trips': optimal_count,
            'Non-Optimal Trips': non_optimal_count,
            'Optimal %': optimal_pct,
            'Target Earnings': recommended['target_earnings']
        })
    
    results_df = pd.DataFrame(results)
    
    print(results_df.to_string(index=False))
    
    # Overall adherence
    total_trips = results_df['Total Trips'].sum()
    total_optimal = results_df['Optimal Hour Trips'].sum()
    overall_adherence = (total_optimal / total_trips) * 100 if total_trips > 0 else 0
    
    print(f"\n{'=' * 100}")
    print(f"OVERALL SCHEDULE ADHERENCE: {overall_adherence:.1f}%")
    print(f"Total Trips: {total_trips}")
    print(f"Optimal Hour Trips: {total_optimal} ({overall_adherence:.1f}%)")
    print(f"Non-Optimal Hour Trips: {total_trips - total_optimal} ({100-overall_adherence:.1f}%)")
    
    return results_df

def analyze_peak_hour_usage(trips):
    """Analyze how much work happened during peak hours (6PM-11PM)"""
    
    print("\n" + "=" * 100)
    print("PEAK HOUR UTILIZATION (6PM-11PM)")
    print("=" * 100)
    
    peak_trips = trips[trips['Trip_Hour'].isin(PEAK_HOURS)]
    non_peak_trips = trips[~trips['Trip_Hour'].isin(PEAK_HOURS)]
    
    print(f"\nRecommended Peak Hours: 6PM-11PM (18:00-22:00)")
    print(f"Peak Hour Trips: {len(peak_trips)} ({len(peak_trips)/len(trips)*100:.1f}%)")
    print(f"Non-Peak Hour Trips: {len(non_peak_trips)} ({len(non_peak_trips)/len(trips)*100:.1f}%)")
    
    print("\nActual distribution by hour:")
    hourly = trips.groupby('Trip_Hour').size().sort_values(ascending=False)
    
    for hour in hourly.index[:15]:
        count = hourly[hour]
        pct = count / len(trips) * 100
        is_peak = "✓ PEAK" if hour in PEAK_HOURS else ""
        print(f"  {hour:02d}:00 - {count:3d} trips ({pct:5.1f}%) {is_peak}")

def analyze_spending_adherence(expenses):
    """Compare actual spending to recommendations"""
    
    print("\n" + "=" * 100)
    print("SPENDING BEHAVIOR ANALYSIS")
    print("=" * 100)
    
    # Monthly spending
    monthly_spending = expenses.groupby('Month')['Amount'].sum()
    avg_monthly = monthly_spending.mean()
    
    print(f"\nRecommended Monthly Spending: ${SPENDING_RECOMMENDATIONS['target_spending']:.2f}")
    print(f"Actual Average Monthly Spending: ${avg_monthly:.2f}")
    print(f"Gap: ${avg_monthly - SPENDING_RECOMMENDATIONS['target_spending']:.2f}")
    
    if avg_monthly > SPENDING_RECOMMENDATIONS['target_spending']:
        print(f"Status: ❌ OVER TARGET by ${avg_monthly - SPENDING_RECOMMENDATIONS['target_spending']:.2f}/month")
    else:
        print(f"Status: ✓ UNDER TARGET by ${SPENDING_RECOMMENDATIONS['target_spending'] - avg_monthly:.2f}/month")
    
    # Raising Canes analysis
    print("\n" + "-" * 100)
    print("RAISING CANES SPENDING (Recommended: AVOID)")
    print("-" * 100)
    
    raising_canes = expenses[expenses['Merchant'].str.upper().str.contains('RAISING CANES', na=False)]
    
    if len(raising_canes) > 0:
        total_rc = raising_canes['Amount'].sum()
        visits = len(raising_canes)
        avg_per_visit = total_rc / visits
        monthly_rc = total_rc / 5  # 5 months of data
        
        print(f"Total Raising Canes Spending: ${total_rc:.2f}")
        print(f"Visits: {visits}")
        print(f"Average per visit: ${avg_per_visit:.2f}")
        print(f"Monthly average: ${monthly_rc:.2f}")
        print(f"Status: ❌ SHOULD ELIMINATE - Wasting ${monthly_rc:.2f}/month")
    else:
        print("Status: ✓ No Raising Canes spending found")
    
    # Weekend spending (meal prep recommendation)
    print("\n" + "-" * 100)
    print("WEEKEND SPENDING (Recommended: MEAL PREP to reduce)")
    print("-" * 100)
    
    weekend_spending = expenses[expenses['DayOfWeek'].isin(['Saturday', 'Sunday'])]
    weekday_spending = expenses[~expenses['DayOfWeek'].isin(['Saturday', 'Sunday'])]
    
    weekend_total = weekend_spending['Amount'].sum()
    weekday_total = weekday_spending['Amount'].sum()
    
    weekend_avg_day = weekend_total / (len(expenses['Date'].dt.date.unique()) / 7 * 2)  # Approx weekend days
    weekday_avg_day = weekday_total / (len(expenses['Date'].dt.date.unique()) / 7 * 5)  # Approx weekday days
    
    print(f"Weekend Spending: ${weekend_total:.2f}")
    print(f"Weekday Spending: ${weekday_total:.2f}")
    print(f"Average Weekend Day: ${weekend_avg_day:.2f}")
    print(f"Average Weekday Day: ${weekday_avg_day:.2f}")
    
    if weekend_avg_day > weekday_avg_day:
        print(f"Status: ❌ Spending ${weekend_avg_day - weekday_avg_day:.2f} MORE per day on weekends")
        print("Recommendation: Meal prep for Sat/Sun to reduce this gap")
    else:
        print("Status: ✓ Weekend spending is controlled")
    
    # Convenience store analysis
    print("\n" + "-" * 100)
    print("CONVENIENCE STORE SPENDING (Recommended: PACK SNACKS)")
    print("-" * 100)
    
    convenience = expenses[expenses['Category'].isin(['Convenience Store', 'Personal/Convenience'])]
    
    if len(convenience) > 0:
        total_conv = convenience['Amount'].sum()
        visits_conv = len(convenience)
        monthly_conv = total_conv / 5
        
        print(f"Total Convenience Store Spending: ${total_conv:.2f}")
        print(f"Visits: {visits_conv}")
        print(f"Monthly average: ${monthly_conv:.2f}")
        print(f"Status: ❌ REDUCE - Pack snacks to save ${monthly_conv:.2f}/month")
    else:
        print("Status: ✓ Minimal convenience store spending")

def identify_improvement_opportunities(trips, expenses):
    """Identify specific areas where behavior doesn't match recommendations"""
    
    print("\n" + "=" * 100)
    print("IMPROVEMENT OPPORTUNITIES")
    print("=" * 100)
    
    opportunities = []
    
    # 1. Working during low-value hours
    low_value_hours = [2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 15, 16]  # Non-peak hours
    low_value_trips = trips[trips['Trip_Hour'].isin(low_value_hours)]
    
    if len(low_value_trips) > 0:
        pct = len(low_value_trips) / len(trips) * 100
        opportunities.append({
            'Area': 'Working Low-Value Hours',
            'Current': f'{len(low_value_trips)} trips ({pct:.1f}%)',
            'Recommendation': 'Shift these trips to peak hours (6PM-11PM)',
            'Potential Impact': f'Could increase efficiency by focusing on peak demand'
        })
    
    # 2. Working too many days
    work_days = len(trips['Trip_Date'].unique())
    recommended_days = 26  # ~26 days per month per schedule
    
    if work_days > recommended_days * 5 / 4:  # 5 months
        opportunities.append({
            'Area': 'Working Too Many Days',
            'Current': f'{work_days} days worked',
            'Recommendation': f'Target {recommended_days} strategic days/month',
            'Potential Impact': 'Reduce burnout, maintain earnings'
        })
    
    # 3. Restaurant spending
    dining = expenses[expenses['Category'].isin(['Dining Restaurants', 'Fast Food', 'Dining - Personal'])]
    if len(dining) > 0:
        dining_total = dining['Amount'].sum()
        dining_monthly = dining_total / 5
        
        if dining_monthly > 50:
            opportunities.append({
                'Area': 'Dining Expenses While Working',
                'Current': f'${dining_monthly:.2f}/month on dining',
                'Recommendation': 'Meal prep + pack snacks',
                'Potential Impact': f'Save ${dining_monthly * 0.7:.2f}/month'
            })
    
    # 4. Uncategorized spending at pickup locations
    uncategorized = expenses[expenses['Category'] == 'Uncategorized']
    if len(uncategorized) > 0:
        uncat_total = uncategorized['Amount'].sum()
        uncat_monthly = uncat_total / 5
        
        opportunities.append({
            'Area': 'Impulse Spending at Work Locations',
            'Current': f'${uncat_monthly:.2f}/month uncategorized (72% at pickup locations)',
            'Recommendation': 'Awareness + pre-planning before shifts',
            'Potential Impact': f'Save ${uncat_monthly * 0.5:.2f}/month'
        })
    
    # Print opportunities
    print("\nTop Opportunities to Match Optimal Plan:\n")
    for i, opp in enumerate(opportunities, 1):
        print(f"{i}. {opp['Area']}")
        print(f"   Current State: {opp['Current']}")
        print(f"   Recommendation: {opp['Recommendation']}")
        print(f"   Impact: {opp['Potential Impact']}")
        print()

def generate_comparison_report(trips, expenses):
    """Generate overall comparison"""
    
    print("\n" + "=" * 100)
    print("SUMMARY: RECOMMENDED vs. ACTUAL")
    print("=" * 100)
    
    # Schedule adherence
    optimal_hours = []
    for day, info in RECOMMENDED_SCHEDULE.items():
        optimal_hours.extend(info['optimal_hours'])
    
    optimal_trips = trips[trips['Trip_Hour'].isin(optimal_hours)]
    schedule_adherence = len(optimal_trips) / len(trips) * 100
    
    # Spending adherence
    monthly_spending = expenses['Amount'].sum() / 5
    target_spending = SPENDING_RECOMMENDATIONS['target_spending']
    spending_gap = monthly_spending - target_spending
    
    # Peak hours
    peak_trips = trips[trips['Trip_Hour'].isin(PEAK_HOURS)]
    peak_usage = len(peak_trips) / len(trips) * 100
    
    print(f"\n📊 SCHEDULE PERFORMANCE")
    print(f"  Recommended optimal hour adherence: {schedule_adherence:.1f}%")
    print(f"  Peak hour usage (6PM-11PM): {peak_usage:.1f}%")
    
    if schedule_adherence < 50:
        print(f"  Status: ❌ LOW ADHERENCE - Significant opportunity to improve efficiency")
    elif schedule_adherence < 70:
        print(f"  Status: ⚠️  MODERATE - Room for improvement")
    else:
        print(f"  Status: ✓ GOOD - Mostly following optimal schedule")
    
    print(f"\n💰 SPENDING PERFORMANCE")
    print(f"  Target: ${target_spending:.2f}/month")
    print(f"  Actual: ${monthly_spending:.2f}/month")
    print(f"  Gap: ${spending_gap:.2f}/month")
    
    if spending_gap > 300:
        print(f"  Status: ❌ SIGNIFICANTLY OVER TARGET")
    elif spending_gap > 100:
        print(f"  Status: ⚠️  OVER TARGET")
    else:
        print(f"  Status: ✓ NEAR TARGET")
    
    print(f"\n🎯 POTENTIAL MONTHLY SAVINGS")
    print(f"  If schedule optimized: Increase efficiency by ~20%")
    print(f"  If spending reduced to target: Save ${spending_gap:.2f}/month")
    print(f"  Combined impact: ${spending_gap:.2f}/month + better work-life balance")

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("Loading data...")
    trips = load_trips()
    expenses = load_expenses()
    
    print(f"\nData loaded:")
    print(f"  Trips: {len(trips)}")
    print(f"  Expenses: {len(expenses)} transactions")
    print(f"  Period: Aug-Dec 2025\n")
    
    # Run analyses
    analyze_schedule_adherence(trips)
    analyze_peak_hour_usage(trips)
    analyze_spending_adherence(expenses)
    identify_improvement_opportunities(trips, expenses)
    generate_comparison_report(trips, expenses)
    
    print("\n" + "=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)

if __name__ == "__main__":
    main()
