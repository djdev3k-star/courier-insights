"""
Generate Visual Route Schedule Reference
"""

def print_weekly_schedule():
    """Print ASCII-based visual weekly schedule"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                   WEEKLY COURIER SCHEDULE - VISUAL GUIDE                   ║
║                    Optimized for Maximum Earnings & Efficiency            ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│                          DAILY HOUR BREAKDOWN                               │
│                    (Gray = Off | Light Blue = Light Shift |                │
│                     Cyan = Moderate | Blue = HIGH PRIORITY)                │
└─────────────────────────────────────────────────────────────────────────────┘

MONDAY - Moderate Day
Time:  06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01
Work:  ░░ ░░ ░░ ░░ ░░ ██ ██ ██ ░░ ░░ ░░ ░░ ░░ ██ ██ ██ ██ ░░ ░░ ░░
       └─ OFF ─┘ └──── OFF────┘ └──── OFF────┘ └── EVENING ──┘ └OFF─┘
Target: $150 | Strategy: Lunch shift (2h) + Evening peak (4h) | Total: 6h

TUESDAY - HIGH VALUE ⭐
Time:  06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01
Work:  ░░ ░░ ░░ ░░ ░░ ░░ ██ ██ ██ ░░ ░░ ░░ ░░ ░░ ██ ██ ██ ██ ░░ ░░
       └────OFF───┘ └────LUNCH────┘ └────OFF────┘ └── EVENING ──┘ └OFF─┘
Target: $200 | Strategy: Peak lunch (2h) + Extended evening (4h) | Total: 6h

WEDNESDAY - Moderate Day
Time:  06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01
Work:  ░░ ░░ ░░ ░░ ░░ ██ ██ ██ ░░ ░░ ░░ ██ ██ ░░ ░░ ░░ ░░ ░░ ░░ ░░
       └──OFF─┘ └────LUNCH────┘ └─EARLY DIN─┘ └──────OFF──────┘
Target: $100 | Strategy: Light shift, focused zones | Total: 3h

THURSDAY - HIGH VALUE ⭐
Time:  06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01
Work:  ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ██ ██ ██ ██ ██ ██ ░░ ░░
       └────────────────OFF───────────────┘ └─── EVENING PEAK ──┘ └OFF─┘
Target: $200 | Strategy: Full evening shift, peak momentum | Total: 5h

FRIDAY - HIGH VALUE ⭐
Time:  06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01
Work:  ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ██ ██ ██ ██ ██ ██ ░░ ░░
       └────────────────OFF───────────────┘ └─ WEEKEND PREP PEAK ┘ └OFF─┘
Target: $200 | Strategy: Full evening shift (premium rates) | Total: 5h

SATURDAY - HIGH VALUE ⭐
Time:  06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01
Work:  ░░ ░░ ░░ ░░ ░░ ██ ██ ██ ░░ ░░ ░░ ██ ██ ██ ██ ██ ██ ░░ ░░ ░░
       └──OFF─┘ └──LUNCH──┘ └─GAPS─┘ └─────EVENING/NIGHT PEAK─┘ └OFF─┘
Target: $200 | Strategy: Split shift (lunch + extended evening) | Total: 7h

SUNDAY - Light Day
Time:  06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01
Work:  ░░ ░░ ░░ ░░ ░░ ░░ ██ ██ ██ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░ ░░
       └────────OFF────┘ └──LUNCH──┘ └──────────OFF──────────┘
Target: $75 | Strategy: Light shift for platform visibility | Total: 2h

┌─────────────────────────────────────────────────────────────────────────────┐
│                          ZONE PRIORITY ROUTING                              │
└─────────────────────────────────────────────────────────────────────────────┘

PRIMARY ZONES (Focus 60% of time):
├─ TX 75206 (91 trips)  ─── Highest Volume Zone
├─ TX 75204 (81 trips)  ─── Second Highest
└─ TX 75219 (74 trips)  ─── Third Highest
   These 3 zones = 23% of ALL trips historically

SECONDARY ZONES (Fill capacity):
├─ TX 75208-1702 (51 trips)
├─ TX 75207 (44 trips)
├─ TX 75126 (42 trips)
└─ TX 75226 (42 trips)

ZONE STRATEGY:
During shifts, focus on PRIMARY zones first. Route clustering saves ~20% dead time.

┌─────────────────────────────────────────────────────────────────────────────┐
│                        HOURLY EARNINGS BENCHMARK                            │
└─────────────────────────────────────────────────────────────────────────────┘

Peak Hours (Target: $40-50/hour)
  22:00-23:00 ███████████████████████ 132 trips
  23:00-00:00 ███████████████░░░░░░░░ 107 trips
  21:00-22:00 ██████████░░░░░░░░░░░░░  98 trips
  20:00-21:00 ████████░░░░░░░░░░░░░░░  89 trips

Good Hours (Target: $25-40/hour)
  00:00-01:00 ████████░░░░░░░░░░░░░░░  85 trips
  19:00-20:00 ████████░░░░░░░░░░░░░░░  83 trips

OFF-PEAK (Avoid if possible)
  11:00-14:00 (Lunch) ██░░░░░░░░░░░░░░░░░░░░░░  Moderate volume, good rates
  All other times     Low volume, lower payoff

DECISION RULE:
If it's not during PEAK or GOOD hours, and you're not in PRIMARY zones,
go HOME and prep for next shift.

┌─────────────────────────────────────────────────────────────────────────────┐
│                       WEEKLY EARNINGS PROJECTION                            │
└─────────────────────────────────────────────────────────────────────────────┘

By Day:
  Monday ........ $150  (11am-1pm, 6pm-10pm)
  Tuesday ....... $200  (12pm-2pm, 6pm-10pm) ⭐
  Wednesday .... $100  (11am-1pm, 5pm-7pm)
  Thursday ..... $200  (6pm-11pm) ⭐
  Friday ....... $200  (6pm-11pm) ⭐
  Saturday ..... $200  (11am-2pm, 5pm-10pm) ⭐
  Sunday ....... $75   (12pm-2pm)
  ───────────────────
  WEEKLY TOTAL: $1,125

By Week (26 work days in typical month):
  High-Value Days (8 days @ $200) ............ $1,600
  Mid-Value Days (4 days @ $100) ............ $400
  Base Days (14 days @ $75) ................. $1,050
  ─────────────────────────────────────
  MONTHLY TOTAL: $3,050

┌─────────────────────────────────────────────────────────────────────────────┐
│                          EFFORT vs. EARNINGS MATRIX                         │
└─────────────────────────────────────────────────────────────────────────────┘

  EFFORT LEVEL
      ▲
  High│    THU  FRI  SAT     (5-7h, $200 each = $40/h)
      │     ⭐  ⭐  ⭐
   Med│ MON    TUE    WED    (3-6h, $100-150 = $25-50/h)
      │  ░     ⭐    ░
   Low│              SUN     (2h, $75 = $37.50/h)
      │                ░
      └─────────────────────────────────────────────► EARNINGS

Strategy: Cluster effort on high-payoff days. Minimize effort on low-demand days.

┌─────────────────────────────────────────────────────────────────────────────┐
│                         MONTH PLANNING CALENDAR                             │
└─────────────────────────────────────────────────────────────────────────────┘

WEEK 1:  Mon Tue Wed Thu Fri Sat Sun    = $1,125
         150 200 100 200 200 200  75

WEEK 2:  Mon Tue Wed Thu Fri Sat Sun    = $1,125
         150 200 100 200 200 200  75

WEEK 3:  Mon Tue Wed Thu Fri Sat Sun    = $1,125
         150 200 100 200 200 200  75

WEEK 4:  Mon Tue Wed Thu Fri Sat Sun    = $675  (Fewer work days in final week)
         150 200 100  —  —  —   75

TOTAL MONTH: $4,050 (28 days worked as scheduled)
TARGET MONTH: $3,050
BUFFER: $1,000 (33% cushion for underperformance)

⚠️  KEY PERFORMANCE INDICATORS (Track These):
  • $/mile (target: $0.30+)
  • $/hour (target: $40+)
  • Acceptance Rate (maintain: >95%)
  • Cancellation Rate (keep: <5%)
  • Trips per hour (aim: 2-2.5 trips/h)
  • Zone efficiency (track top 3 zones' performance weekly)

═══════════════════════════════════════════════════════════════════════════════

IMPLEMENTATION CHECKLIST:

Week 1-2:  Establish Schedule
  ☐ Block calendar with this schedule
  ☐ Set phone reminders 30min before shifts
  ☐ Identify geographic boundaries for primary zones
  ☐ Note which restaurants/stores open/close times
  ☐ Test split-shift approach on Tuesday

Week 3-4:  Optimize & Measure
  ☐ Track actual vs projected earnings daily
  ☐ Note any hours with 0-2 trip offers (adjust next time)
  ☐ Identify any unexpected peak periods
  ☐ Calculate efficiency metrics ($/mile, $/hour)
  ☐ Adjust zone focus if secondary zones outperforming primary

Month 2:   Execute & Refine
  ☐ Implement refined schedule based on Month 1 learnings
  ☐ Lock in consistent work hours for algorithm optimization
  ☐ Track weekly earnings trend
  ☐ Make one strategic adjustment mid-month if needed
  ☐ Document what worked vs. what didn't

═══════════════════════════════════════════════════════════════════════════════
""")

if __name__ == "__main__":
    print_weekly_schedule()
