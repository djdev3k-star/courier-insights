import { LucideIcon } from 'lucide-react'

interface StatCardProps {
  title: string
  value: string | number
  label: string
  icon?: LucideIcon
  trend?: {
    value: number
    isPositive: boolean
  }
}

export function StatCard({ title, value, label, icon: Icon, trend }: StatCardProps) {
  return (
    <div className="stat-card">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-blue-600 text-xs uppercase tracking-wider font-black mb-2">
            {title}
          </h3>
          <div className="text-4xl font-black text-black mb-1">{value}</div>
          <p className="text-gray-700 text-sm font-bold">{label}</p>
        </div>
        {Icon && (
          <div className="bg-blue-600 p-3 border-3 border-black">
            <Icon className="w-6 h-6 text-white" />
          </div>
        )}
      </div>
      {trend && (
        <div className="mt-4 flex items-center space-x-1">
          <span
            className={`text-sm font-bold border-2 border-black px-2 py-1 ${
              trend.isPositive ? 'bg-green-400 text-black' : 'bg-red-500 text-white'
            }`}
          >
            {trend.isPositive ? '+' : '-'}{Math.abs(trend.value)}%
          </span>
          <span className="text-gray-700 text-sm font-bold">vs last month</span>
        </div>
      )}
    </div>
  )
}
