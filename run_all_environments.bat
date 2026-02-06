@echo off
REM Master Test Suite Runner - Run tests across all environments
REM Batch file wrapper for run_all_environments.py

echo.
echo ================================================================================
echo   Multi-Environment Test Suite Runner
echo   Running tests across: Devtr, QA, Staging, (optional) Production
echo ================================================================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Run the Python test runner
python run_all_environments.py

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%

REM Pause to see results
echo.
echo ================================================================================
echo   Press any key to exit...
echo ================================================================================
pause

exit /b %EXIT_CODE%
