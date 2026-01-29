import { TrendingUp, TrendingDown, Target, AlertCircle, CheckCircle, XCircle } from 'lucide-react'
import { SectionCard } from '@/components/SectionCard'
import { StatCard } from '@/components/StatCard'
import { Alert } from '@/components/Alert'

export function Performance() {
  const scheduleAdherence = 33.3
  const grade = 'F'
  const currentEarnings = 1985
  const targetEarnings = 3050
  const earningsGap = targetEarnings - currentEarnings
  const currentSpending = 1667
  const targetSpending = 811
  const spendingOverage = currentSpending - targetSpending

  const annualSavingsPotential = (earningsGap + spendingOverage) * 12

  return (
    <div className="space-y-8">
      <header className="section-card">
        <h1 className="text-5xl font-bold text-primary mb-3">Performance Analysis</h1>
        <p className="text-xl text-gray-600">
          Compare actual behavior against optimal recommendations
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Overall Grade"
          value={grade}
          label={`${scheduleAdherence}% adherence`}
          icon={Target}
        />
        <StatCard
          title="Earnings Gap"
          value={`-$${earningsGap}`}
          label="Below monthly target"
          icon={TrendingDown}
        />
        <StatCard
          title="Spending Over"
          value={`+$${spendingOverage}`}
          label="Above recommended"
          icon={AlertCircle}
        />
        <StatCard
          title="Savings Potential"
          value={`$${Math.round(annualSavingsPotential / 1000)}K`}
          label="Annual opportunity"
          icon={TrendingUp}
        />
      </div>

      <Alert variant="error" title="Action Required">
        Current performance is significantly below optimal. Following the recommended schedule and
        spending controls could increase annual net income by <strong>${annualSavingsPotential.toLocaleString()}</strong>.
      </Alert>

      <SectionCard title="Schedule Adherence Breakdown">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <h3 className="text-lg font-bold mb-4">Optimal Schedule Compliance</h3>
            <div className="space-y-4">
              {[
                {
                  metric: 'Peak Hours (6-11 PM)',
                  actual: '45%',
                  target: '70%',
                  status: 'poor',
                },
                {
                  metric: 'Optimal Days (Tue/Thu/Fri/Sat)',
                  actual: '38%',
                  target: '80%',
                  status: 'poor',
                },
                {
                  metric: 'Top 3 Zones Focus',
                  actual: '52%',
                  target: '60%',
                  status: 'fair',
                },
                {
                  metric: 'Split Shift Execution',
                  actual: '25%',
                  target: '75%',
                  status: 'poor',
                },
              ].map((item) => (
                <div key={item.metric} className="border-2 border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium">{item.metric}</span>
                    {item.status === 'poor' ? (
                      <XCircle className="w-5 h-5 text-red-500" />
                    ) : item.status === 'fair' ? (
                      <AlertCircle className="w-5 h-5 text-yellow-500" />
                    ) : (
                      <CheckCircle className="w-5 h-5 text-green-500" />
                    )}
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="flex-1">
                      <div className="text-sm text-gray-600 mb-1">Current: {item.actual}</div>
                      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className={`h-full ${
                            item.status === 'poor'
                              ? 'bg-red-500'
                              : item.status === 'fair'
                              ? 'bg-yellow-500'
                              : 'bg-green-500'
                          }`}
                          style={{ width: item.actual }}
                        />
                      </div>
                    </div>
                    <div className="text-sm font-bold text-primary">Target: {item.target}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 className="text-lg font-bold mb-4">Grade Breakdown</h3>
            <div className="space-y-4">
              <div className="p-6 bg-gradient-primary rounded-xl text-white">
                <div className="text-6xl font-bold text-center mb-4">{grade}</div>
                <div className="text-center text-lg opacity-90">{scheduleAdherence}% Overall Adherence</div>
              </div>

              <div className="space-y-3">
                <div className="p-4 bg-red-50 border-2 border-red-200 rounded-lg">
                  <div className="font-bold text-red-700 mb-1">Critical Issues (3)</div>
                  <ul className="text-sm text-red-600 space-y-1">
                    <li>• Not working recommended peak hours</li>
                    <li>• Missing optimal days consistently</li>
                    <li>• Split shifts not being executed</li>
                  </ul>
                </div>

                <div className="p-4 bg-yellow-50 border-2 border-yellow-200 rounded-lg">
                  <div className="font-bold text-yellow-700 mb-1">Needs Improvement (1)</div>
                  <ul className="text-sm text-yellow-600 space-y-1">
                    <li>• Geographic focus below target</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </SectionCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <SectionCard title="Earnings Analysis">
          <div className="space-y-4">
            <div className="p-6 bg-gradient-primary rounded-xl text-white">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm opacity-90">Current Monthly</span>
                <span className="text-3xl font-bold">${currentEarnings}</span>
              </div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm opacity-90">Target Monthly</span>
                <span className="text-3xl font-bold">${targetEarnings}</span>
              </div>
              <div className="border-t border-white/20 pt-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm opacity-90">Gap to Close</span>
                  <span className="text-2xl font-bold text-red-200">-${earningsGap}</span>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <h4 className="font-bold">How to Close the Gap:</h4>
              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded">
                  <span>Work peak hours (6-11 PM)</span>
                  <span className="font-bold text-green-700">+$1,200/mo</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded">
                  <span>Focus on optimal days</span>
                  <span className="font-bold text-green-700">+$800/mo</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded">
                  <span>Execute split shifts</span>
                  <span className="font-bold text-green-700">+$468/mo</span>
                </div>
              </div>
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Spending Control">
          <div className="space-y-4">
            <div className="p-6 bg-red-50 border-2 border-red-200 rounded-xl">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm text-red-700">Current Monthly</span>
                <span className="text-3xl font-bold text-red-700">${currentSpending}</span>
              </div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm text-green-700">Recommended Max</span>
                <span className="text-3xl font-bold text-green-700">${targetSpending}</span>
              </div>
              <div className="border-t border-red-200 pt-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-red-700">Over Budget</span>
                  <span className="text-2xl font-bold text-red-700">+${spendingOverage}</span>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <h4 className="font-bold">Spending Reduction Opportunities:</h4>
              <div className="space-y-2 text-sm">
                <div className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded">
                  <span>Meal prep vs. fast food</span>
                  <span className="font-bold text-green-700">-$470/mo</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded">
                  <span>Track customer purchases</span>
                  <span className="font-bold text-green-700">-$913/mo</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded">
                  <span>Reduce impulse spending</span>
                  <span className="font-bold text-green-700">-$286/mo</span>
                </div>
              </div>
            </div>
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Action Plan">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 border-2 border-primary rounded-xl">
            <div className="w-12 h-12 bg-gradient-primary rounded-full flex items-center justify-center text-white font-bold text-xl mb-4">
              1
            </div>
            <h3 className="text-lg font-bold mb-3">Immediate (This Week)</h3>
            <ul className="space-y-2 text-sm text-gray-700">
              <li>✓ Block calendar with optimal schedule</li>
              <li>✓ Set reminders for peak hours</li>
              <li>✓ Meal prep for next 3 days</li>
              <li>✓ Map top 3 zones in GPS</li>
            </ul>
          </div>

          <div className="p-6 border-2 border-primary rounded-xl">
            <div className="w-12 h-12 bg-gradient-primary rounded-full flex items-center justify-center text-white font-bold text-xl mb-4">
              2
            </div>
            <h3 className="text-lg font-bold mb-3">Short-term (This Month)</h3>
            <ul className="space-y-2 text-sm text-gray-700">
              <li>✓ Execute schedule for 4 weeks</li>
              <li>✓ Track daily $/hour and $/mile</li>
              <li>✓ Reduce fast food by 50%</li>
              <li>✓ Focus 60% time in top zones</li>
            </ul>
          </div>

          <div className="p-6 border-2 border-primary rounded-xl">
            <div className="w-12 h-12 bg-gradient-primary rounded-full flex items-center justify-center text-white font-bold text-xl mb-4">
              3
            </div>
            <h3 className="text-lg font-bold mb-3">Long-term (3 Months)</h3>
            <ul className="space-y-2 text-sm text-gray-700">
              <li>✓ Hit $3,050 monthly target</li>
              <li>✓ Reduce spending to $811/mo</li>
              <li>✓ Achieve 80%+ schedule adherence</li>
              <li>✓ Maintain Grade B or better</li>
            </ul>
          </div>
        </div>
      </SectionCard>

      <div className="p-8 bg-gradient-primary rounded-2xl text-white text-center">
        <h2 className="text-3xl font-bold mb-4">Potential Annual Impact</h2>
        <div className="text-6xl font-bold mb-4">${annualSavingsPotential.toLocaleString()}</div>
        <p className="text-xl opacity-90">
          By following recommendations, you could add this to your annual net income
        </p>
        <div className="mt-6 grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold">+${(earningsGap * 12).toLocaleString()}</div>
            <div className="text-sm opacity-80">Increased Earnings</div>
          </div>
          <div>
            <div className="text-2xl font-bold">-${(spendingOverage * 12).toLocaleString()}</div>
            <div className="text-sm opacity-80">Reduced Spending</div>
          </div>
          <div>
            <div className="text-2xl font-bold">{Math.round((annualSavingsPotential / currentEarnings / 12) * 100)}%</div>
            <div className="text-sm opacity-80">Income Increase</div>
          </div>
        </div>
      </div>
    </div>
  )
}
