@echo off
REM Batch compile all LaTeX files to PDF
REM Requires MiKTeX or TeX Live installed

echo ========================================
echo LaTeX PDF Compilation Script
echo ========================================
echo.

cd /d "c:\Users\dj-dev\Documents\courier\reports\latex"

echo Checking for pdflatex...
where pdflatex >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pdflatex not found!
    echo.
    echo Please install MiKTeX or TeX Live:
    echo   - MiKTeX: https://miktex.org/download
    echo   - TeX Live: https://www.tug.org/texlive/
    echo.
    pause
    exit /b 1
)

echo Found pdflatex. Starting compilation...
echo.

for %%f in (*.tex) do (
    echo Compiling: %%f
    pdflatex -interaction=nonstopmode "%%f" > nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo   [OK] %%~nf.pdf created
    ) else (
        echo   [ERROR] Failed to compile %%f
    )
    echo.
)

echo ========================================
echo Cleaning up auxiliary files...
echo ========================================
del *.aux *.log *.out *.toc >nul 2>nul

echo.
echo ========================================
echo Compilation Complete!
echo ========================================
echo.
echo PDF files are in: %CD%
echo.
pause
