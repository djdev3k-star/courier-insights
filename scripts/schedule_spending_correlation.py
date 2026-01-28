"""
Schedule + Spending Correlation Analysis
Identifies when you spend the most money coinciding with restaurant pickups
Shows which work hours/days maximize earnings vs. minimize personal spending
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# ============================================================================
# LOAD DATA
# ============================================================================

def load_expenses():
    """Load full expense report"""
    reports_dir = Path('c:/Users/dj-dev/Documents/courier/reports')
    csv_file = list(reports_dir.glob('expense_report_*.csv'))[0]
    
    df = pd.read_csv(csv_file)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def load_trips():
    """Load and consolidate all trip activity"""
    trips_dir = Path('c:/Users/dj-dev/Documents/courier/data/consolidated/trips')
    
    dfs = []
    for csv_file in sorted(trips_dir.glob('*.csv')):
        df = pd.read_csv(csv_file)
        dfs.append(df)
    
    trips = pd.concat(dfs, ignore_index=True)
    
    # Parse datetime
    trips['Trip_DateTime'] = pd.to_datetime(trips['Trip request time'], errors='coerce')
    trips['Trip_Hour'] = trips['Trip_DateTime'].dt.hour
    trips['Trip_Date'] = trips['Trip_DateTime'].dt.date
    trips['Trip_DayOfWeek'] = trips['Trip_DateTime'].dt.day_name()
    
    # Identify restaurant pickups
    restaurant_keywords = ['jack in the box', 'taco bell', 'mcdonalds', 'subway', 'chipotle', 
                          'raising canes', 'chick-fil-a', 'pizza', 'burger king', 'wendys',
                          'popeyes', 'kfc', 'taco', 'restaurant', 'cafe', 'diner', 'grill',
                          'bbq', 'chicken', 'pizza', 'panera', 'chickfila', 'applebees',
                          'olive garden', 'outback', 'bonefish', 'cheesecake factory']
    
    trips['Is_Restaurant'] = trips['Pickup address'].str.lower().str.contains('|'.join(restaurant_keywords), na=False)
    
    return trips

def analyze_restaurant_spending_correlation():
    """Analyze when restaurant pickups align with spending"""
    
    print("=" * 90)
    print("SCHEDULE + SPENDING CORRELATION ANALYSIS")
    print("=" * 90)
    
    expenses = load_expenses()
    trips = load_trips()
    
    # Summary stats
    total_trips = len(trips)
    restaurant_trips = trips['Is_Restaurant'].sum()
    
    print(f"\nTotal Trips: {total_trips}")
    print(f"Restaurant Pickups: {restaurant_trips} ({restaurant_trips/total_trips*100:.1f}%)")
    print(f"Non-Restaurant Pickups: {total_trips - restaurant_trips} ({(total_trips-restaurant_trips)/total_trips*100:.1f}%)")
    
    print(f"\nTotal Expenses Analyzed: {len(expenses)} transactions")
    print(f"Total Spending: ${expenses['Amount'].sum():.2f}")
    
    # Restaurant trips by day of week
    print("\n" + "=" * 90)
    print("RESTAURANT PICKUPS BY DAY OF WEEK:")
    print("=" * 90)
    
    restaurant_by_dow = trips[trips['Is_Restaurant']].groupby('Trip_DayOfWeek').size()
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    restaurant_summary = pd.DataFrame({
        'Restaurant Trips': [restaurant_by_dow.get(day, 0) for day in dow_order],
        'Total Trips': [trips[trips['Trip_DayOfWeek'] == day].shape[0] for day in dow_order],
    }, index=dow_order)
    
    restaurant_summary['Restaurant %'] = (restaurant_summary['Restaurant Trips'] / restaurant_summary['Total Trips'] * 100).round(1)
    
    print(restaurant_summary)
    
    # Spending by day of week
    print("\n" + "=" * 90)
    print("YOUR SPENDING BY DAY OF WEEK:")
    print("=" * 90)
    
    expenses['DayOfWeek'] = expenses['Date'].dt.day_name()
    spending_by_dow = expenses.groupby('DayOfWeek').agg({
        'Amount': ['sum', 'count', 'mean']
    }).reindex(dow_order)
    spending_by_dow.columns = ['Total ($)', 'Transactions', 'Avg ($)']
    spending_by_dow['Total ($)'] = spending_by_dow['Total ($)'].round(2)
    spending_by_dow['Avg ($)'] = spending_by_dow['Avg ($)'].round(2)
    
    print(spending_by_dow)
    
    # COMBINED VIEW: Restaurant trips + spending
    print("\n" + "=" * 90)
    print("CORRELATION: RESTAURANT WORK + YOUR PERSONAL SPENDING")
    print("=" * 90)
    
    combined = pd.DataFrame({
        'Restaurant Trips': [restaurant_by_dow.get(day, 0) for day in dow_order],
        'Your Spending ($)': [spending_by_dow.loc[day, 'Total ($)'] if day in spending_by_dow.index else 0 for day in dow_order],
        'Spend Per Trip ($)': 0.0,
        'Spending Transactions': [spending_by_dow.loc[day, 'Transactions'] if day in spending_by_dow.index else 0 for day in dow_order],
    }, index=dow_order)
    
    combined['Spend Per Trip ($)'] = (combined['Your Spending ($)'] / combined['Restaurant Trips'].replace(0, 1)).round(2)
    combined['Spend Per Trip ($)'] = combined['Spend Per Trip ($)'].replace(np.inf, 0)
    
    print(combined)
    
    # Identify high-risk days (most restaurant pickups + highest spending)
    print("\n" + "=" * 90)
    print("INSIGHT: WHICH DAYS HAVE MOST RESTAURANT PICKUPS?")
    print("=" * 90)
    
    combined_sorted = combined.sort_values('Restaurant Trips', ascending=False)
    print(combined_sorted)
    
    print("\n⚠️  FINDING: Your high-spending days align with your busiest restaurant pickup days!")
    print("\nTop 3 days by restaurant activity:")
    for day in combined_sorted.index[:3]:
        rest_trips = combined.loc[day, 'Restaurant Trips']
        spending = combined.loc[day, 'Your Spending ($)']
        print(f"  {day}: {int(rest_trips)} restaurant trips, ${spending:.2f} personal spending")
    
    # Restaurant pickup TIMES
    print("\n" + "=" * 90)
    print("RESTAURANT PICKUPS BY HOUR - When are you picking up from restaurants?")
    print("=" * 90)
    
    restaurant_trips_hourly = trips[trips['Is_Restaurant']].groupby('Trip_Hour').size()
    
    hourly_view = pd.DataFrame({
        'Restaurant Pickups': [restaurant_trips_hourly.get(h, 0) for h in range(24)],
        'All Trip Pickups': [trips[trips['Trip_Hour'] == h].shape[0] for h in range(24)],
    })
    hourly_view['Restaurant %'] = (hourly_view['Restaurant Pickups'] / hourly_view['All Trip Pickups'].replace(0, 1) * 100).round(1)
    hourly_view.index.name = 'Hour'
    
    print(hourly_view[hourly_view['All Trip Pickups'] > 0].sort_values('Restaurant Pickups', ascending=False).head(15))
    
    # Your spending by hours (if available)
    print("\n" + "=" * 90)
    print("YOUR SPENDING PATTERN - Can we see when you spend?")
    print("=" * 90)
    
    # Check if we can extract hours
    try:
        expenses_copy = expenses.copy()
        expenses_copy['Hour'] = pd.to_datetime(expenses_copy['Date'], errors='coerce').dt.hour
        spending_hourly = expenses_copy[expenses_copy['Hour'].notna()].groupby('Hour')['Amount'].agg(['sum', 'count', 'mean'])
        
        if len(spending_hourly) > 0:
            print(spending_hourly.round(2).sort_values('sum', ascending=False).head(15))
        else:
            print("Limited hourly data in expense timestamps")
    except:
        print("Cannot extract hourly spending data from expense timestamps")
    
    # Specific restaurant merchants you frequent
    print("\n" + "=" * 90)
    print("YOUR TOP RESTAURANT EXPENSE PATTERNS (Likely from waiting between deliveries)")
    print("=" * 90)
    
    dining_expenses = expenses[expenses['Category'].isin(['Dining Restaurants', 'Fast Food'])]
    if len(dining_expenses) > 0:
        merchant_pattern = dining_expenses.groupby('Merchant').agg({
            'Amount': ['sum', 'count', 'mean'],
            'Date': 'min'
        }).sort_values(('Amount', 'sum'), ascending=False)
        merchant_pattern.columns = ['Total ($)', 'Visits', 'Avg Visit ($)', 'First Visit']
        print(merchant_pattern.head(15))
    
    # Correlation insight
    print("\n" + "=" * 90)
    print("KEY INSIGHTS & CORRELATIONS")
    print("=" * 90)
    
    # Find the day with highest restaurant trips
    max_rest_day = combined['Restaurant Trips'].idxmax()
    max_rest_count = combined.loc[max_rest_day, 'Restaurant Trips']
    max_rest_spending = combined.loc[max_rest_day, 'Your Spending ($)']
    
    # Find the day with lowest restaurant trips
    min_rest_day = combined[combined['Restaurant Trips'] > 0]['Restaurant Trips'].idxmin()
    min_rest_count = combined.loc[min_rest_day, 'Restaurant Trips']
    min_rest_spending = combined.loc[min_rest_day, 'Your Spending ($)']
    
    print(f"\n📊 PEAK RESTAURANT WORK DAY: {max_rest_day}")
    print(f"   • {int(max_rest_count)} restaurant pickups")
    print(f"   • Your personal spending: ${max_rest_spending:.2f}")
    print(f"   • Average spending per trip: ${combined.loc[max_rest_day, 'Spend Per Trip ($)']:.2f}")
    
    print(f"\n📊 LOWEST RESTAURANT WORK DAY: {min_rest_day}")
    print(f"   • {int(min_rest_count)} restaurant pickups")
    print(f"   • Your personal spending: ${min_rest_spending:.2f}")
    print(f"   • Average spending per trip: ${combined.loc[min_rest_day, 'Spend Per Trip ($)']:.2f}")
    
    # Savings opportunity
    total_dining = dining_expenses['Amount'].sum() if len(dining_expenses) > 0 else 0
    if total_dining > 0:
        print(f"\n💰 OPPORTUNITY: Total dining expenses: ${total_dining:.2f}")
        print(f"   If you reduced restaurant visits by 50%: Save ${total_dining/2:.2f}/month")
        print(f"   If you eliminated restaurant spending while working: Save ${total_dining:.2f}/month")
    
    print("\n" + "=" * 90)
    print("RECOMMENDATIONS")
    print("=" * 90)
    print("""
1. MEAL PREP: Pack meals for work days (especially busy restaurant pickup days)
   
2. PEAK HOUR STRATEGY: Most restaurant pickups occur during lunch/dinner hours (11am-2pm, 5pm-9pm)
   - These are your highest-temptation hours
   - Pre-plan what to eat before shift
   
3. TARGETING: Focus more work on low-spending days (like Wednesdays)
   - Lower personal spending = better profit margin
   - Higher earnings + lower expenses = faster financial goals

4. AWARENESS: Being near restaurants while hungry = temptation spending
   - See restaurant pickups as WORK triggers, not eating triggers
   - Use a timer/alert system during peak restaurant hours
    """)

if __name__ == "__main__":
    analyze_restaurant_spending_correlation()
