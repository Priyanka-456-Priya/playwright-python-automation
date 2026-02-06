@echo off
REM Run tests specifically for Devtr environment
REM Usage: run_devtr_tests.bat [pytest arguments]

echo ======================================================================
echo   Devtr Environment Test Runner
echo ======================================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    exit /b 1
)

REM Run the Python test runner script
python run_devtr_tests.py %*

exit /b %errorlevel%
