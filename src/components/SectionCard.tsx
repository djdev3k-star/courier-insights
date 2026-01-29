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
          <h2 className="text-blue-600 text-3xl font-black uppercase tracking-tight">{title}</h2>
          {subtitle && <p className="text-black mt-2 font-bold">{subtitle}</p>}
        </div>
        {action && <div>{action}</div>}
      </div>
      <div className="border-b-4 border-black mb-6" />
      {children}
    </div>
  )
}
