@echo off
REM API Error Codes Validation - Test Runner Script
REM Quick script to run tests with common options

echo ================================================
echo API Error Codes Validation Framework - Test Runner
echo ================================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Check if argument provided
if "%1"=="" (
    echo Running all tests...
    pytest
) else if "%1"=="smoke" (
    echo Running smoke tests only...
    pytest -m smoke
) else if "%1"=="4xx" (
    echo Running 4xx error tests...
    pytest -m error_4xx
) else if "%1"=="5xx" (
    echo Running 5xx error tests...
    pytest -m error_5xx
) else if "%1"=="playwright" (
    echo Running Playwright UI tests...
    pytest -m playwright
) else if "%1"=="quick" (
    echo Running quick tests (no Playwright)...
    pytest -m "not playwright"
) else if "%1"=="collect" (
    echo Collecting tests (dry run)...
    pytest --collect-only
) else (
    echo Running tests matching: %1
    pytest -k "%1"
)

echo.
echo ================================================
echo Test execution complete!
echo ================================================
echo.
echo View HTML report: reports\api_error_validation_report.html
echo View logs: reports\pytest.log
echo.
echo Test options:
echo   run_tests.bat          - Run all tests
echo   run_tests.bat smoke    - Run smoke tests
echo   run_tests.bat 4xx      - Run 4xx error tests
echo   run_tests.bat 5xx      - Run 5xx error tests
echo   run_tests.bat playwright - Run UI tests
echo   run_tests.bat quick    - Run tests without Playwright
echo   run_tests.bat collect  - List all tests (dry run)
echo   run_tests.bat "test_name" - Run tests matching name
echo ================================================
pause
