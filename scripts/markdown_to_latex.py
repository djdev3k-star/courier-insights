"""
LaTeX Report Generator
Converts Markdown reports to professional LaTeX PDF documents
"""

import re
from pathlib import Path
from datetime import datetime

def markdown_to_latex(md_content, title="Courier Business Report"):
    """Convert markdown content to LaTeX"""
    
    # Escape special LaTeX characters
    def escape_latex(text):
        replacements = {
            '\\': r'\textbackslash{}',
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text
    
    latex_content = []
    
    # LaTeX preamble
    latex_content.append(r'''\documentclass[11pt,letterpaper]{article}

% Packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=1in]{geometry}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{enumitem}
\usepackage{tcolorbox}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{listings}

% Colors
\definecolor{titleblue}{RGB}{102,126,234}
\definecolor{headergray}{RGB}{240,240,240}
\definecolor{warningred}{RGB}{239,68,68}
\definecolor{successgreen}{RGB}{34,197,94}
\definecolor{infoyellow}{RGB}{251,191,36}

% Hyperlink setup
\hypersetup{
    colorlinks=true,
    linkcolor=titleblue,
    filecolor=titleblue,
    urlcolor=titleblue,
    citecolor=titleblue
}

% Header and footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\textcolor{titleblue}{Courier Business Analytics}}
\fancyhead[R]{\small\thepage}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0pt}

% Custom boxes
\newtcolorbox{alertbox}[1][]{
    colback=warningred!5,
    colframe=warningred,
    arc=3mm,
    boxrule=1pt,
    title=#1,
    fonttitle=\bfseries
}

\newtcolorbox{successbox}[1][]{
    colback=successgreen!5,
    colframe=successgreen,
    arc=3mm,
    boxrule=1pt,
    title=#1,
    fonttitle=\bfseries
}

\newtcolorbox{infobox}[1][]{
    colback=infoyellow!5,
    colframe=infoyellow,
    arc=3mm,
    boxrule=1pt,
    title=#1,
    fonttitle=\bfseries
}

% Title customization
\makeatletter
\renewcommand{\maketitle}{
    \begin{center}
        \vspace*{1cm}
        {\Huge\bfseries\color{titleblue}\@title\par}
        \vspace{0.5cm}
        {\large\@author\par}
        \vspace{0.3cm}
        {\large\@date\par}
        \vspace{1cm}
    \end{center}
}
\makeatother

\title{''' + escape_latex(title) + r'''}
\author{JTech Logistics}
\date{''' + datetime.now().strftime('%B %d, %Y') + r'''}

\begin{document}

\maketitle
\tableofcontents
\newpage

''')
    
    # Process markdown line by line
    lines = md_content.split('\n')
    in_code_block = False
    in_table = False
    table_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                latex_content.append(r'\begin{lstlisting}[basicstyle=\ttfamily\small, frame=single, breaklines=true]')
            else:
                in_code_block = False
                latex_content.append(r'\end{lstlisting}')
            i += 1
            continue
        
        if in_code_block:
            latex_content.append(line)
            i += 1
            continue
        
        # Headers
        if line.startswith('# '):
            title_text = escape_latex(line[2:].strip())
            latex_content.append(f'\n\\section{{{title_text}}}\n')
        elif line.startswith('## '):
            title_text = escape_latex(line[3:].strip())
            latex_content.append(f'\n\\subsection{{{title_text}}}\n')
        elif line.startswith('### '):
            title_text = escape_latex(line[4:].strip())
            latex_content.append(f'\n\\subsubsection{{{title_text}}}\n')
        elif line.startswith('#### '):
            title_text = escape_latex(line[5:].strip())
            latex_content.append(f'\n\\paragraph{{{title_text}}}\n')
        
        # Horizontal rules
        elif line.strip() == '---':
            latex_content.append('\n\\hrulefill\n')
        
        # Tables
        elif '|' in line and not in_table:
            in_table = True
            table_lines = [line]
        elif in_table:
            if '|' in line:
                table_lines.append(line)
            else:
                # Process table
                latex_content.append(format_table(table_lines))
                in_table = False
                table_lines = []
                # Process current line normally
                latex_content.append(process_normal_line(line))
        
        # Alert boxes (emoji indicators)
        elif '⚠️' in line or '❌' in line or 'ALERT' in line.upper() or 'WARNING' in line.upper():
            text = escape_latex(line.strip())
            latex_content.append(f'\\begin{{alertbox}}[Alert]\n{text}\n\\end{{alertbox}}\n')
        elif '✅' in line or 'SUCCESS' in line.upper():
            text = escape_latex(line.strip())
            latex_content.append(f'\\begin{{successbox}}[Success]\n{text}\n\\end{{successbox}}\n')
        elif '💡' in line or 'TIP' in line.upper() or 'NOTE' in line.upper():
            text = escape_latex(line.strip())
            latex_content.append(f'\\begin{{infobox}}[Note]\n{text}\n\\end{{infobox}}\n')
        
        # Lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            # Start itemize if not already in one
            if i == 0 or not (lines[i-1].strip().startswith('- ') or lines[i-1].strip().startswith('* ')):
                latex_content.append('\\begin{itemize}')
            item_text = escape_latex(line.strip()[2:])
            item_text = format_inline(item_text)
            latex_content.append(f'\\item {item_text}')
            # End itemize if next line is not a list item
            if i+1 >= len(lines) or not (lines[i+1].strip().startswith('- ') or lines[i+1].strip().startswith('* ')):
                latex_content.append('\\end{itemize}\n')
        
        # Numbered lists
        elif re.match(r'^\d+\.\s', line.strip()):
            # Start enumerate if not already in one
            if i == 0 or not re.match(r'^\d+\.\s', lines[i-1].strip()):
                latex_content.append('\\begin{enumerate}')
            item_text = escape_latex(re.sub(r'^\d+\.\s', '', line.strip()))
            item_text = format_inline(item_text)
            latex_content.append(f'\\item {item_text}')
            # End enumerate if next line is not a numbered item
            if i+1 >= len(lines) or not re.match(r'^\d+\.\s', lines[i+1].strip()):
                latex_content.append('\\end{enumerate}\n')
        
        # Empty lines
        elif line.strip() == '':
            latex_content.append('')
        
        # Normal paragraphs
        else:
            latex_content.append(process_normal_line(line))
        
        i += 1
    
    # Close document
    latex_content.append('\n\\end{document}')
    
    return '\n'.join(latex_content)

def format_table(table_lines):
    """Format markdown table to LaTeX"""
    if len(table_lines) < 2:
        return ''
    
    # Parse table
    rows = []
    for line in table_lines:
        if '---' in line:  # Skip separator line
            continue
        cells = [cell.strip() for cell in line.split('|') if cell.strip()]
        if cells:
            rows.append(cells)
    
    if not rows:
        return ''
    
    # Determine column count
    num_cols = len(rows[0])
    
    # Build LaTeX table
    latex = ['\\begin{center}']
    latex.append('\\begin{tabular}{' + '|'.join(['l'] * num_cols) + '}')
    latex.append('\\toprule')
    
    # Header row
    header = ' & '.join([f'\\textbf{{{escape_latex(cell)}}}' for cell in rows[0]])
    latex.append(header + ' \\\\')
    latex.append('\\midrule')
    
    # Data rows
    for row in rows[1:]:
        row_text = ' & '.join([escape_latex(cell) for cell in row])
        latex.append(row_text + ' \\\\')
    
    latex.append('\\bottomrule')
    latex.append('\\end{tabular}')
    latex.append('\\end{center}\n')
    
    return '\n'.join(latex)

def escape_latex(text):
    """Escape special LaTeX characters and remove emojis."""
    import re
    
    # Remove emojis (Unicode ranges for emojis and symbols)
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # extended symbols
        "\U00002600-\U000026FF"  # misc symbols
        "\uFE0F"                 # variation selector
        "]+", 
        flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)
    
    replacements = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def format_inline(text):
    """Format inline markdown (bold, italic, code)"""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'\\texttt{\1}', text)
    # Links [text](url)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'\\href{\2}{\1}', text)
    return text

