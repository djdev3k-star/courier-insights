"""
Generate Expense Reports as LaTeX/PDF
Converts itemized expenses and merchant summaries to professional LaTeX documents
"""

import pandas as pd
from pathlib import Path
from datetime import datetime


def generate_itemized_expense_latex():
    """Generate LaTeX for itemized expense report"""
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    expenses_file = base_path / 'reports' / 'itemized_expenses_by_month.csv'
    
    df = pd.read_csv(expenses_file)
    df['Posted Date'] = pd.to_datetime(df['Posted Date'])
    df['Month'] = pd.to_datetime(df['Month'])
    
    latex_content = []
    
    # Preamble
    latex_content.append(r'''\documentclass[11pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=0.75in,landscape]{geometry}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage[table]{xcolor}

\definecolor{titleblue}{RGB}{102,126,234}
\definecolor{lightgray}{RGB}{240,240,240}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textcolor{titleblue}{Itemized Expenses by Month}}
\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.5pt}

\title{\textcolor{titleblue}{\textbf{Itemized Expense Report}}}
\author{JTech Logistics}
\date{August - December 2025}

\begin{document}

\maketitle

\section*{Summary}
\begin{itemize}
    \item \textbf{Total Spending:} \$8,334.61
    \item \textbf{Total Transactions:} 394
    \item \textbf{Period:} September 2025 - December 2025
    \item \textbf{Unique Merchants:} 198
\end{itemize}

\newpage

''')
    
    # Generate tables by month
    for month in sorted(df['Month'].unique()):
        month_data = df[df['Month'] == month].sort_values('Posted Date')
        month_str = month.strftime('%B %Y')
        month_total = month_data['Amount'].sum()
        
        latex_content.append(f"\\section*{{{month_str}}}")
        latex_content.append(f"\\textit{{Total: \\${month_total:,.2f} ({len(month_data)} transactions)}}\n")
        latex_content.append("\\begin{longtable}{llr}")
        latex_content.append("\\toprule")
        latex_content.append("\\textbf{Date} & \\textbf{Description} & \\textbf{Amount} \\\\")
        latex_content.append("\\midrule")
        latex_content.append("\\endfirsthead")
        latex_content.append("\\multicolumn{3}{c}{{\\tablename\\ \\thetable{} -- continued from previous page}} \\\\")
        latex_content.append("\\toprule")
        latex_content.append("\\textbf{Date} & \\textbf{Description} & \\textbf{Amount} \\\\")
        latex_content.append("\\midrule")
        latex_content.append("\\endhead")
        latex_content.append("\\bottomrule")
        latex_content.append("\\endfoot")
        latex_content.append("\\bottomrule")
        latex_content.append("\\endlastfoot")
        
        for _, row in month_data.iterrows():
            date_str = row['Posted Date'].strftime('%m/%d')
            desc = str(row['Description']).replace('&', '\\&').replace('_', '\\_').replace('#', '\\#')
            if len(desc) > 50:
                desc = desc[:47] + '...'
            amount = f"\\${row['Amount']:,.2f}"
            latex_content.append(f"{date_str} & {desc} & {amount} \\\\")
        
        latex_content.append("\\midrule")
        latex_content.append(f"\\textbf{{Month Total}} & & \\textbf{{\\${month_total:,.2f}}} \\\\")
        latex_content.append("\\end{longtable}")
        latex_content.append("\\newpage\n")
    
    latex_content.append("\\end{document}")
    
    # Write to file
    output_file = base_path / 'reports' / 'latex' / 'itemized_expenses.tex'
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_content))
    
    print(f"✓ Generated: {output_file}")
    return output_file


