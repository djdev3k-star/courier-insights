import { FileText, TrendingUp, FileDown } from 'lucide-react'
import { SectionCard } from '@/components/SectionCard'
import { GradientCard } from '@/components/GradientCard'
import { Alert } from '@/components/Alert'
import { useState } from 'react'
import { reportService, type ReportType } from '@/services/reportService'

export function Reports() {
  const [isGenerating, setIsGenerating] = useState(false)
  const [generationStatus, setGenerationStatus] = useState<string | null>(null)

  const generateLatexReport = async (reportType: ReportType) => {
    setIsGenerating(true)
    const reportDef = reportService.getReportDefinition(reportType)
    const reportName = reportDef?.title || 'Report'

    setGenerationStatus(`Generating ${reportName}...`)

    try {
      await reportService.downloadReport(reportType)
      setGenerationStatus(`${reportName} downloaded successfully!`)
      setTimeout(() => setGenerationStatus(null), 3000)
    } catch (error) {
      setGenerationStatus(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`)
      setTimeout(() => setGenerationStatus(null), 5000)
    } finally {
      setIsGenerating(false)
    }
  }
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

  const latexReports = reportService.getAllReportDefinitions().map((report) => ({
    ...report,
    icon: report.id === 'monthly-report' ? TrendingUp : FileText,
  }))

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

      {generationStatus && (
        <Alert variant={generationStatus.startsWith('Error') ? 'error' : 'success'}>
          {generationStatus}
        </Alert>
      )}

      <SectionCard title="Generate LaTeX Documents">
        <div className="mb-4">
          <p className="text-gray-600 mb-4">
            Generate professional LaTeX documents for printing. Compile with pdflatex to create PDF reports.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {latexReports.map((report) => {
            const Icon = report.icon
            return (
              <div
                key={report.id}
                className="border-2 border-gray-200 rounded-xl p-6 hover:border-primary hover:shadow-lg transition-all"
              >
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-gradient-primary rounded-lg flex items-center justify-center flex-shrink-0">
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-bold text-lg mb-2">{report.title}</h3>
                    <p className="text-sm text-gray-600 mb-4">{report.description}</p>
                    <button
                      onClick={() => generateLatexReport(report.id as ReportType)}
                      disabled={isGenerating}
                      className="w-full bg-gradient-primary text-white px-4 py-2 rounded-lg font-semibold hover:opacity-90 transition-opacity disabled:opacity-50 flex items-center justify-center space-x-2"
                    >
                      <FileDown className="w-4 h-4" />
                      <span>{isGenerating ? 'Generating...' : 'Download .tex'}</span>
                    </button>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </SectionCard>

      <SectionCard title="Analysis Documentation">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {reports.map((report) => (
            <div key={report.title}>
              <GradientCard
                title={report.title}
                description={report.description}
                icon={FileText}
                badge={report.badge}
              />
            </div>
          ))}
        </div>
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">
            <strong>Note:</strong> Analysis documentation files are reference materials from the original Python analysis scripts.
            Use the LaTeX document generator above to create printable reports from your live database data.
          </p>
        </div>
      </SectionCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <SectionCard title="Data Summary">
          <div className="space-y-3">
            {[
              {
                name: 'Trip Data',
                desc: 'Complete trip history with pickups, dropoffs, and earnings',
                metric: 'Database: trips table',
              },
              {
                name: 'Expense Records',
                desc: 'All expenses tracked with categories and merchants',
                metric: 'Database: expenses table',
              },
              {
                name: 'Analytics Cache',
                desc: 'Pre-computed metrics and performance data',
                metric: 'Database: analytics_summary table',
              },
            ].map((item) => (
              <div
                key={item.name}
                className="p-4 border-2 border-gray-200 rounded-lg"
              >
                <div className="flex items-start space-x-3">
                  <div className="w-10 h-10 bg-gradient-primary rounded-lg flex items-center justify-center flex-shrink-0">
                    <FileText className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <div className="font-bold text-primary mb-1">{item.name}</div>
                    <div className="text-sm text-gray-600 mb-2">{item.desc}</div>
                    <div className="text-xs text-gray-500 font-mono">{item.metric}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="Report Features">
          <div className="space-y-3">
            {[
              {
                name: 'Professional LaTeX Output',
                desc: 'Industry-standard document format for printing',
              },
              {
                name: 'Real-Time Data',
                desc: 'Reports generated from live database records',
              },
              {
                name: 'Comprehensive Analysis',
                desc: 'Detailed breakdowns with summaries and totals',
              },
              {
                name: 'Multi-Format Support',
                desc: 'Generate various report types for different purposes',
              },
            ].map((item) => (
              <div
                key={item.name}
                className="flex items-start space-x-3 p-4 border-2 border-gray-200 rounded-lg"
              >
                <div className="w-2 h-2 bg-gradient-primary rounded-full mt-2 flex-shrink-0"></div>
                <div className="flex-1">
                  <div className="font-bold mb-1">{item.name}</div>
                  <div className="text-sm text-gray-600">{item.desc}</div>
                </div>
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
        <h2 className="text-3xl font-bold mb-4">Professional Report Generation</h2>
        <p className="text-lg opacity-90 mb-6 max-w-2xl mx-auto">
          Generate professional LaTeX documents ready for compilation to PDF. All reports pull live data from your Supabase database and format it into publication-ready documents.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-3xl mx-auto text-left">
          {[
            { title: 'LaTeX Format', desc: 'Industry-standard typesetting for professional documents' },
            { title: 'Auto-Generated', desc: 'No manual data entry - everything pulls from your database' },
            { title: 'Print Ready', desc: 'Compile with pdflatex to create high-quality PDF reports' },
          ].map((feature) => (
            <div key={feature.title} className="bg-white/10 backdrop-blur rounded-lg p-4">
              <div className="font-bold mb-2">{feature.title}</div>
              <div className="text-sm opacity-90">{feature.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
