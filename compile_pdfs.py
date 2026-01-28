"""
Compile all LaTeX files to PDF
"""

import subprocess
from pathlib import Path
import os
import sys

def find_pdflatex():
    """Attempt to locate pdflatex in common installation paths"""
    common_paths = [
        r'C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe',
        r'C:\Program Files (x86)\MiKTeX\miktex\bin\x64\pdflatex.exe',
        r'C:\Users\dj-dev\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe',
        r'C:\Program Files\TeX Live\2024\bin\win32\pdflatex.exe',
        r'C:\texlive\2024\bin\win32\pdflatex.exe',
    ]
    
    # First try PATH
    result = subprocess.run(['where', 'pdflatex'], capture_output=True, text=True)
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip().split('\n')[0]
    
    # Check common paths
    for path in common_paths:
        if Path(path).exists():
            print(f"Found pdflatex at: {path}")
            return path
    
    return None

def compile_latex_to_pdf(tex_file):
    """Compile single LaTeX file to PDF"""
    
    pdflatex_path = find_pdflatex()
    
    if not pdflatex_path:
        print(f"⚠ pdflatex not found. Cannot compile {tex_file.name}")
        print("  Install MiKTeX from https://miktex.org/download")
        return False
    
    try:
        print(f"Compiling {tex_file.name}...")
        result = subprocess.run(
            [pdflatex_path, '-interaction=nonstopmode', str(tex_file)],
            cwd=str(tex_file.parent),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            pdf_file = tex_file.with_suffix('.pdf')
            if pdf_file.exists():
                print(f"  ✓ Created: {pdf_file.name}")
                return True
            else:
                print(f"  ⚠ Compilation appeared to succeed but PDF not found")
                return False
        else:
            print(f"  ✗ Compilation failed (return code: {result.returncode})")
            if result.stdout:
                print(f"    Output: {result.stdout[:200]}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"  ✗ Compilation timed out")
        return False
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False


def main():
    base_path = Path('c:/Users/dj-dev/Documents/courier')
    latex_dir = base_path / 'reports' / 'latex'
    
    # List of LaTeX files to compile
    tex_files = [
        'master_summary.tex',
        'itemized_expenses.tex',
        'merchant_summary.tex',
        'merchant_monthly_dates.tex',
        'categorized_spending.tex',
        'category_by_month.tex',
        'reimbursement_reconciliation.tex',
    ]
    
    print("="*80)
    print("COMPILING LaTeX FILES TO PDF")
    print("="*80)
    print()
    
    compiled = 0
    failed = 0
    
    for tex_filename in tex_files:
        tex_file = latex_dir / tex_filename
        
        if not tex_file.exists():
            print(f"⚠ {tex_filename} - File not found")
            continue
        
        if compile_latex_to_pdf(tex_file):
            compiled += 1
        else:
            failed += 1
    
    print()
    print("="*80)
    print(f"RESULTS: {compiled} compiled, {failed} failed")
    print("="*80)
    print()
    
    if failed > 0:
        print("If pdflatex is not installed:")
        print("  1. Download MiKTeX Basic: https://miktex.org/download")
        print("  2. Install it (will add pdflatex to PATH)")
        print("  3. Re-run this script")
        print()


if __name__ == '__main__':
    main()
