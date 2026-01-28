@echo off
REM Compile master_summary.tex to PDF
REM This batch file attempts to use pdflatex if available in PATH

cd /d "C:\Users\dj-dev\Documents\courier\reports\latex"

echo Attempting to compile master_summary.tex...
echo.

REM Try to find pdflatex
where pdflatex >nul 2>&1
if %errorlevel% equ 0 (
    echo pdflatex found in PATH
    pdflatex -interaction=nonstopmode master_summary.tex
    if exist master_summary.pdf (
        echo.
        echo Success! Generated master_summary.pdf
    ) else (
        echo.
        echo Compilation completed but PDF not found
    )
) else (
    echo pdflatex not found in PATH
    echo Attempting common installation paths...
    
    if exist "C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe" (
        "C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe" -interaction=nonstopmode master_summary.tex
    ) else if exist "C:\Users\dj-dev\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe" (
        "C:\Users\dj-dev\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe" -interaction=nonstopmode master_summary.tex
    ) else (
        echo.
        echo ERROR: pdflatex not found. Please install MiKTeX first.
        echo Download from: https://miktex.org/download
        exit /b 1
    )
)

if exist master_summary.pdf (
    echo.
    echo ✓ master_summary.pdf created successfully
    exit /b 0
) else (
    echo.
    echo ✗ Failed to create master_summary.pdf
    exit /b 1
)
