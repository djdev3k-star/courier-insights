import { LucideIcon } from 'lucide-react'

interface GradientCardProps {
  title: string
  description: string
  icon?: LucideIcon
  onClick?: () => void
  badge?: {
    text: string
    variant: 'new' | 'important' | 'analysis'
  }
  gradient?: 'primary' | 'accent'
}

export function GradientCard({
  title,
  description,
  icon: Icon,
  onClick,
  badge,
}: GradientCardProps) {
  return (
    <div
      className="gradient-card"
      onClick={onClick}
    >
      {Icon && (
        <div className="mb-4 relative z-10">
          <Icon className="w-10 h-10" />
        </div>
      )}
      <h3 className="text-xl font-black mb-2 relative z-10 uppercase tracking-tight">{title}</h3>
      <p className="text-sm leading-relaxed font-bold relative z-10">{description}</p>
      {badge && (
        <span
          className={`badge mt-3 relative z-10 ${
            badge.variant === 'new'
              ? 'badge-new'
              : badge.variant === 'important'
              ? 'badge-important'
              : 'badge-analysis'
          }`}
        >
          {badge.text}
        </span>
      )}
    </div>
  )
}
