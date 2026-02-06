@echo off
REM Sureprep API Test Suite Execution Script
REM This script provides easy ways to run different test scenarios

echo ========================================
echo   Sureprep API Test Suite Runner
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if pytest is installed
python -c "import pytest" >nul 2>&1
if %errorlevel% neq 0 (
    echo Pytest not found. Installing dependencies...
    pip install -r requirements_sureprep.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create directories if they don't exist
if not exist "reports" mkdir reports
if not exist "logs" mkdir logs

echo.
echo Select test execution option:
echo.
echo 1. Run ALL tests with HTML report
echo 2. Run Authentication tests only
echo 3. Run Binder tests (BinderInfo + Binder CRUD)
echo 4. Run TaxCaddy tests
echo 5. Run Negative/Security tests
echo 6. Run Performance tests
echo 7. Run Smoke tests (quick critical tests)
echo 8. Run ALL tests in parallel (faster)
echo 9. Run specific test by name
echo 0. Exit
echo.

set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" (
    echo Running ALL tests...
    pytest tests/test_sureprep_api_suite.py -v --html=reports/sureprep_test_report.html --self-contained-html
    goto :end
)

if "%choice%"=="2" (
    echo Running Authentication tests...
    pytest tests/test_sureprep_api_suite.py -v -m authentication --html=reports/auth_test_report.html --self-contained-html
    goto :end
)

if "%choice%"=="3" (
    echo Running Binder tests...
    pytest tests/test_sureprep_api_suite.py -v -m "binderinfo or binder" --html=reports/binder_test_report.html --self-contained-html
    goto :end
)

if "%choice%"=="4" (
    echo Running TaxCaddy tests...
    pytest tests/test_sureprep_api_suite.py -v -m taxcaddy --html=reports/taxcaddy_test_report.html --self-contained-html
    goto :end
)

if "%choice%"=="5" (
    echo Running Negative/Security tests...
    pytest tests/test_sureprep_api_suite.py -v -m negative --html=reports/negative_test_report.html --self-contained-html
    goto :end
)

if "%choice%"=="6" (
    echo Running Performance tests...
    pytest tests/test_sureprep_api_suite.py -v -m performance --html=reports/performance_test_report.html --self-contained-html
    goto :end
)

if "%choice%"=="7" (
    echo Running Smoke tests...
    pytest tests/test_sureprep_api_suite.py -v -m smoke --html=reports/smoke_test_report.html --self-contained-html
    goto :end
)

if "%choice%"=="8" (
    echo Running ALL tests in parallel (4 workers)...
    pytest tests/test_sureprep_api_suite.py -v -n 4 --html=reports/sureprep_test_report.html --self-contained-html
    goto :end
)

if "%choice%"=="9" (
    set /p testname="Enter test name (e.g., test_auth_v7_get_token): "
    echo Running test: %testname%...
    pytest tests/test_sureprep_api_suite.py -v -k "%testname%" --html=reports/custom_test_report.html --self-contained-html
    goto :end
)

if "%choice%"=="0" (
    echo Exiting...
    exit /b 0
)

echo Invalid choice. Please run the script again.
pause
exit /b 1

:end
echo.
echo ========================================
echo   Test execution completed!
echo ========================================
echo.
echo Report location: reports\
echo Log location: logs\
echo.
echo Open HTML report? (Y/N)
set /p openreport="Your choice: "
if /i "%openreport%"=="Y" (
    start reports\sureprep_test_report.html 2>nul
    if not exist reports\sureprep_test_report.html (
        echo Report file not found. Check the execution logs above.
    )
)

echo.
echo Press any key to exit...
pause >nul
