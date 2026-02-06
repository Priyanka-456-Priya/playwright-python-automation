@echo off
REM Test Suite Runner for DEVTR Environment
REM Batch file wrapper for run_tests_devtr.py

echo.
echo ================================================================================
echo   Running DEVTR Environment Test Suite
echo ================================================================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Run the Python test runner
python run_tests_devtr.py

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%

REM Pause to see results
echo.
echo ================================================================================
echo   Press any key to exit...
echo ================================================================================
pause

exit /b %EXIT_CODE%
