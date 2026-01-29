import { Link } from 'react-router-dom'
import { Calendar, DollarSign, TrendingUp, ArrowRight, Car, Receipt } from 'lucide-react'
import { StatCard } from '@/components/StatCard'
import { SectionCard } from '@/components/SectionCard'
import { GradientCard } from '@/components/GradientCard'
import { Alert } from '@/components/Alert'

export function Dashboard() {
  const monthlyEarnings = 1985
  const monthlyExpenses = 1667
  const netIncome = monthlyEarnings - monthlyExpenses
  const targetEarnings = 3050
  const targetGap = targetEarnings - monthlyEarnings
  const totalTrips = 1077

  return (
    <div className="space-y-8">
      <header className="section-card">
        <h1 className="text-5xl font-bold text-primary mb-3">
          Courier Business Analytics
        </h1>
        <p className="text-xl text-gray-600">
          Comprehensive analysis and optimization tools for your courier operations
        </p>
        <p className="text-gray-500 mt-2">
          Analysis Period: August - December 2025
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Trips"
          value={totalTrips}
          label="5 months analyzed"
          icon={Car}
        />
        <StatCard
          title="Monthly Target"
          value={`$${targetEarnings.toLocaleString()}`}
          label="Optimized earnings goal"
          icon={TrendingUp}
        />
        <StatCard
          title="Current Earnings"
          value={`$${monthlyEarnings.toLocaleString()}`}
          label="Per month average"
          icon={DollarSign}
        />
        <StatCard
          title="Net Income"
          value={`$${netIncome.toLocaleString()}`}
          label="After expenses"
          icon={Receipt}
        />
      </div>

      <Alert variant="error" title="Data Model Corrected (Phase 9)">
        Previous metrics had calculation errors. Actual monthly earnings: ${monthlyEarnings} (not
        $2,165). Actual spending: ${Math.round(monthlyExpenses)} (not $1,282). See corrected reports
        below.
      </Alert>

      <Alert variant="warning" title="Spending Now Fully Accounted">
        The $8,084 is not "untracked" - it's <strong>$4,565 customer purchases</strong> (matched to
        trips via cross-reference, should be reimbursed!) + <strong>$241 EV charging</strong>{' '}
        (business expense) + <strong>$3,528 true personal</strong>. Monthly net improves from $318
        to <strong>$1,279 with customer reimbursements!</strong> Uber still has $900 payment gap.
      </Alert>

      <SectionCard
        title="Key Reports & Analysis"
        subtitle="Explore your business data and optimization opportunities"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Link to="/schedule">
            <GradientCard
              title="Schedule Optimization"
              description="Optimal work schedule targeting $3,050/month with minimal effort. Peak hours: 6-11 PM."
              icon={Calendar}
              badge={{ text: 'RECOMMENDED', variant: 'important' }}
            />
          </Link>

          <Link to="/expenses">
            <GradientCard
              title="Expense Analysis"
              description="Complete breakdown: $1,158 reimbursable vs. $5,250 personal spending over 5 months."
              icon={Receipt}
              badge={{ text: 'KEY INSIGHTS', variant: 'new' }}
            />
          </Link>

          <Link to="/performance">
            <GradientCard
              title="Performance Review"
              description="Compare actual behavior against optimal recommendations. Current adherence: 33.3%"
              icon={TrendingUp}
              badge={{ text: 'NEEDS ATTENTION', variant: 'analysis' }}
            />
          </Link>
        </div>
      </SectionCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <SectionCard title="Peak Performance Hours">
          <div className="space-y-4">
            <p className="text-gray-600">
              Work these hours aggressively for maximum earnings:
            </p>
            <div className="space-y-3">
              {[
                { time: '10 PM - 11 PM', trips: 132, status: 'PEAK' },
                { time: '11 PM - 12 AM', trips: 107, status: 'PEAK' },
                { time: '9 PM - 10 PM', trips: 98, status: 'PEAK' },
                { time: '8 PM - 9 PM', trips: 89, status: 'PEAK' },
              ].map((slot) => (
                <div
                  key={slot.time}
                  className="flex items-center justify-between p-4 bg-gradient-primary rounded-lg text-white"
                >
                  <div>
                    <div className="font-bold">{slot.time}</div>
                    <div className="text-sm opacity-90">{slot.trips} trips</div>
                  </div>
                  <span className="badge bg-white text-primary font-bold">{slot.status}</span>
                </div>
              ))}
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Top Revenue Zones">
          <div className="space-y-4">
            <p className="text-gray-600">These three zones represent 23% of all orders:</p>
            <div className="space-y-3">
              {[
                { zone: 'TX 75206', trips: 91, percent: '8.5%' },
                { zone: 'TX 75204', trips: 81, percent: '7.5%' },
                { zone: 'TX 75219', trips: 74, percent: '6.9%' },
              ].map((zone) => (
                <div
                  key={zone.zone}
                  className="flex items-center justify-between p-4 border-2 border-primary rounded-lg hover:bg-primary/5 transition-colors"
                >
                  <div>
                    <div className="font-bold text-primary">{zone.zone}</div>
                    <div className="text-sm text-gray-600">{zone.trips} trips</div>
                  </div>
                  <span className="text-2xl font-bold text-primary">{zone.percent}</span>
                </div>
              ))}
            </div>
            <p className="text-sm text-gray-500 mt-4">
              Strategy: Focus 60% of working time in these zones. Route clustering can save ~20% in
              dead mileage.
            </p>
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Monthly Earnings Breakdown">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-bold mb-4">To Hit $3,050/month you need:</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-green-50 border-l-4 border-green-500 rounded">
                <span>8 days @ $200</span>
                <span className="font-bold text-green-700">$1,600</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-blue-50 border-l-4 border-blue-500 rounded">
                <span>4 days @ $100</span>
                <span className="font-bold text-blue-700">$400</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-purple-50 border-l-4 border-primary rounded">
                <span>14 days @ $75</span>
                <span className="font-bold text-primary">$1,050</span>
              </div>
            </div>
          </div>
          <div>
            <h3 className="text-lg font-bold mb-4">Current Status:</h3>
            <div className="space-y-4">
              <div className="p-4 bg-gradient-primary rounded-lg text-white">
                <div className="text-sm opacity-90">Monthly Average</div>
                <div className="text-3xl font-bold">${monthlyEarnings}</div>
                <div className="text-sm opacity-90">Gap to target: ${targetGap}</div>
              </div>
              <div className="p-4 border-2 border-green-500 rounded-lg">
                <div className="text-sm text-gray-600">Good News:</div>
                <div className="font-semibold text-green-700">
                  You already have 4 guaranteed $200 days locked in (Tue, Thu, Fri, Sat)
                </div>
              </div>
            </div>
          </div>
        </div>
      </SectionCard>

      <div className="flex justify-center">
        <Link
          to="/schedule"
          className="btn-primary flex items-center space-x-2 text-lg px-8 py-4"
        >
          <span>View Complete Schedule Optimization</span>
          <ArrowRight className="w-5 h-5" />
        </Link>
      </div>
    </div>
  )
}
