@echo off
REM Setup script for API Error Codes Validation Project
echo ========================================
echo API Error Codes Validation - Setup
echo ========================================
echo.

echo [1/4] Checking Node.js...
node --version
echo.

echo [2/4] Checking Python...
python --version
echo.

echo [3/4] Installing Node.js dependencies...
call npm install
echo.

echo [4/4] Installing Python dependencies...
pip install pytest pyyaml requests python-dotenv jsonschema colorlog
echo.

echo ========================================
echo Setup completed!
echo ========================================
echo.
echo Run: npm test (for JavaScript tests)
echo Run: pytest tests/ (for Python tests)
pause
