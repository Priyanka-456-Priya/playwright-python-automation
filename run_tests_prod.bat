@echo off
REM Test Suite Runner for PRODUCTION Environment
REM Batch file wrapper for run_tests_prod.py
REM WARNING: This runs tests against PRODUCTION!

echo.
echo ********************************************************************************
echo   !!! PRODUCTION ENVIRONMENT WARNING !!!
echo   Running tests against PRODUCTION environment
echo ********************************************************************************
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Run the Python test runner (will prompt for confirmation)
python run_tests_prod.py

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%

REM Pause to see results
echo.
echo ================================================================================
echo   Press any key to exit...
echo ================================================================================
pause

exit /b %EXIT_CODE%
