"""
Generate LaTeX/PDF report for reimbursement reconciliation
"""

import pandas as pd
from pathlib import Path
import subprocess

def generate_reimbursement_reconciliation_latex():
    """Generate comprehensive reimbursement reconciliation report"""
    
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    reconciliation_file = base_path / 'reimbursement_reconciliation.csv'
    
    if not reconciliation_file.exists():
        print(f"⚠ File not found: {reconciliation_file}")
        return None
    
    df = pd.read_csv(reconciliation_file)
    df['Date'] = pd.to_datetime(df['Date'])
    
    latex_content = []
    
    # Preamble
    latex_content.append(r'''\documentclass[10pt,letterpaper,landscape]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=0.5in]{geometry}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{fancyhdr}

\definecolor{titleblue}{RGB}{102,126,234}
\definecolor{successgreen}{RGB}{46,125,50}
\definecolor{warningorange}{RGB}{255,152,0}
\definecolor{errorred}{RGB}{211,47,47}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textcolor{titleblue}{Reimbursement Reconciliation Report}}
\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.5pt}

\title{\textcolor{titleblue}{\textbf{Reimbursement Reconciliation Report}}}
\author{JTech Logistics - Customer Reimbursement Tracking}
\date{August - December 2025}

\begin{document}

\maketitle

\section*{Executive Summary}

This report reconciles customer reimbursements across four data sources:
\begin{itemize}
\item \textbf{Uber Payments} - What Uber claims they paid as reimbursements
\item \textbf{Receipt Tracker} - Manually tracked reimbursements (72 entries)
\item \textbf{Trips Data} - Actual trip/delivery details
\item \textbf{Bank Statements} - Actual money received in bank account
\end{itemize}

''')
    
    # Overall statistics
    total_uber = df['Uber_Amount'].sum()
    total_bank = df[df['Bank_Match'] == 'Yes']['Bank_Amount'].sum()
    receipt_matches = len(df[df['Receipt_Match'] == 'Yes'])
    bank_matches = len(df[df['Bank_Match'] == 'Yes'])
    
    latex_content.append(f'''
\\subsection*{{Overall Statistics}}

\\begin{{tabular}}{{ll}}
\\toprule
\\textbf{{Metric}} & \\textbf{{Value}} \\\\
\\midrule
Total Reimbursements (Uber Claims) & \\${total_uber:,.2f} ({len(df)} transactions) \\\\
Total Bank Received & \\${total_bank:,.2f} ({bank_matches} payments) \\\\
\\textcolor{{warningorange}}{{Difference}} & \\textcolor{{warningorange}}{{\\${total_bank - total_uber:,.2f}}} \\\\
\\midrule
Receipt Tracker Matches & {receipt_matches}/{len(df)} ({receipt_matches/len(df)*100:.1f}\\%) \\\\
Bank Payment Matches & {bank_matches}/{len(df)} ({bank_matches/len(df)*100:.1f}\\%) \\\\
\\bottomrule
\\end{{tabular}}

\\vspace{{0.5cm}}

\\textit{{Note: Bank received amount is higher than Uber claims, indicating the matching algorithm may be picking up related transactions or timing differences in how amounts are reported.}}

\\newpage

''')
    
    # Monthly breakdown
    latex_content.append("\\section*{Monthly Reconciliation}\n\n")
    
    for month in sorted(df['Month'].unique()):
        month_data = df[df['Month'] == month]
        month_label = pd.to_datetime(month + '-01').strftime('%B %Y')
        
        uber_total = month_data['Uber_Amount'].sum()
        bank_total = month_data[month_data['Bank_Match'] == 'Yes']['Bank_Amount'].sum()
        
        latex_content.append(f"\\subsection*{{{month_label}}}\n")
        latex_content.append(f"Uber Claims: \\${uber_total:,.2f} | Bank Received: \\${bank_total:,.2f} | Difference: \\${bank_total - uber_total:,.2f}\n\n")
        
        latex_content.append("\\begin{longtable}{p{2cm}p{4cm}rp{1.5cm}p{1.5cm}p{1.5cm}rr}")
        latex_content.append("\\toprule")
        latex_content.append("\\textbf{Date} & \\textbf{Description} & \\textbf{Uber Amount} & \\textbf{Receipt} & \\textbf{Trip} & \\textbf{Bank} & \\textbf{Bank Amount} & \\textbf{Difference} \\\\")
        latex_content.append("\\midrule")
        
        for _, row in month_data.iterrows():
            date_str = pd.to_datetime(row['Date']).strftime('%m/%d')
            desc = str(row['Description'])[:30].replace('&', '\\&').replace('_', '\\_')
            uber_amt = row['Uber_Amount']
            
            receipt = 'Y' if row['Receipt_Match'] == 'Yes' else 'N'
            trip = 'Y' if row['Trip_Match'] == 'Yes' else 'N'
            bank = 'Y' if row['Bank_Match'] == 'Yes' else 'N'
            
            bank_amt = row['Bank_Amount'] if pd.notna(row['Bank_Amount']) else 0
            diff = bank_amt - uber_amt
            
            # Color code the match status
            receipt_color = 'successgreen' if receipt == 'Y' else 'errorred'
            bank_color = 'successgreen' if bank == 'Y' else 'errorred'
            diff_color = 'warningorange' if abs(diff) > 0.50 else 'black'
            
            latex_content.append(f"{date_str} & {desc} & \\${uber_amt:.2f} & "
                               f"\\textcolor{{{receipt_color}}}{{{receipt}}} & "
                               f"{trip} & "
                               f"\\textcolor{{{bank_color}}}{{{bank}}} & "
                               f"\\${bank_amt:.2f} & "
                               f"\\textcolor{{{diff_color}}}{{\\${diff:.2f}}} \\\\")
        
        latex_content.append("\\midrule")
        latex_content.append(f"\\textbf{{Month Total}} & & \\textbf{{\\${uber_total:.2f}}} & & & & \\textbf{{\\${bank_total:.2f}}} & \\textbf{{\\${bank_total - uber_total:.2f}}} \\\\")
        latex_content.append("\\bottomrule")
        latex_content.append("\\end{longtable}")
        latex_content.append("\\vspace{0.5cm}\n")
    
    # Summary statistics table
    latex_content.append("\\newpage")
    latex_content.append("\\section*{Match Rate Analysis}\n\n")
    
    latex_content.append("\\begin{longtable}{lrr}")
    latex_content.append("\\toprule")
    latex_content.append("\\textbf{Month} & \\textbf{Receipt Matches} & \\textbf{Bank Matches} \\\\")
    latex_content.append("\\midrule")
    
    for month in sorted(df['Month'].unique()):
        month_data = df[df['Month'] == month]
        month_label = pd.to_datetime(month + '-01').strftime('%B %Y')
        
        receipt_rate = len(month_data[month_data['Receipt_Match'] == 'Yes']) / len(month_data) * 100
        bank_rate = len(month_data[month_data['Bank_Match'] == 'Yes']) / len(month_data) * 100
        
        latex_content.append(f"{month_label} & {receipt_rate:.1f}\\% ({len(month_data[month_data['Receipt_Match'] == 'Yes'])}/{len(month_data)}) & "
                           f"{bank_rate:.1f}\\% ({len(month_data[month_data['Bank_Match'] == 'Yes'])}/{len(month_data)}) \\\\")
    
    latex_content.append("\\midrule")
    overall_receipt = len(df[df['Receipt_Match'] == 'Yes']) / len(df) * 100
    overall_bank = len(df[df['Bank_Match'] == 'Yes']) / len(df) * 100
    latex_content.append(f"\\textbf{{Overall}} & \\textbf{{{overall_receipt:.1f}\\%}} & \\textbf{{{overall_bank:.1f}\\%}} \\\\")
    latex_content.append("\\bottomrule")
    latex_content.append("\\end{longtable}")
    
    latex_content.append("\\end{document}")
    
    # Write to file
    output_file = base_path / 'reports' / 'latex' / 'reimbursement_reconciliation.tex'
    output_file.parent.mkdir(exist_ok=True, parents=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(latex_content))
    
    print(f"✓ Generated: {output_file}")
    
    # Compile to PDF
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', 'reimbursement_reconciliation.tex'],
            cwd=output_file.parent,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        pdf_file = output_file.with_suffix('.pdf')
        if pdf_file.exists():
            print(f"✓ Created PDF: {pdf_file}")
        else:
            print(f"⚠ PDF compilation may have failed")
    except Exception as e:
        print(f"⚠ Error compiling PDF: {e}")
    
    return output_file


if __name__ == '__main__':
    print("=" * 80)
    print("GENERATING REIMBURSEMENT RECONCILIATION REPORT")
    print("=" * 80)
    print()
    
    generate_reimbursement_reconciliation_latex()
    
    print()
    print("=" * 80)
    print("COMPLETE")
    print("=" * 80)
