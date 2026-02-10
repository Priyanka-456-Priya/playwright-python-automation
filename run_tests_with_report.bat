@echo off
REM ============================================================================
REM Run API Tests and Open Allure Report Automatically
REM ============================================================================

echo.
echo ============================================================================
echo   SurePrep API Test Suite - Automated Test Runner
echo ============================================================================
echo.
echo [1/2] Running tests...
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Run tests with pytest
pytest tests/test_TY2025_swagger_apis.py -v

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================================
    echo   Tests completed successfully!
    echo ============================================================================
    echo.
) ELSE (
    echo.
    echo ============================================================================
    echo   Tests completed with some failures
    echo ============================================================================
    echo.
)

echo [2/2] Generating and opening Allure report...
echo.

REM Generate and serve Allure report (opens automatically in browser)
allure serve reports/allure-results

pause