def generate_merchant_summary_latex():
    """Generate LaTeX for merchant summary report"""
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    merchant_file = base_path / 'reports' / 'merchant_summary_by_month.csv'
    
    df = pd.read_csv(merchant_file)
    
    latex_content = []
    
    # Preamble
    latex_content.append(r'''\documentclass[11pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=1in]{geometry}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{fancyhdr}

\definecolor{titleblue}{RGB}{102,126,234}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textcolor{titleblue}{Merchant Summary by Month}}
\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.5pt}

\title{\textcolor{titleblue}{\textbf{Merchant Summary Report}}}
\author{JTech Logistics}
\date{September - December 2025}

\begin{document}

\maketitle

\section*{Accounting Summary}
\begin{itemize}
    \item \textbf{Total Spending:} \$8,334.61
    \item \textbf{Total Transactions:} 394
    \item \textbf{Unique Merchants:} 198
    \item \textbf{Average Transaction:} \$21.15
    \item \textbf{Average per Merchant:} \$42.09
\end{itemize}

\newpage

''')
    
    # Generate tables by month
    for month in sorted(df['Month'].unique()):
        month_data = df[df['Month'] == month].sort_values('Total', ascending=False)
        
        latex_content.append(f"\\section*{{{month}}}")
        latex_content.append(f"\\textit{{{len(month_data)} unique merchants}}\n")
        latex_content.append("\\begin{longtable}{lrr}")
        latex_content.append("\\toprule")
        latex_content.append("\\textbf{Merchant} & \\textbf{Visits} & \\textbf{Total} \\\\")
        latex_content.append("\\midrule")
        latex_content.append("\\endfirsthead")
        latex_content.append("\\multicolumn{3}{c}{{\\tablename\\ \\thetable{} -- continued from previous page}} \\\\")
        latex_content.append("\\toprule")
        latex_content.append("\\textbf{Merchant} & \\textbf{Visits} & \\textbf{Total} \\\\")
        latex_content.append("\\midrule")
        latex_content.append("\\endhead")
        latex_content.append("\\bottomrule")
        latex_content.append("\\endfoot")
        latex_content.append("\\bottomrule")
        latex_content.append("\\endlastfoot")
        
        for _, row in month_data.head(50).iterrows():  # Top 50 per month
            merchant = str(row['Merchant']).replace('&', '\\&').replace('_', '\\_').replace('#', '\\#')
            if len(merchant) > 55:
                merchant = merchant[:52] + '...'
            visits = int(row['Transactions'])
            total = row['Total']
            
            latex_content.append(f"{merchant} & {visits}x & \\${total:,.2f} \\\\")
        
        latex_content.append("\\end{longtable}")
        latex_content.append("\\newpage\n")
    
    # Top merchants overall
    overall = df.groupby('Merchant').agg({'Transactions': 'sum', 'Total': 'sum'}).reset_index()
    overall = overall.sort_values('Transactions', ascending=False).head(30)
    
    latex_content.append("\\section*{Most Visited Merchants (All Months)}")
    latex_content.append("\\begin{longtable}{lrr}")
    latex_content.append("\\toprule")
    latex_content.append("\\textbf{Merchant} & \\textbf{Total Visits} & \\textbf{Total Spent} \\\\")
    latex_content.append("\\midrule")
    
    for _, row in overall.iterrows():
        merchant = str(row['Merchant']).replace('&', '\\&').replace('_', '\\_').replace('#', '\\#')
        if len(merchant) > 55:
            merchant = merchant[:52] + '...'
        visits = int(row['Transactions'])
        total = row['Total']
        latex_content.append(f"{merchant} & {visits}x & \\${total:,.2f} \\\\")
    
    latex_content.append("\\bottomrule")
    latex_content.append("\\end{longtable}")
    latex_content.append("\\end{document}")
    
    # Write to file
    output_file = base_path / 'reports' / 'latex' / 'merchant_summary.tex'
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_content))
    
    print(f"✓ Generated: {output_file}")
    return output_file


