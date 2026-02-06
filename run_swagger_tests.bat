@echo off
REM Batch script to run auto-generated Swagger API tests and generate reports

echo ================================================================
echo Running Auto-Generated Swagger API Test Suite
echo ================================================================
echo.

REM Set environment variables
set SUREPREP_BASE_URL=https://devtr-api-iscrum.sureprep.com

REM V5 Credentials
set SUREPREP_V5_USERNAME=PRIYA1
set SUREPREP_V5_PASSWORD=Abcd@12345
set SUREPREP_V5_API_KEY=C690222D-8625-46F7-92CC-A61DA060D7A9

REM V7 Credentials
set SUREPREP_V7_CLIENT_ID=GxJQo22jTg9koTeDtbIHpg8nmWdns9cu
set SUREPREP_V7_CLIENT_SECRET=yZdKNGi2b-Fsp1uWZllPnST7VM2PdSc3hDC4_rZ5tfGektIltwkfYPLLDEGD6f_M

REM Create reports directory if it doesn't exist
if not exist "reports" mkdir reports
if not exist "logs" mkdir logs

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Running tests...
echo.

REM Run pytest with HTML report generation
pytest tests\test_auto_generated_swagger_apis.py ^
    -v ^
    --html=reports\swagger_api_test_report_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.html ^
    --self-contained-html ^
    --tb=short ^
    --maxfail=0 ^
    --continue-on-collection-errors ^
    -o log_cli=true ^
    -o log_cli_level=INFO

echo.
echo ================================================================
echo Test execution completed!
echo ================================================================
echo.
echo Check the reports folder for the HTML report
echo.

pause
