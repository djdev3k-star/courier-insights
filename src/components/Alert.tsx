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
    error: 'alert-error text-red-900',
    warning: 'alert-warning text-yellow-900',
    success: 'alert-success text-green-900',
    info: 'bg-blue-100 border-blue-600 text-blue-900',
  }

  const Icon = icons[variant]

  return (
    <div className={`alert ${colors[variant]}`}>
      <div className="flex items-start space-x-3">
        <Icon className="w-6 h-6 mt-0.5 flex-shrink-0 font-bold" />
        <div className="flex-1">
          {title && <p className="font-black mb-1 uppercase">{title}</p>}
          <div className="text-sm font-bold">{children}</div>
        </div>
      </div>
    </div>
  )
}