def generate_merchant_monthly_dates_latex():
    """Generate LaTeX for merchant monthly activity with dates"""
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    merchant_file = base_path / 'reports' / 'merchant_by_month_with_dates.csv'
    
    df = pd.read_csv(merchant_file)
    
    latex_content = []
    
    # Preamble
    latex_content.append(r'''\documentclass[11pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=0.75in,landscape]{geometry}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{fancyhdr}

\definecolor{titleblue}{RGB}{102,126,234}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textcolor{titleblue}{Merchant Activity by Month}}
\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.5pt}

\title{\textcolor{titleblue}{\textbf{Merchant Activity Report by Month}}}
\author{JTech Logistics}
\date{September - December 2025}

\begin{document}

\maketitle

\section*{Summary}
\begin{itemize}
    \item \textbf{Total Spending:} \$8,334.61
    \item \textbf{Total Transactions:} 394
    \item \textbf{Unique Merchants:} 198
    \item \textbf{Months Covered:} 4 (September - December 2025)
\end{itemize}

\newpage

''')
    
    # Generate tables by month
    for month in sorted(df['Month'].unique()):
        month_data = df[df['Month'] == month].sort_values('Total_Spent', ascending=False)
        month_total = month_data['Total_Spent'].sum()
        
        latex_content.append(f"\\section*{{{month}}}")
        latex_content.append(f"\\textit{{Total: \\${month_total:,.2f} ({len(month_data)} merchants, {month_data['Transactions'].sum()} transactions)}}\n")
        latex_content.append("\\begin{longtable}{llrr}")
        latex_content.append("\\toprule")
        latex_content.append("\\textbf{Merchant} & \\textbf{Latest Date} & \\textbf{Visits} & \\textbf{Total} \\\\")
        latex_content.append("\\midrule")
        latex_content.append("\\endfirsthead")
        latex_content.append("\\multicolumn{4}{c}{{\\tablename\\ \\thetable{} -- continued from previous page}} \\\\")
        latex_content.append("\\toprule")
        latex_content.append("\\textbf{Merchant} & \\textbf{Latest Date} & \\textbf{Visits} & \\textbf{Total} \\\\")
        latex_content.append("\\midrule")
        latex_content.append("\\endhead")
        latex_content.append("\\bottomrule")
        latex_content.append("\\endfoot")
        latex_content.append("\\bottomrule")
        latex_content.append("\\endlastfoot")
        
        for _, row in month_data.iterrows():
            merchant = str(row['Merchant']).replace('&', '\\&').replace('_', '\\_').replace('#', '\\#')
            if len(merchant) > 45:
                merchant = merchant[:42] + '...'
            latest_date = str(row['Latest_Charge_Date'])
            visits = int(row['Transactions'])
            total = row['Total_Spent']
            
            latex_content.append(f"{merchant} & {latest_date} & {visits}x & \\${total:,.2f} \\\\")
        
        latex_content.append("\\midrule")
        latex_content.append(f"\\textbf{{Month Total}} & & & \\textbf{{\\${month_total:,.2f}}} \\\\")
        latex_content.append("\\end{longtable}")
        latex_content.append("\\newpage\n")
    
    latex_content.append("\\end{document}")
    
    # Write to file
    output_file = base_path / 'reports' / 'latex' / 'merchant_monthly_dates.tex'
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_content))
    
    print(f"✓ Generated: {output_file}")
    return output_file


