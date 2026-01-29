import { Calendar as CalendarIcon, Clock, DollarSign } from 'lucide-react'
import { SectionCard } from '@/components/SectionCard'
import { StatCard } from '@/components/StatCard'
import { Alert } from '@/components/Alert'

export function Schedule() {
  const schedule = [
    { day: 'MONDAY', shift: '11am-1pm + 6pm-10pm', target: 150 },
    { day: 'TUESDAY', shift: '12pm-2pm + 6pm-10pm', target: 200, featured: true },
    { day: 'WEDNESDAY', shift: '11am-1pm + 5pm-7pm', target: 100 },
    { day: 'THURSDAY', shift: '6pm-11pm', target: 200, featured: true },
    { day: 'FRIDAY', shift: '6pm-11pm', target: 200, featured: true },
    { day: 'SATURDAY', shift: '11am-2pm + 5pm-10pm', target: 200, featured: true },
    { day: 'SUNDAY', shift: '12pm-2pm', target: 75 },
  ]

  const weeklyTotal = schedule.reduce((sum, day) => sum + day.target, 0)

  return (
    <div className="space-y-8">
      <header className="section-card">
        <h1 className="text-5xl font-black text-blue-600 mb-3 uppercase tracking-tight">Schedule Optimization</h1>
        <p className="text-xl text-black font-bold">
          Your personalized earnings optimization plan based on 1,077 actual trips
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Weekly Target"
          value={`$${weeklyTotal}`}
          label="From optimized schedule"
          icon={DollarSign}
        />
        <StatCard
          title="Monthly Goal"
          value="$3,050"
          label="26 work days"
          icon={CalendarIcon}
        />
        <StatCard
          title="Peak Hours"
          value="6-11 PM"
          label="55% of all trips"
          icon={Clock}
        />
      </div>

      <Alert variant="success" title="Data-Driven Schedule">
        This schedule is based on your actual historical data, not guesswork. It concentrates work
        during proven high-demand periods to maximize earnings while minimizing effort.
      </Alert>

      <SectionCard title="Your Optimized Weekly Schedule">
        <div className="space-y-4">
          {schedule.map((day) => (
            <div
              key={day.day}
              className={`p-6 border-4 transition-all duration-200 ${
                day.featured
                  ? 'border-black bg-blue-600 text-white'
                  : 'border-blue-600 hover:border-black bg-white'
              }`}
              style={day.featured ? { boxShadow: '8px 8px 0px 0px rgba(0, 0, 0, 1)' } : {}}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div
                    className={`w-16 h-16 flex items-center justify-center border-3 border-black ${
                      day.featured ? 'bg-white/20' : 'bg-blue-600'
                    }`}
                  >
                    <CalendarIcon
                      className={`w-8 h-8 ${day.featured ? 'text-white' : 'text-white'}`}
                    />
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <h3 className="text-xl font-black uppercase">{day.day}</h3>
                      {day.featured && (
                        <span className="px-2 py-1 bg-white text-blue-600 text-xs font-black border-2 border-black uppercase">
                          PRIORITY
                        </span>
                      )}
                    </div>
                    <p className={`mt-1 font-bold ${day.featured ? 'text-white' : 'text-gray-700'}`}>
                      {day.shift}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <div
                    className={`text-3xl font-black ${day.featured ? 'text-white' : 'text-blue-600'}`}
                  >
                    ${day.target}
                  </div>
                  <div className={`text-sm font-bold ${day.featured ? 'text-white' : 'text-gray-700'}`}>
                    target
                  </div>
                </div>
              </div>
            </div>
          ))}

          <div className="mt-6 p-6 bg-green-400 border-4 border-black" style={{ boxShadow: '8px 8px 0px 0px rgba(0, 0, 0, 1)' }}>
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm text-black font-black uppercase">
                  Weekly Total
                </div>
                <div className="text-black mt-1 font-bold">Estimated earnings potential</div>
              </div>
              <div className="text-4xl font-black text-black">${weeklyTotal}</div>
            </div>
          </div>
        </div>
      </SectionCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <SectionCard title="Why This Schedule Works">
          <div className="space-y-4">
            <div className="border-l-4 border-blue-600 pl-4">
              <h4 className="font-black text-blue-600 mb-2 uppercase">Evening Focus</h4>
              <p className="text-black font-bold">
                55% of trips occur 6 PM - 11 PM. Evening orders typically pay 30-50% more than
                lunch orders.
              </p>
            </div>
            <div className="border-l-4 border-blue-600 pl-4">
              <h4 className="font-black text-blue-600 mb-2 uppercase">Weekend Priority</h4>
              <p className="text-black font-bold">
                Saturday & Sunday have 2x the trip volume of Monday-Wednesday. Friday kicks off the
                weekend demand spike.
              </p>
            </div>
            <div className="border-l-4 border-blue-600 pl-4">
              <h4 className="font-black text-blue-600 mb-2 uppercase">Split Shifts</h4>
              <p className="text-black font-bold">
                Lunch (11 AM - 2 PM) provides supplementary income. Evening (6-11 PM) is your
                primary earning window. Rest between peaks.
              </p>
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Top 3 Revenue Zones">
          <div className="space-y-4">
            <p className="text-black font-bold">Focus 60% of your time in these high-volume zones:</p>
            <div className="space-y-3">
              {[
                { zone: 'TX 75206', trips: 91, revenue: '$1,123' },
                { zone: 'TX 75204', trips: 81, revenue: '$998' },
                { zone: 'TX 75219', trips: 74, revenue: '$912' },
              ].map((zone, index) => (
                <div
                  key={zone.zone}
                  className="flex items-center justify-between p-4 bg-blue-600 border-3 border-black text-white"
                >
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-white border-2 border-black flex items-center justify-center font-black text-blue-600">
                      {index + 1}
                    </div>
                    <div>
                      <div className="font-black">{zone.zone}</div>
                      <div className="text-sm font-bold">{zone.trips} trips</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-black">{zone.revenue}</div>
                    <div className="text-xs font-bold">estimated</div>
                  </div>
                </div>
              ))}
            </div>
            <Alert variant="info">
              Route clustering in one zone saves ~20% in dead mileage compared to jumping around the
              city.
            </Alert>
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Quick Start: Next 4 Weeks">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            {
              week: 'Week 1',
              title: 'Establish',
              tasks: [
                'Block calendar with schedule',
                'Set phone reminders',
                'Map top 3 zones on GPS',
                'Test split-shift approach',
              ],
            },
            {
              week: 'Week 2',
              title: 'Measure',
              tasks: [
                'Track actual vs. targets',
                'Calculate $/mile and $/hour',
                'Document what worked',
                'Stay in primary zones',
              ],
            },
            {
              week: 'Week 3',
              title: 'Optimize',
              tasks: [
                'Review Week 2 data',
                'Identify underperforming hours',
                'Test adjustments',
                'Prepare refinements',
              ],
            },
            {
              week: 'Week 4',
              title: 'Execute',
              tasks: [
                'Run final week analysis',
                'Calculate total earnings',
                'Compare to $3,050 target',
                'Plan Month 2 optimizations',
              ],
            },
          ].map((week) => (
            <div key={week.week} className="border-4 border-blue-600 p-6">
              <div className="text-blue-600 font-black mb-2 uppercase">{week.week}</div>
              <h3 className="text-xl font-black mb-4 uppercase">{week.title}</h3>
              <ul className="space-y-2 text-sm text-black">
                {week.tasks.map((task, i) => (
                  <li key={i} className="flex items-start">
                    <span className="text-blue-600 mr-2 font-bold">✓</span>
                    <span className="font-bold">{task}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  )
}
