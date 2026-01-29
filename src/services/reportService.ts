export type ReportType = 'master-summary' | 'business-expenses' | 'itemized-expenses' | 'monthly-report'

export interface ReportDefinition {
  id: ReportType
  title: string
  description: string
  filename: string
}

export const AVAILABLE_REPORTS: ReportDefinition[] = [
  {
    id: 'master-summary',
    title: 'Master Summary Report',
    description: 'Business profit analysis with expense classification',
    filename: 'master_summary.tex',
  },
  {
    id: 'business-expenses',
    title: 'Business Expenses Only',
    description: 'Tax-deductible business expenses (EV charging, fuel, phone)',
    filename: 'business_expenses.tex',
  },
  {
    id: 'itemized-expenses',
    title: 'Complete Expense Report',
    description: 'All expenses categorized: business, personal, customer purchases',
    filename: 'itemized_expenses.tex',
  },
  {
    id: 'monthly-report',
    title: 'Monthly Performance Report',
    description: 'Month-by-month breakdown of trips and earnings',
    filename: 'monthly_report.tex',
  },
]

export class ReportService {
  private supabaseUrl: string
  private supabaseAnonKey: string

  constructor() {
    this.supabaseUrl = import.meta.env.VITE_SUPABASE_URL
    this.supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

    if (!this.supabaseUrl || !this.supabaseAnonKey) {
      throw new Error('Supabase configuration is missing')
    }
  }

  async generateReport(reportType: ReportType): Promise<string> {
    const response = await fetch(
      `${this.supabaseUrl}/functions/v1/reports?type=${reportType}`,
      {
        headers: {
          'Authorization': `Bearer ${this.supabaseAnonKey}`,
          'Content-Type': 'application/json',
        },
      }
    )

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Unknown error' }))
      throw new Error(error.error || 'Failed to generate report')
    }

    return await response.text()
  }

  async downloadReport(reportType: ReportType): Promise<void> {
    const latex = await this.generateReport(reportType)
    const report = AVAILABLE_REPORTS.find((r) => r.id === reportType)
    const filename = report?.filename || `${reportType}.tex`

    const blob = new Blob([latex], { type: 'application/x-latex' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
  }

  getReportDefinition(reportType: ReportType): ReportDefinition | undefined {
    return AVAILABLE_REPORTS.find((r) => r.id === reportType)
  }

  getAllReportDefinitions(): ReportDefinition[] {
    return AVAILABLE_REPORTS
  }
}

export const reportService = new ReportService()
