@echo off
REM Evidence Capture Script for Sureprep API Test Suite
REM This script runs each test step and pauses for screenshot capture

echo.
echo ============================================================
echo   SCREENSHOT EVIDENCE CAPTURE GUIDE
echo   Sureprep API Test Suite
echo ============================================================
echo.
echo This script will run each test step and pause for screenshots.
echo.
echo INSTRUCTIONS:
echo 1. When output appears, press Windows + Shift + S to capture
echo 2. Select the entire window/relevant content
echo 3. Save screenshot with the suggested filename
echo 4. Press any key to continue to next step
echo.
echo Ready to start? Press any key...
pause >nul
echo.

REM Create evidence folder
if not exist "evidence" mkdir evidence
echo Created evidence folder: .\evidence\
echo.

REM ============================================================
echo.
echo ============================================================
echo STEP 1 of 6: Credential Verification
echo ============================================================
echo.
echo Running: python scripts\verify_credentials.py
echo.
echo CAPTURE THIS AS: evidence\01_credential_verification.png
echo.
echo What to capture:
echo - V5.0 API: [OK] PASSED
echo - V7 API: [OK] PASSED
echo - Status Code: 200 for both
echo - Tokens received
echo - Timestamp
echo.
pause
cls

python scripts\verify_credentials.py

echo.
echo.
echo ============================================================
echo Did you capture the screenshot?
echo Save as: evidence\01_credential_verification.png
echo ============================================================
echo Press any key to continue to Step 2...
pause >nul
cls

REM ============================================================
echo.
echo ============================================================
echo STEP 2 of 6: Authentication Test Execution
echo ============================================================
echo.
echo Running: pytest tests\test_sureprep_api_suite.py -v -m authentication
echo.
echo CAPTURE THIS AS: evidence\02_authentication_tests.png
echo.
echo What to capture:
echo - Test collection results
echo - PASSED status for V5 and V7 tests
echo - Execution time
echo - Summary: 2 passed
echo.
pause
cls

pytest tests\test_sureprep_api_suite.py -v -m authentication

echo.
echo.
echo ============================================================
echo Did you capture the screenshot?
echo Save as: evidence\02_authentication_tests.png
echo ============================================================
echo Press any key to continue to Step 3...
pause >nul
cls

REM ============================================================
echo.
echo ============================================================
echo STEP 3 of 6: HTML Test Report
echo ============================================================
echo.
echo Opening HTML report in your default browser...
echo.
echo CAPTURE THIS AS: evidence\03_html_report_summary.png
echo.
echo What to capture:
echo - Report header with timestamp
echo - Summary (passed/failed/skipped)
echo - Total duration
echo - Test results table
echo.
echo Press any key to open report...
pause >nul

start reports\api_error_validation_report.html

echo.
echo Browser should have opened with the HTML report.
echo.
echo TO CAPTURE FULL PAGE IN BROWSER:
echo - Firefox: Press Ctrl+Shift+S, then click "Save full page"
echo - Chrome: Press F12, then Ctrl+Shift+P, type "screenshot", select "Capture full size screenshot"
echo - Or use Windows+Shift+S to capture visible area
echo.
echo ============================================================
echo Did you capture the HTML report?
echo Save as: evidence\03_html_report_summary.png
echo ============================================================
echo Press any key to continue to Step 4...
pause >nul
cls

REM ============================================================
echo.
echo ============================================================
echo STEP 4 of 6: Test Data Configuration
echo ============================================================
echo.
echo Opening test data file in VS Code...
echo.
echo CAPTURE THIS AS: evidence\04_test_data_config.png
echo.
echo What to capture:
echo - V5 credentials section (UserName, Password, APIKey)
echo - V7 credentials section (ClientID, ClientSecret)
echo - JSON structure
echo - Lines 1-20
echo.
echo Press any key to open file...
pause >nul

code testData\sureprep_test_data.json

echo.
echo VS Code should have opened with testData\sureprep_test_data.json
echo.
echo Capture the credentials section (lines 1-20)
echo Use Windows+Shift+S to capture
echo.
echo ============================================================
echo Did you capture the test data config?
echo Save as: evidence\04_test_data_config.png
echo ============================================================
echo Press any key to continue to Step 5...
pause >nul
cls

REM ============================================================
echo.
echo ============================================================
echo STEP 5 of 6: Pytest Log File
echo ============================================================
echo.
echo Opening pytest.log in VS Code...
echo.
echo CAPTURE THIS AS: evidence\05_pytest_logs.png
echo.
echo What to capture:
echo - Log entries with timestamps
echo - API requests to /Authenticate/GetToken
echo - Status Code 200 responses
echo - Search for: "Authenticate/GetToken" in the log
echo.
echo Press any key to open log file...
pause >nul

code reports\pytest.log

echo.
echo VS Code should have opened with reports\pytest.log
echo.
echo Search for "Authenticate/GetToken" (Ctrl+F)
echo Capture the authentication log entries
echo.
echo ============================================================
echo Did you capture the log file?
echo Save as: evidence\05_pytest_logs.png
echo ============================================================
echo Press any key to continue to Step 6...
pause >nul
cls

REM ============================================================
echo.
echo ============================================================
echo STEP 6 of 6: Project Structure
echo ============================================================
echo.
echo Opening project in VS Code Explorer...
echo.
echo CAPTURE THIS AS: evidence\06_project_structure.png
echo.
echo What to capture:
echo - VS Code Explorer (Ctrl+Shift+E)
echo - Folder tree showing: tests, testData, reports, docs, scripts
echo - Key files visible
echo.
echo Press any key to show file structure...
pause >nul

echo.
echo Project Structure:
echo.
tree /F /A
echo.
echo.
echo Also capture the VS Code Explorer view if you have VS Code open
echo (Press Ctrl+Shift+E to show Explorer in VS Code)
echo.
echo ============================================================
echo Did you capture the project structure?
echo Save as: evidence\06_project_structure.png
echo ============================================================
echo Press any key to continue...
pause >nul
cls

REM ============================================================
echo.
echo ============================================================
echo   EVIDENCE CAPTURE COMPLETE!
echo ============================================================
echo.
echo You should now have captured 6 screenshots:
echo.
echo [1] evidence\01_credential_verification.png
echo [2] evidence\02_authentication_tests.png
echo [3] evidence\03_html_report_summary.png
echo [4] evidence\04_test_data_config.png
echo [5] evidence\05_pytest_logs.png
echo [6] evidence\06_project_structure.png
echo.
echo ============================================================
echo.
echo All screenshots should be saved in the 'evidence' folder.
echo.
echo Would you like to open the evidence folder? (Y/N)
set /p openevidence="Your choice: "

if /i "%openevidence%"=="Y" (
    echo Opening evidence folder...
    explorer evidence
)

echo.
echo ============================================================
echo   NEXT STEPS:
echo ============================================================
echo.
echo 1. Review all screenshots in evidence\ folder
echo 2. Ensure all screenshots are clear and readable
echo 3. Create documentation package if needed
echo 4. See docs\SCREENSHOT_EVIDENCE_GUIDE.md for more details
echo.
echo ============================================================
echo.
echo Thank you! Press any key to exit...
pause >nul
