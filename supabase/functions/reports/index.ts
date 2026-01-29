import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.39.3";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

interface ReportData {
  trips: any[];
  expenses: any[];
}

// Generate LaTeX for itemized expenses
function generateItemizedExpensesLatex(expenses: any[]): string {
  const monthGroups = expenses.reduce((acc, exp) => {
    const month = new Date(exp.posted_date).toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
    if (!acc[month]) acc[month] = [];
    acc[month].push(exp);
    return acc;
  }, {} as Record<string, any[]>);

  const totalAmount = expenses.reduce((sum, e) => sum + Number(e.amount || 0), 0);

  let latex = `\\documentclass[11pt,letterpaper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage[margin=0.75in,landscape]{geometry}
\\usepackage{longtable}
\\usepackage{booktabs}
\\usepackage{xcolor}
\\usepackage{fancyhdr}

\\definecolor{titleblue}{RGB}{102,126,234}
\\definecolor{lightgray}{RGB}{240,240,240}

\\pagestyle{fancy}
\\fancyhf{}
\\fancyhead[L]{\\small\\textcolor{titleblue}{Itemized Expenses Report}}
\\fancyhead[R]{\\small\\thepage}
\\renewcommand{\\headrulewidth}{0.5pt}

\\title{\\textcolor{titleblue}{\\textbf{Itemized Expense Report}}}
\\author{JTech Logistics}
\\date{${new Date().toLocaleDateString()}}

\\begin{document}

\\maketitle

\\section*{Summary}
\\begin{itemize}
    \\item \\textbf{Total Spending:} \\$${totalAmount.toFixed(2)}
    \\item \\textbf{Total Transactions:} ${expenses.length}
    \\item \\textbf{Generated:} ${new Date().toLocaleDateString()}
\\end{itemize}

\\newpage

`;

  for (const [month, monthExpenses] of Object.entries(monthGroups)) {
    const monthTotal = monthExpenses.reduce((sum, e) => sum + Number(e.amount || 0), 0);

    latex += `\\section*{${month}}
\\textit{Total: \\$${monthTotal.toFixed(2)} (${monthExpenses.length} transactions)}

\\begin{longtable}{llr}
\\toprule
\\textbf{Date} & \\textbf{Description} & \\textbf{Amount} \\\\
\\midrule
\\endfirsthead
\\multicolumn{3}{c}{{\\tablename\\ \\thetable{} -- continued from previous page}} \\\\
\\toprule
\\textbf{Date} & \\textbf{Description} & \\textbf{Amount} \\\\
\\midrule
\\endhead
\\bottomrule
\\endfoot
\\bottomrule
\\endlastfoot

`;

    for (const exp of monthExpenses) {
      const dateStr = new Date(exp.posted_date).toLocaleDateString('en-US', { month: '2-digit', day: '2-digit' });
      const desc = String(exp.description || '').substring(0, 50)
        .replace(/&/g, '\\&')
        .replace(/_/g, '\\_')
        .replace(/#/g, '\\#');
      latex += `${dateStr} & ${desc} & \\$${Number(exp.amount || 0).toFixed(2)} \\\\\n`;
    }

    latex += `\\midrule
\\textbf{Month Total} & & \\textbf{\\$${monthTotal.toFixed(2)}} \\\\
\\end{longtable}
\\newpage

`;
  }

  latex += "\\end{document}";
  return latex;
}

// Generate LaTeX for master summary
function generateMasterSummaryLatex(data: ReportData): string {
  const totalTrips = data.trips.length;
  const totalExpenses = data.expenses.reduce((sum, e) => sum + Number(e.amount || 0), 0);
  const totalEarnings = data.trips.reduce((sum, t) => sum + Number(t.fare_amount || 0), 0);

  return `\\documentclass[11pt,letterpaper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage[margin=1in]{geometry}
\\usepackage{longtable}
\\usepackage{booktabs}
\\usepackage{xcolor}
\\usepackage{fancyhdr}

\\definecolor{titleblue}{RGB}{102,126,234}
\\definecolor{successgreen}{RGB}{76,175,80}

\\pagestyle{fancy}
\\fancyhf{}
\\fancyhead[L]{\\small\\textcolor{titleblue}{JTech Logistics - Financial Summary}}
\\fancyhead[R]{\\small\\thepage}
\\renewcommand{\\headrulewidth}{0.5pt}

\\title{\\textcolor{titleblue}{\\textbf{\\LARGE JTech Logistics}\\\\[0.3cm]\\Large Financial Reconciliation Report}}
\\author{}
\\date{Generated: ${new Date().toLocaleDateString()}}

\\begin{document}

\\maketitle

\\section*{Executive Summary}

This comprehensive financial reconciliation report provides complete analysis of trips, earnings, and expenses.

\\subsection*{Key Metrics}

\\begin{tabular}{ll}
\\toprule
\\textbf{Metric} & \\textbf{Value} \\\\
\\midrule
Total Trips & ${totalTrips} \\\\
Total Earnings & \\$${totalEarnings.toFixed(2)} \\\\
Total Expenses & \\$${totalExpenses.toFixed(2)} \\\\
Net Profit & \\$${(totalEarnings - totalExpenses).toFixed(2)} \\\\
Report Generated & ${new Date().toLocaleDateString()} \\\\
\\bottomrule
\\end{tabular}

\\vspace{1cm}

\\section*{Trip Analysis}

Total completed trips: ${totalTrips}

Average earnings per trip: \\$${(totalEarnings / totalTrips).toFixed(2)}

\\section*{Expense Analysis}

Total transactions: ${data.expenses.length}

Total amount: \\$${totalExpenses.toFixed(2)}

Average per transaction: \\$${(totalExpenses / data.expenses.length).toFixed(2)}

\\vspace{1cm}

\\centerline{\\textcolor{titleblue}{\\textbf{---  END OF SUMMARY  ---}}}

\\vspace{0.5cm}

\\centerline{\\textit{This is a master summary document. See individual reports for detailed analysis.}}

\\end{document}`;
}

// Generate comprehensive monthly report
function generateMonthlyReportLatex(data: ReportData): string {
  const monthGroups: Record<string, { trips: any[], expenses: any[] }> = {};

  data.trips.forEach(trip => {
    const month = new Date(trip.drop_off_time).toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
    if (!monthGroups[month]) monthGroups[month] = { trips: [], expenses: [] };
    monthGroups[month].trips.push(trip);
  });

  data.expenses.forEach(exp => {
    const month = new Date(exp.posted_date).toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
    if (!monthGroups[month]) monthGroups[month] = { trips: [], expenses: [] };
    monthGroups[month].expenses.push(exp);
  });

  let latex = `\\documentclass[11pt,letterpaper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage[margin=1in]{geometry}
\\usepackage{longtable}
\\usepackage{booktabs}
\\usepackage{xcolor}
\\usepackage{fancyhdr}

\\definecolor{titleblue}{RGB}{102,126,234}

\\pagestyle{fancy}
\\fancyhf{}
\\fancyhead[L]{\\small\\textcolor{titleblue}{Monthly Performance Report}}
\\fancyhead[R]{\\small\\thepage}
\\renewcommand{\\headrulewidth}{0.5pt}

\\title{\\textcolor{titleblue}{\\textbf{Monthly Performance Report}}}
\\author{JTech Logistics}
\\date{${new Date().toLocaleDateString()}}

\\begin{document}

\\maketitle

\\section*{Monthly Breakdown}

`;

  for (const [month, data] of Object.entries(monthGroups)) {
    const tripCount = data.trips.length;
    const monthEarnings = data.trips.reduce((sum, t) => sum + Number(t.fare_amount || 0), 0);
    const monthExpenses = data.expenses.reduce((sum, e) => sum + Number(e.amount || 0), 0);
    const netProfit = monthEarnings - monthExpenses;

    latex += `\\subsection*{${month}}

\\begin{tabular}{ll}
\\toprule
\\textbf{Metric} & \\textbf{Value} \\\\
\\midrule
Trips Completed & ${tripCount} \\\\
Total Earnings & \\$${monthEarnings.toFixed(2)} \\\\
Total Expenses & \\$${monthExpenses.toFixed(2)} \\\\
Net Profit & \\$${netProfit.toFixed(2)} \\\\
Avg per Trip & \\$${(monthEarnings / tripCount).toFixed(2)} \\\\
\\bottomrule
\\end{tabular}

\\vspace{0.5cm}

`;
  }

  latex += "\\end{document}";
  return latex;
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 200,
      headers: corsHeaders,
    });
  }

  try {
    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
    const supabaseKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
    const supabase = createClient(supabaseUrl, supabaseKey);

    const url = new URL(req.url);
    const path = url.pathname.split("/reports")[1] || "";

    // Get report type from query params or path
    const reportType = url.searchParams.get("type") || path.replace("/", "");

    // Fetch data from Supabase
    const { data: trips } = await supabase
      .from("trips")
      .select("*")
      .order("drop_off_time", { ascending: false });

    const { data: expenses } = await supabase
      .from("expenses")
      .select("*")
      .order("posted_date", { ascending: false });

    const reportData: ReportData = {
      trips: trips || [],
      expenses: expenses || [],
    };

    let latex = "";
    let filename = "report.tex";

    switch (reportType) {
      case "itemized-expenses":
        latex = generateItemizedExpensesLatex(reportData.expenses);
        filename = "itemized_expenses.tex";
        break;

      case "master-summary":
        latex = generateMasterSummaryLatex(reportData);
        filename = "master_summary.tex";
        break;

      case "monthly-report":
        latex = generateMonthlyReportLatex(reportData);
        filename = "monthly_report.tex";
        break;

      default:
        return new Response(
          JSON.stringify({
            error: "Invalid report type",
            available: ["itemized-expenses", "master-summary", "monthly-report"],
          }),
          {
            status: 400,
            headers: { ...corsHeaders, "Content-Type": "application/json" },
          }
        );
    }

    // Return LaTeX content
    return new Response(latex, {
      headers: {
        ...corsHeaders,
        "Content-Type": "application/x-latex",
        "Content-Disposition": `attachment; filename="${filename}"`,
      },
    });
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        status: 500,
        headers: {
          ...corsHeaders,
          "Content-Type": "application/json",
        },
      }
    );
  }
});
