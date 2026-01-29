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
        <h1 className="text-5xl font-black text-blue-600 mb-3 uppercase tracking-tight">
          Courier Business Analytics
        </h1>
        <p className="text-xl text-black font-bold">
          Comprehensive analysis and optimization tools for your courier operations
        </p>
        <p className="text-gray-700 mt-2 font-bold">
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
          <Link to="/schedule" className="block">
            <GradientCard
              title="Schedule Optimization"
              description="Optimal work schedule targeting $3,050/month with minimal effort. Peak hours: 6-11 PM."
              icon={Calendar}
              badge={{ text: 'RECOMMENDED', variant: 'important' }}
            />
          </Link>

          <Link to="/expenses" className="block">
            <GradientCard
              title="Expense Analysis"
              description="Complete breakdown: $1,158 reimbursable vs. $5,250 personal spending over 5 months."
              icon={Receipt}
              badge={{ text: 'KEY INSIGHTS', variant: 'new' }}
            />
          </Link>

          <Link to="/performance" className="block">
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
            <p className="text-black font-bold">
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
                  className="flex items-center justify-between p-4 bg-blue-600 border-3 border-black text-white"
                >
                  <div>
                    <div className="font-black">{slot.time}</div>
                    <div className="text-sm font-bold">{slot.trips} trips</div>
                  </div>
                  <span className="badge bg-white text-blue-600">{slot.status}</span>
                </div>
              ))}
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Top Revenue Zones">
          <div className="space-y-4">
            <p className="text-black font-bold">These three zones represent 23% of all orders:</p>
            <div className="space-y-3">
              {[
                { zone: 'TX 75206', trips: 91, percent: '8.5%' },
                { zone: 'TX 75204', trips: 81, percent: '7.5%' },
                { zone: 'TX 75219', trips: 74, percent: '6.9%' },
              ].map((zone) => (
                <div
                  key={zone.zone}
                  className="flex items-center justify-between p-4 border-4 border-blue-600 hover:bg-blue-50 transition-colors"
                >
                  <div>
                    <div className="font-black text-blue-600">{zone.zone}</div>
                    <div className="text-sm text-black font-bold">{zone.trips} trips</div>
                  </div>
                  <span className="text-2xl font-black text-blue-600">{zone.percent}</span>
                </div>
              ))}
            </div>
            <p className="text-sm text-gray-700 mt-4 font-bold">
              Strategy: Focus 60% of working time in these zones. Route clustering can save ~20% in
              dead mileage.
            </p>
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Monthly Earnings Breakdown">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-black mb-4 uppercase">To Hit $3,050/month you need:</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-green-400 border-4 border-black">
                <span className="font-bold">8 days @ $200</span>
                <span className="font-black text-black">$1,600</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-cyan-400 border-4 border-black">
                <span className="font-bold">4 days @ $100</span>
                <span className="font-black text-black">$400</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-yellow-400 border-4 border-black">
                <span className="font-bold">14 days @ $75</span>
                <span className="font-black text-black">$1,050</span>
              </div>
            </div>
          </div>
          <div>
            <h3 className="text-lg font-black mb-4 uppercase">Current Status:</h3>
            <div className="space-y-4">
              <div className="p-4 bg-blue-600 border-4 border-black text-white">
                <div className="text-sm font-bold">Monthly Average</div>
                <div className="text-3xl font-black">${monthlyEarnings}</div>
                <div className="text-sm font-bold">Gap to target: ${targetGap}</div>
              </div>
              <div className="p-4 border-4 border-green-600 bg-green-100">
                <div className="text-sm text-black font-bold">Good News:</div>
                <div className="font-black text-black">
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
