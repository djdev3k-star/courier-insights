import { DollarSign, TrendingUp, Receipt, ShoppingBag } from 'lucide-react'
import { SectionCard } from '@/components/SectionCard'
import { StatCard } from '@/components/StatCard'
import { Alert } from '@/components/Alert'
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts'

export function Expenses() {
  const totalExpenses = 8334
  const reimbursable = 1158
  const customerPurchases = 4565
  const evCharging = 241
  const truePersonal = 3528

  const categoryData = [
    { name: 'Customer Purchases', value: customerPurchases, color: '#667eea' },
    { name: 'True Personal', value: truePersonal, color: '#764ba2' },
    { name: 'EV Charging', value: evCharging, color: '#4ade80' },
    { name: 'Reimbursable', value: reimbursable, color: '#f87171' },
  ]

  const topMerchants = [
    { name: 'Raising Canes', amount: 814, visits: 27, type: 'Food' },
    { name: 'Whataburger', amount: 456, visits: 18, type: 'Food' },
    { name: 'QuikTrip', amount: 389, visits: 24, type: 'Gas/Snacks' },
    { name: 'McDonald\'s', amount: 312, visits: 15, type: 'Food' },
    { name: 'Walmart', amount: 287, visits: 8, type: 'Groceries' },
  ]

  return (
    <div className="space-y-8">
      <header className="section-card">
        <h1 className="text-5xl font-bold text-primary mb-3">Expense Analysis</h1>
        <p className="text-xl text-gray-600">
          Complete breakdown of spending patterns and optimization opportunities
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Expenses"
          value={`$${totalExpenses.toLocaleString()}`}
          label="5 months (Aug-Dec)"
          icon={DollarSign}
        />
        <StatCard
          title="Customer Purchases"
          value={`$${customerPurchases.toLocaleString()}`}
          label="Should be reimbursed"
          icon={ShoppingBag}
        />
        <StatCard
          title="True Personal"
          value={`$${truePersonal.toLocaleString()}`}
          label="Actual personal spending"
          icon={Receipt}
        />
        <StatCard
          title="Monthly Avg"
          value={`$${Math.round(totalExpenses / 5).toLocaleString()}`}
          label="Per month"
          icon={TrendingUp}
        />
      </div>

      <Alert variant="success" title="Spending Mystery Solved!">
        The $8,084 is now fully accounted for: <strong>$4,565 customer purchases</strong> (matched
        to trips, should be reimbursed!) + <strong>$241 EV charging</strong> (business expense) +{' '}
        <strong>$3,528 true personal</strong>. With customer reimbursements, monthly net improves
        from $318 to <strong>$1,279!</strong>
      </Alert>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <SectionCard title="Spending Breakdown">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value: number) => `$${value.toLocaleString()}`} />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-6 space-y-2">
            {categoryData.map((cat) => (
              <div key={cat.name} className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-4 h-4 rounded" style={{ backgroundColor: cat.color }} />
                  <span className="font-medium">{cat.name}</span>
                </div>
                <span className="font-bold">${cat.value.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="Top Spending Merchants">
          <div className="space-y-3">
            {topMerchants.map((merchant, index) => (
              <div
                key={merchant.name}
                className="flex items-center justify-between p-4 border-2 border-gray-200 rounded-lg hover:border-primary transition-colors"
              >
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 bg-gradient-primary rounded-full flex items-center justify-center text-white font-bold">
                    {index + 1}
                  </div>
                  <div>
                    <div className="font-bold">{merchant.name}</div>
                    <div className="text-sm text-gray-600">
                      {merchant.visits} visits • {merchant.type}
                    </div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xl font-bold text-primary">${merchant.amount}</div>
                  <div className="text-xs text-gray-500">
                    ${Math.round(merchant.amount / merchant.visits)}/visit
                  </div>
                </div>
              </div>
            ))}
          </div>
          <Alert variant="warning">
            <strong>Raising Canes Alert:</strong> $814 spent at 27 visits. This is your #1
            spending trigger at pickup locations. Meal prep could save $470/month.
          </Alert>
        </SectionCard>
      </div>

      <SectionCard title="Spending Patterns & Insights">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 bg-red-50 border-2 border-red-200 rounded-xl">
            <h3 className="text-lg font-bold text-red-700 mb-2">High Spending Days</h3>
            <ul className="space-y-2 text-sm">
              <li className="flex justify-between">
                <span>Sundays</span>
                <span className="font-bold">Highest</span>
              </li>
              <li className="flex justify-between">
                <span>Saturdays</span>
                <span className="font-bold">High</span>
              </li>
              <li className="text-gray-600">
                Weekend work correlates with higher food spending at pickup locations
              </li>
            </ul>
          </div>

          <div className="p-6 bg-yellow-50 border-2 border-yellow-200 rounded-xl">
            <h3 className="text-lg font-bold text-yellow-700 mb-2">Spending Triggers</h3>
            <ul className="space-y-2 text-sm">
              <li className="flex items-start">
                <span className="text-yellow-600 mr-2">⚠️</span>
                <span>72% spending at restaurant pickup locations</span>
              </li>
              <li className="flex items-start">
                <span className="text-yellow-600 mr-2">⚠️</span>
                <span>Waiting for orders = impulse purchases</span>
              </li>
              <li className="flex items-start">
                <span className="text-yellow-600 mr-2">⚠️</span>
                <span>Late night shifts = higher food spending</span>
              </li>
            </ul>
          </div>

          <div className="p-6 bg-green-50 border-2 border-green-200 rounded-xl">
            <h3 className="text-lg font-bold text-green-700 mb-2">Optimization Ideas</h3>
            <ul className="space-y-2 text-sm">
              <li className="flex items-start">
                <span className="text-green-600 mr-2">✓</span>
                <span>Meal prep before shifts: Save $470/mo</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">✓</span>
                <span>Pack snacks & water: Reduce impulse buys</span>
              </li>
              <li className="flex items-start">
                <span className="text-green-600 mr-2">✓</span>
                <span>Track customer purchases separately</span>
              </li>
            </ul>
          </div>
        </div>
      </SectionCard>

      <SectionCard title="Category Breakdown">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { name: 'Fast Food', amount: 2891, percent: 34.7 },
            { name: 'Restaurants', amount: 1674, percent: 20.1 },
            { name: 'Gas & Fuel', amount: 987, percent: 11.8 },
            { name: 'Groceries', amount: 643, percent: 7.7 },
            { name: 'Convenience', amount: 534, percent: 6.4 },
            { name: 'EV Charging', amount: 241, percent: 2.9 },
            { name: 'Retail', amount: 428, percent: 5.1 },
            { name: 'Other', amount: 936, percent: 11.2 },
          ].map((cat) => (
            <div key={cat.name} className="p-4 border-2 border-gray-200 rounded-lg text-center">
              <div className="text-xs text-gray-500 uppercase mb-1">{cat.name}</div>
              <div className="text-2xl font-bold text-primary">${cat.amount}</div>
              <div className="text-sm text-gray-600">{cat.percent}%</div>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  )
}
