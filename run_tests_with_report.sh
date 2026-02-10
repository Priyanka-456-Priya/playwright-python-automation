#!/bin/bash
################################################################################
# Run API Tests and Open Allure Report Automatically
################################################################################

echo ""
echo "============================================================================"
echo "  SurePrep API Test Suite - Automated Test Runner"
echo "============================================================================"
echo ""
echo "[1/2] Running tests..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Run tests with pytest
pytest tests/test_TY2025_swagger_apis.py -v

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================================"
    echo "  Tests completed successfully!"
    echo "============================================================================"
    echo ""
else
    echo ""
    echo "============================================================================"
    echo "  Tests completed with some failures"
    echo "============================================================================"
    echo ""
fi

echo "[2/2] Generating and opening Allure report..."
echo ""

# Generate and serve Allure report (opens automatically in browser)
allure serve reports/allure-results