def process_normal_line(line):
    """Process a normal paragraph line"""
    if not line.strip():
        return ''
    text = escape_latex(line.strip())
    text = format_inline(text)
    return text + '\n'

def convert_report(input_file, output_file=None):
    """Convert a markdown report to LaTeX"""
    
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"Error: File {input_file} not found")
        return
    
    # Read markdown content
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Generate output filename
    if output_file is None:
        output_file = input_path.stem + '.tex'
    
    output_path = Path(output_file)
    
    # Extract title from first header or filename
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else input_path.stem.replace('_', ' ').title()
    
    # Convert to LaTeX
    latex_content = markdown_to_latex(md_content, title)
    
    # Write LaTeX file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"✓ Converted: {input_file} → {output_path}")
    print(f"  To compile: pdflatex {output_path}")
    
    return str(output_path)

def batch_convert_reports():
    """Convert all key reports to LaTeX"""
    
    docs_dir = Path('c:/Users/dj-dev/Documents/courier/docs')
    
    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}")
        return
    
    # Key reports to convert
    reports = [
        'ACTUAL_VS_RECOMMENDED_REPORT.md',
        'SCHEDULE_OPTIMIZATION_PLAN.md',
        'SCHEDULE_SPENDING_CORRELATION_REPORT.md',
        'UNCATEGORIZED_MERCHANT_ANALYSIS_REPORT.md',
        'EXPENSE_REPORT.md',
        'SCHEDULE_QUICK_REFERENCE.md',
        '../SPENDING_BREAKDOWN_SUMMARY.md',
        '../CALCULATION_ERROR_REPORT.md',
        '../QUICK_REFERENCE_PHASE9.md'
    ]
    
    output_dir = Path('c:/Users/dj-dev/Documents/courier/reports/latex')
    output_dir.mkdir(exist_ok=True)
    
    converted = []
    
    for report in reports:
        input_file = docs_dir / report
        if input_file.exists():
            output_file = output_dir / (input_file.stem + '.tex')
            tex_file = convert_report(str(input_file), str(output_file))
            if tex_file:
                converted.append(tex_file)
    
    print(f"\n{'='*80}")
    print(f"BATCH CONVERSION COMPLETE")
    print(f"{'='*80}")
    print(f"\nConverted {len(converted)} files to LaTeX")
    print(f"Output directory: {output_dir}")
    print(f"\nTo compile all PDFs:")
    print(f"  cd {output_dir}")
    print(f"  for file in *.tex; do pdflatex $file; done")
    
    return converted

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Single file conversion
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        convert_report(input_file, output_file)
    else:
        # Batch conversion
        print("Converting all key reports to LaTeX...\n")
        batch_convert_reports()
