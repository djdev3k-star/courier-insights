import { ReactNode } from 'react'
import { AlertCircle, CheckCircle, AlertTriangle, Info } from 'lucide-react'

interface AlertProps {
  children: ReactNode
  variant?: 'error' | 'warning' | 'success' | 'info'
  title?: string
}

export function Alert({ children, variant = 'info', title }: AlertProps) {
  const icons = {
    error: AlertCircle,
    warning: AlertTriangle,
    success: CheckCircle,
    info: Info,
  }

  const colors = {
    error: 'alert-error text-red-800',
    warning: 'alert-warning text-yellow-800',
    success: 'alert-success text-green-800',
    info: 'bg-blue-50 border-blue-500 text-blue-800',
  }

  const Icon = icons[variant]

  return (
    <div className={`alert ${colors[variant]}`}>
      <div className="flex items-start space-x-3">
        <Icon className="w-5 h-5 mt-0.5 flex-shrink-0" />
        <div className="flex-1">
          {title && <p className="font-bold mb-1">{title}</p>}
          <div className="text-sm">{children}</div>
        </div>
      </div>
    </div>
  )
}