def generate_categorized_spending_latex():
    """Generate LaTeX for categorized spending report"""
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    category_file = base_path / 'reports' / 'spending_by_category.csv'
    personal_file = base_path / 'reports' / 'personal_spending_by_merchant.csv'
    
    category_df = pd.read_csv(category_file)
    personal_df = pd.read_csv(personal_file)
    
    latex_content = []
    
    # Preamble
    latex_content.append(r'''\documentclass[11pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=1in]{geometry}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{fancyhdr}

\definecolor{titleblue}{RGB}{102,126,234}
\definecolor{businessgreen}{RGB}{46,125,50}
\definecolor{personalblue}{RGB}{25,118,210}
\definecolor{financialgray}{RGB}{117,117,117}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textcolor{titleblue}{Categorized Spending Analysis}}
\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.5pt}

\title{\textcolor{titleblue}{\textbf{Personal Spending Analysis}}}
\author{JTech Logistics}
\date{September - December 2025}

\begin{document}

\maketitle

\section*{Executive Summary}

Total bank spending of \$8,334.61 has been categorized into three primary groups:

\begin{itemize}
    \item \textcolor{businessgreen}{\textbf{Business Expenses:}} \$2,140.82 (25.7\%)
    \begin{itemize}
        \item EV Charging for delivery operations
        \item Customer purchases (reimbursed from Uber)
    \end{itemize}
    \item \textcolor{personalblue}{\textbf{Personal Expenses:}} \$2,907.44 (34.9\%)
    \begin{itemize}
        \item Food, groceries, shopping, and personal services
    \end{itemize}
    \item \textcolor{financialgray}{\textbf{Financial Transfers:}} \$3,286.35 (39.4\%)
    \begin{itemize}
        \item Credit card payments, ACH transfers, ATM fees
    \end{itemize}
\end{itemize}

\newpage

\section*{Spending by Category}

''')
    
    # Calculate totals
    business_total = category_df[category_df['Category'].str.contains('Business', case=False)]['Total'].sum()
    personal_total = category_df[~category_df['Category'].str.contains('Business|Financial', case=False)]['Total'].sum()
    financial_total = category_df[category_df['Category'].str.contains('Financial', case=False)]['Total'].sum()
    
    # Category table
    latex_content.append("\\begin{longtable}{lrr}")
    latex_content.append("\\toprule")
    latex_content.append("\\textbf{Category} & \\textbf{Transactions} & \\textbf{Total} \\\\")
    latex_content.append("\\midrule")
    
    for _, row in category_df.iterrows():
        category = str(row['Category']).replace('&', '\\&').replace('_', '\\_')
        txns = int(row['Transactions'])
        total = row['Total']
        latex_content.append(f"{category} & {txns} & \\${total:,.2f} \\\\")
    
    latex_content.append("\\midrule")
    latex_content.append(f"\\textcolor{{businessgreen}}{{\\textbf{{Business Total}}}} & & \\textbf{{\\${business_total:,.2f}}} \\\\")
    latex_content.append(f"\\textcolor{{personalblue}}{{\\textbf{{Personal Total}}}} & & \\textbf{{\\${personal_total:,.2f}}} \\\\")
    latex_content.append(f"\\textcolor{{financialgray}}{{\\textbf{{Financial Total}}}} & & \\textbf{{\\${financial_total:,.2f}}} \\\\")
    latex_content.append("\\midrule")
    latex_content.append(f"\\textbf{{Grand Total}} & & \\textbf{{\\${category_df['Total'].sum():,.2f}}} \\\\")
    latex_content.append("\\bottomrule")
    latex_content.append("\\end{longtable}")
    
    # Personal spending breakdown
    latex_content.append("\n\\newpage\n")
    latex_content.append("\\section*{Personal Spending by Merchant}")
    latex_content.append("\\textit{Top 50 merchants ranked by total spending}\n")
    
    latex_content.append("\\begin{longtable}{lrr}")
    latex_content.append("\\toprule")
    latex_content.append("\\textbf{Merchant} & \\textbf{Category} & \\textbf{Total} \\\\")
    latex_content.append("\\midrule")
    latex_content.append("\\endfirsthead")
    latex_content.append("\\multicolumn{3}{c}{{\\tablename\\ \\thetable{} -- continued from previous page}} \\\\")
    latex_content.append("\\toprule")
    latex_content.append("\\textbf{Merchant} & \\textbf{Category} & \\textbf{Total} \\\\")
    latex_content.append("\\midrule")
    latex_content.append("\\endhead")
    latex_content.append("\\bottomrule")
    latex_content.append("\\endfoot")
    latex_content.append("\\bottomrule")
    latex_content.append("\\endlastfoot")
    
    for _, row in personal_df.head(50).iterrows():
        merchant = str(row['Description']).replace('&', '\\&').replace('_', '\\_').replace('#', '\\#')
        if len(merchant) > 42:
            merchant = merchant[:39] + '...'
        category = str(row['Category']).replace('Personal - ', '')[:20]
        total = row['Amount']
        latex_content.append(f"{merchant} & {category} & \\${total:,.2f} \\\\")
    
    latex_content.append("\\end{longtable}")
    latex_content.append("\\end{document}")
    
    # Write to file
    output_file = base_path / 'reports' / 'latex' / 'categorized_spending.tex'
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_content))
    
    print(f"✓ Generated: {output_file}")
    return output_file


