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
          <h3 className="text-primary text-xs uppercase tracking-wider font-semibold mb-2">
            {title}
          </h3>
          <div className="text-4xl font-bold text-gray-900 mb-1">{value}</div>
          <p className="text-gray-500 text-sm">{label}</p>
        </div>
        {Icon && (
          <div className="bg-gradient-primary p-3 rounded-lg">
            <Icon className="w-6 h-6 text-white" />
          </div>
        )}
      </div>
      {trend && (
        <div className="mt-4 flex items-center space-x-1">
          <span
            className={`text-sm font-semibold ${
              trend.isPositive ? 'text-green-600' : 'text-red-600'
            }`}
          >
            {trend.isPositive ? '+' : '-'}{Math.abs(trend.value)}%
          </span>
          <span className="text-gray-500 text-sm">vs last month</span>
        </div>
      )}
    </div>
  )
}
