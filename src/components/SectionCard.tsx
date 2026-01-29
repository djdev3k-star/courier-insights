import { ReactNode } from 'react'

interface SectionCardProps {
  title: string
  subtitle?: string
  children: ReactNode
  action?: ReactNode
}

export function SectionCard({ title, subtitle, children, action }: SectionCardProps) {
  return (
    <div className="section-card">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h2 className="text-primary text-3xl font-bold">{title}</h2>
          {subtitle && <p className="text-gray-600 mt-2">{subtitle}</p>}
        </div>
        {action && <div>{action}</div>}
      </div>
      <div className="border-b-2 border-gray-100 mb-6" />
      {children}
    </div>
  )
}