def generate_category_by_month_latex():
    """Generate LaTeX for category spending by month"""
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    monthly_file = base_path / 'reports' / 'category_spending_by_month.csv'
    
    df = pd.read_csv(monthly_file)
    
    latex_content = []
    
    # Preamble
    latex_content.append(r'''\documentclass[11pt,letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=1in]{geometry}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{fancyhdr}

\definecolor{titleblue}{RGB}{102,126,234}
\definecolor{businessgreen}{RGB}{46,125,50}
\definecolor{personalblue}{RGB}{25,118,210}
\definecolor{financialgray}{RGB}{117,117,117}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textcolor{titleblue}{Category Spending by Month}}
\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.5pt}

\title{\textcolor{titleblue}{\textbf{Category Spending Analysis by Month}}}
\author{JTech Logistics}
\date{September - December 2025}

\begin{document}

\maketitle

\section*{Overview}

This report shows spending trends across categories month-by-month, allowing you to track changes in business expenses, personal spending, and financial transfers over time.

\newpage

''')
    
    # Generate tables by month
    for month in sorted(df['Month'].unique()):
        month_data = df[df['Month'] == month].sort_values('Total', ascending=False)
        month_total = month_data['Total'].sum()
        
        month_label = pd.to_datetime(month).strftime('%B %Y')
        
        latex_content.append(f"\\section*{{{month_label}}}")
        latex_content.append(f"\\textit{{Total: \\${month_total:,.2f} ({month_data['Transactions'].sum()} transactions)}}\n")
        latex_content.append("\\begin{longtable}{lrr}")
        latex_content.append("\\toprule")
        latex_content.append("\\textbf{Category} & \\textbf{Transactions} & \\textbf{Total} \\\\")
        latex_content.append("\\midrule")
        
        for _, row in month_data.iterrows():
            category = str(row['Category']).replace('&', '\\&').replace('_', '\\_')
            txns = int(row['Transactions'])
            total = row['Total']
            
            # Color code by category type
            if 'Business' in category:
                latex_content.append(f"\\textcolor{{businessgreen}}{{{category}}} & {txns} & \\${total:,.2f} \\\\")
            elif 'Financial' in category:
                latex_content.append(f"\\textcolor{{financialgray}}{{{category}}} & {txns} & \\${total:,.2f} \\\\")
            else:
                latex_content.append(f"\\textcolor{{personalblue}}{{{category}}} & {txns} & \\${total:,.2f} \\\\")
        
        latex_content.append("\\midrule")
        latex_content.append(f"\\textbf{{Month Total}} & {month_data['Transactions'].sum()} & \\textbf{{\\${month_total:,.2f}}} \\\\")
        latex_content.append("\\bottomrule")
        latex_content.append("\\end{longtable}")
        latex_content.append("\\vspace{0.5cm}\n")
    
    # Category totals
    latex_content.append("\\newpage")
    latex_content.append("\\section*{Category Totals (All Months)}")
    
    category_totals = df.groupby('Category').agg({
        'Transactions': 'sum',
        'Total': 'sum'
    }).reset_index().sort_values('Total', ascending=False)
    
    latex_content.append("\\begin{longtable}{lrr}")
    latex_content.append("\\toprule")
    latex_content.append("\\textbf{Category} & \\textbf{Total Transactions} & \\textbf{Total} \\\\")
    latex_content.append("\\midrule")
    
    for _, row in category_totals.iterrows():
        category = str(row['Category']).replace('&', '\\&').replace('_', '\\_')
        txns = int(row['Transactions'])
        total = row['Total']
        
        if 'Business' in category:
            latex_content.append(f"\\textcolor{{businessgreen}}{{{category}}} & {txns} & \\${total:,.2f} \\\\")
        elif 'Financial' in category:
            latex_content.append(f"\\textcolor{{financialgray}}{{{category}}} & {txns} & \\${total:,.2f} \\\\")
        else:
            latex_content.append(f"\\textcolor{{personalblue}}{{{category}}} & {txns} & \\${total:,.2f} \\\\")
    
    latex_content.append("\\midrule")
    latex_content.append(f"\\textbf{{Grand Total}} & {df['Transactions'].sum()} & \\textbf{{\\${df['Total'].sum():,.2f}}} \\\\")
    latex_content.append("\\bottomrule")
    latex_content.append("\\end{longtable}")
    latex_content.append("\\end{document}")
    
    # Write to file
    output_file = base_path / 'reports' / 'latex' / 'category_by_month.tex'
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_content))
    
    print(f"✓ Generated: {output_file}")
    return output_file


