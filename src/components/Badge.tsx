interface BadgeProps {
  children: string
  variant?: 'new' | 'important' | 'analysis' | 'default'
}

export function Badge({ children, variant = 'default' }: BadgeProps) {
  const variants = {
    new: 'badge-new',
    important: 'badge-important',
    analysis: 'badge-analysis',
    default: 'bg-gray-200 text-gray-800',
  }

  return <span className={`badge ${variants[variant]}`}>{children}</span>
}
