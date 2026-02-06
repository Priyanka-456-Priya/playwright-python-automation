# Allure Reporting Guide

## Overview
Allure Framework is now integrated into your API test suite, providing rich, interactive HTML reports with detailed test execution information.

## What Was Added

### 1. Allure Integration
- ✅ Installed `allure-pytest` package
- ✅ Updated `pytest.ini` configuration
- ✅ Added Allure decorators to all 113 test methods
- ✅ Enhanced test methods with Allure attachments for request/response data

### 2. Test Enhancements
Each test now includes:
- **@allure.story()** - Categorizes tests by functionality (Authentication, Binder Operations, etc.)
- **@allure.title()** - Descriptive test titles with TC numbers and endpoints
- **@allure.severity()** - Test severity levels (CRITICAL, NORMAL)
- **Allure attachments** - Request details, response status, and response body

### 3. Report Features
Your Allure reports include:
- ✅ Test execution timeline
- ✅ Categorization by features and stories
- ✅ Severity-based filtering
- ✅ Request/Response attachments for each test
- ✅ Failure details with stack traces
- ✅ Test history and trends
- ✅ Interactive charts and graphs

## Running Tests with Allure

### Basic Test Execution
```bash
# Run all tests with Allure reporting
pytest tests/test_TY2025_swagger_apis.py

# Run with verbose output
pytest tests/test_TY2025_swagger_apis.py -v

# Run specific test
pytest tests/test_TY2025_swagger_apis.py::TestSwaggerAPIs::test_v5_0_authenticate_gettoken_1
```

### Generate Allure Report
```bash
# Generate HTML report from results
allure generate reports/allure-results -o reports/allure-report --clean

# Generate and automatically open in browser
allure serve reports/allure-results
```

### View Existing Report
```bash
# Open the generated report
allure open reports/allure-report
```

## Report Location
- **Allure Results**: `reports/allure-results/` (JSON files)
- **Allure HTML Report**: `reports/allure-report/` (HTML report)

## Complete Workflow

### 1. Run Tests
```bash
pytest tests/test_TY2025_swagger_apis.py
```

### 2. Generate Report
```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

### 3. View Report
```bash
# Option 1: Open with Allure CLI (recommended)
allure open reports/allure-report

# Option 2: Open index.html directly in browser
# Navigate to: reports/allure-report/index.html
```

## Test Categorization

### By Story (Functionality)
- **Authentication** - Login and token management tests (CRITICAL)
- **Binder Operations** - Binder CRUD operations (CRITICAL)
- **Billing** - Billing and payment tests (NORMAL)
- **Document Management** - Document upload/download (NORMAL)
- **TaxCaddy API** - TaxCaddy integration tests (NORMAL)
- **DRL Operations** - DRL-related tests (NORMAL)
- **UT Integration** - UT system integration (NORMAL)
- **API Operations** - General API tests (NORMAL)

### By Severity
- **CRITICAL** - Authentication and core binder operations
- **NORMAL** - All other API endpoints

## Pytest Configuration

The `pytest.ini` file now includes:
```ini
addopts =
    -v
    --strict-markers
    --tb=short
    --alluredir=reports/allure-results
    --clean-alluredir
    --capture=no
    -p no:warnings
```

## Tips and Best Practices

### 1. Clean Reports Between Runs
```bash
# The --clean-alluredir flag automatically cleans old results
pytest tests/test_TY2025_swagger_apis.py
```

### 2. Filter Tests by Marker
```bash
# Run only authentication tests
pytest tests/test_TY2025_swagger_apis.py -m authentication

# Run only critical tests
pytest tests/test_TY2025_swagger_apis.py -m "severity:critical"
```

### 3. Parallel Execution (if needed)
```bash
# Install pytest-xdist first: pip install pytest-xdist
pytest tests/test_TY2025_swagger_apis.py -n auto --alluredir=reports/allure-results
```

### 4. Generate Trend History
Keep the `allure-report/history` folder to track test trends over time:
```bash
# Copy history before regenerating
cp -r reports/allure-report/history reports/allure-results/history
allure generate reports/allure-results -o reports/allure-report --clean
```

## Troubleshooting

### Issue: "allure: command not found"
**Solution**: Install Allure CLI
```bash
# Windows (with npm)
npm install -g allure-commandline

# Windows (with Scoop)
scoop install allure

# macOS
brew install allure
```

### Issue: Report doesn't show data
**Solution**: Ensure tests ran and generated results
```bash
# Check if results exist
ls -la reports/allure-results/

# Re-run tests if needed
pytest tests/test_TY2025_swagger_apis.py
```

### Issue: Old results showing in report
**Solution**: Clean results directory
```bash
# Clean and regenerate
allure generate reports/allure-results -o reports/allure-report --clean
```

## Advanced Usage

### Custom Environment Information
Create `reports/allure-results/environment.properties`:
```properties
Environment=DEVTR
Base.URL=https://devtr-api-iscrum.sureprep.com
Browser=N/A
Python.Version=3.13.5
Pytest.Version=9.0.2
```

### Categories Configuration
Create `reports/allure-results/categories.json`:
```json
[
  {
    "name": "Authentication Failures",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*authentication.*"
  },
  {
    "name": "Timeout Errors",
    "matchedStatuses": ["failed", "broken"],
    "messageRegex": ".*timed out.*"
  }
]
```

## Test Results Summary

### Latest Run
- **Total Tests**: 113
- **Passed**: 112 ✅
- **Failed**: 1 ❌ (Timeout issue)
- **Duration**: 147.79s (2m 27s)
- **Environment**: DEVTR

### Allure Features Added
- ✅ 113 test methods with `@allure.story()` decorators
- ✅ 113 test methods with `@allure.title()` decorators
- ✅ 113 test methods with `@allure.severity()` decorators
- ✅ Request/Response attachments for all tests
- ✅ Step-by-step execution details

## Quick Reference Commands

```bash
# Run tests and generate report
pytest tests/test_TY2025_swagger_apis.py && allure generate reports/allure-results -o reports/allure-report --clean

# Run tests and open report immediately
pytest tests/test_TY2025_swagger_apis.py && allure serve reports/allure-results

# View last report
allure open reports/allure-report
```

## Next Steps

1. Review the generated Allure report
2. Customize categories and environment info as needed
3. Integrate with CI/CD pipeline for automated reporting
4. Set up report archiving for historical trends

---

**Report Location**: [reports/allure-report/index.html](reports/allure-report/index.html)

**Documentation**: https://docs.qameta.io/allure/