def generate_reimbursement_summary_latex():
    """Generate summary reimbursement reconciliation (calls external script)"""
    import subprocess
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    
    # Run the reimbursement reconciliation script first
    print("Running reimbursement reconciliation...")
    result = subprocess.run(['python', 'reimbursement_reconciliation.py'], 
                          cwd=base_path, capture_output=True, text=True)
    
    # Then generate the LaTeX
    result = subprocess.run(['python', 'generate_reimbursement_latex.py'],
                          cwd=base_path, capture_output=True, text=True)
    
    output_file = base_path / 'reports' / 'latex' / 'reimbursement_reconciliation.tex'
    
    if output_file.exists():
        print(f"✓ Generated: {output_file}")
        return output_file
    else:
        print("⚠ Failed to generate reimbursement report")
        return None


def generate_master_summary():
    """Generate master summary report"""
    import subprocess
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    
    # Run master summary generation
    print("Generating master summary...")
    result = subprocess.run(['python', 'generate_master_summary.py'],
                          cwd=base_path, capture_output=True, text=True)
    
    output_file = base_path / 'reports' / 'latex' / 'master_summary.tex'
    
    if output_file.exists():
        print(f"✓ Generated: {output_file}")
        return output_file
    else:
        print("⚠ Failed to generate master summary")
        return None


def compile_all_expense_pdfs():
    """Generate all expense LaTeX files and compile to PDF"""
    import subprocess
    
    print("="*80)
    print("GENERATING EXPENSE REPORTS FOR LATEX/PDF")
    print("="*80)
    print()
    
    # Generate LaTeX files
    tex_files = []
    
    # Master summary first (overview)
    master_file = generate_master_summary()
    if master_file:
        tex_files.append(master_file)
    
    # Then detailed reports
    tex_files.append(generate_itemized_expense_latex())
    tex_files.append(generate_merchant_summary_latex())
    tex_files.append(generate_merchant_monthly_dates_latex())
    tex_files.append(generate_categorized_spending_latex())
    tex_files.append(generate_category_by_month_latex())
    
    # Generate reimbursement reconciliation
    reimb_file = generate_reimbursement_summary_latex()
    if reimb_file:
        tex_files.append(reimb_file)
    
    print()
    print("="*80)
    print("COMPILING TO PDF (requires pdflatex)")
    print("="*80)
    print()
    
    for tex_file in tex_files:
        print(f"Compiling {tex_file.name}...")
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', str(tex_file)],
                cwd=tex_file.parent,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                pdf_file = tex_file.with_suffix('.pdf')
                print(f"  ✓ Created: {pdf_file}")
            else:
                print(f"  ✗ Error compiling (check if pdflatex is installed)")
        except FileNotFoundError:
            print(f"  ⚠ pdflatex not found - LaTeX file created, compile manually")
    
    print()
    print("="*80)
    print("COMPLETE")
    print("="*80)
    print(f"\nLaTeX files: {tex_files[0].parent}")
    print("\nGenerated PDFs:")
    if len(tex_files) > 0:
        print(f"  1. master_summary.pdf - START HERE (overview of all reports)")
        print(f"  2. itemized_expenses.pdf - All 394 transactions")
        print(f"  3. merchant_summary.pdf - 198 merchants ranked")
        print(f"  4. merchant_monthly_dates.pdf - Latest activity")
        print(f"  5. categorized_spending.pdf - Business vs personal")
        print(f"  6. category_by_month.pdf - Monthly trends")
        print(f"  7. reimbursement_reconciliation.pdf - Full reconciliation")
    
    print("\nTo compile manually:")
    print(f"  cd {tex_files[0].parent if tex_files else 'reports/latex'}")
    print(f"  pdflatex master_summary.tex")
    print(f"  pdflatex itemized_expenses.tex")
    print(f"  pdflatex merchant_summary.tex")
    print(f"  pdflatex merchant_monthly_dates.tex")
    print(f"  pdflatex categorized_spending.tex")
    print(f"  pdflatex category_by_month.tex")
    print(f"  pdflatex reimbursement_reconciliation.tex")


if __name__ == '__main__':
    compile_all_expense_pdfs()
