import { FileText, Download, ExternalLink, TrendingUp } from 'lucide-react'
import { SectionCard } from '@/components/SectionCard'
import { GradientCard } from '@/components/GradientCard'
import { Alert } from '@/components/Alert'

export function Reports() {
  const reports = [
    {
      title: 'Phase 9: Corrected Data Model',
      description:
        'All calculation errors fixed. Actual earnings: $1,985/mo. Actual spending: $1,667/mo.',
      category: 'Critical',
      badge: { text: 'NEW - START HERE', variant: 'important' as const },
      file: 'QUICK_REFERENCE_PHASE9.md',
    },
    {
      title: 'Complete Spending Breakdown',
      description:
        'Cross-reference analysis reveals all $8,334 spending: $4,565 customer purchases + $241 EV + $3,528 personal.',
      category: 'Financial',
      badge: { text: 'BREAKTHROUGH', variant: 'important' as const },
      file: 'SPENDING_BREAKDOWN_SUMMARY.md',
    },
    {
      title: 'Schedule Optimization Plan',
      description:
        'Optimal work schedule targeting $3,050/month with minimal effort. Peak hours: 6-11 PM.',
      category: 'Strategy',
      badge: { text: 'RECOMMENDED', variant: 'new' as const },
      file: 'docs/SCHEDULE_OPTIMIZATION_PLAN.md',
    },
    {
      title: 'Actual vs Recommended Performance',
      description:
        'Performance analysis comparing your behavior against optimal recommendations. Grade: F (33.3%)',
      category: 'Analysis',
      badge: { text: 'NEEDS UPDATE', variant: 'analysis' as const },
      file: 'docs/ACTUAL_VS_RECOMMENDED_REPORT.md',
    },
    {
      title: 'Spending Correlation Analysis',
      description:
        'Analysis of spending patterns during restaurant pickups. Save $470/month with meal prep.',
      category: 'Financial',
      badge: { text: 'KEY INSIGHTS', variant: 'new' as const },
      file: 'docs/SCHEDULE_SPENDING_CORRELATION_REPORT.md',
    },
    {
      title: 'Merchant Analysis Report',
      description:
        'Deep dive into $3,982 uncategorized spending. 72% occurs at pickup locations.',
      category: 'Analysis',
      badge: { text: 'DETAILED', variant: 'analysis' as const },
      file: 'docs/UNCATEGORIZED_MERCHANT_ANALYSIS_REPORT.md',
    },
  ]

  return (
    <div className="space-y-8">
      <header className="section-card">
        <h1 className="text-5xl font-bold text-primary mb-3">Reports & Documentation</h1>
        <p className="text-xl text-gray-600">
          Comprehensive analysis reports and business insights
        </p>
      </header>

      <Alert variant="info">
        All reports are generated from your actual trip and expense data. Download or view any report
        to get detailed insights and recommendations.
      </Alert>

      <SectionCard title="Featured Reports">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {reports.map((report) => (
            <div key={report.title}>
              <GradientCard
                title={report.title}
                description={report.description}
                icon={FileText}
                badge={report.badge}
                onClick={() => window.open(report.file, '_blank')}
              />
            </div>
          ))}
        </div>
      </SectionCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <SectionCard title="Quick Reference Guides">
          <div className="space-y-3">
            {[
              {
                name: 'Schedule Quick Reference',
                desc: 'One-page summary of optimal schedule, top zones, and peak hours',
                file: 'docs/SCHEDULE_QUICK_REFERENCE.md',
              },
              {
                name: 'Expense Quick Summary',
                desc: 'Fast breakdown of spending by category',
                file: 'docs/EXPENSE_QUICK_SUMMARY.md',
              },
              {
                name: 'Quick Start Guide',
                desc: 'Get started with the analytics system',
                file: 'docs/QUICK_START.md',
              },
            ].map((guide) => (
              <button
                key={guide.name}
                onClick={() => window.open(guide.file, '_blank')}
                className="w-full p-4 border-2 border-gray-200 rounded-lg hover:border-primary hover:bg-primary/5 transition-all text-left"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="font-bold text-primary mb-1">{guide.name}</div>
                    <div className="text-sm text-gray-600">{guide.desc}</div>
                  </div>
                  <ExternalLink className="w-5 h-5 text-gray-400 flex-shrink-0 ml-2" />
                </div>
              </button>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="Data & Analysis Files">
          <div className="space-y-3">
            {[
              { name: 'Trip Data (CSV)', size: '1,077 records', file: 'data/consolidated/trips/' },
              { name: 'Bank Statements', size: '2,294 transactions', file: 'bank/' },
              { name: 'Analysis Reports', size: '12+ reports', file: 'reports/' },
              {
                name: 'Python Analysis Scripts',
                size: '40+ scripts',
                file: 'scripts/',
              },
            ].map((item) => (
              <div
                key={item.name}
                className="flex items-center justify-between p-4 border-2 border-gray-200 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-primary rounded-lg flex items-center justify-center">
                    <FileText className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <div className="font-bold">{item.name}</div>
                    <div className="text-sm text-gray-600">{item.size}</div>
                  </div>
                </div>
                <button
                  onClick={() => window.open(item.file, '_blank')}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <Download className="w-5 h-5 text-primary" />
                </button>
              </div>
            ))}
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Report Categories">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { name: 'Earnings Reports', count: 8, icon: TrendingUp },
            { name: 'Expense Reports', count: 12, icon: FileText },
            { name: 'Schedule Analysis', count: 6, icon: FileText },
            { name: 'Performance Reviews', count: 4, icon: TrendingUp },
          ].map((cat) => {
            const Icon = cat.icon
            return (
              <div key={cat.name} className="p-6 border-2 border-primary rounded-xl text-center">
                <div className="w-12 h-12 bg-gradient-primary rounded-lg flex items-center justify-center mx-auto mb-3">
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <div className="font-bold text-lg">{cat.name}</div>
                <div className="text-2xl font-bold text-primary mt-2">{cat.count}</div>
                <div className="text-sm text-gray-600 mt-1">reports available</div>
              </div>
            )
          })}
        </div>
      </SectionCard>

      <div className="p-8 bg-gradient-primary rounded-2xl text-white text-center">
        <FileText className="w-16 h-16 mx-auto mb-4" />
        <h2 className="text-3xl font-bold mb-4">Need a Custom Report?</h2>
        <p className="text-lg opacity-90 mb-6">
          Use the Python analysis scripts to generate custom reports based on your specific needs
        </p>
        <button
          onClick={() => window.open('scripts/', '_blank')}
          className="bg-white text-primary px-8 py-3 rounded-lg font-bold hover:bg-gray-100 transition-colors inline-flex items-center space-x-2"
        >
          <span>View Analysis Scripts</span>
          <ExternalLink className="w-5 h-5" />
        </button>
      </div>
    </div>
  )
}
