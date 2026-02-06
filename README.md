# API Error Codes Validation - SurePrep API Test Suite

Comprehensive API testing suite for SurePrep API endpoints with Allure reporting integration. This project validates all API error codes and responses across 113 test cases covering authentication, binder operations, billing, document management, and more.

## 🚀 Features

- ✅ **113 Automated Test Cases** - Complete coverage of SurePrep API endpoints
- ✅ **Allure Reporting** - Rich, interactive HTML reports with request/response details
- ✅ **Multi-Environment Support** - DEVTR, QA, Production environments
- ✅ **Dual Authentication** - Support for both V5 and V7 API authentication
- ✅ **Request/Response Logging** - Detailed logging of all API interactions
- ✅ **Error Code Validation** - Comprehensive validation of HTTP status codes
- ✅ **CI/CD Ready** - Easy integration with GitHub Actions or Jenkins

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Allure Reports](#allure-reports)
- [Test Coverage](#test-coverage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🔧 Prerequisites

- Python 3.13+
- pip (Python package manager)
- Git
- Allure CLI (for report generation)

### Installing Allure CLI

**Windows:**
```bash
# Using npm
npm install -g allure-commandline

# Using Scoop
scoop install allure
```

**macOS:**
```bash
brew install allure
```

**Linux:**
```bash
# Download and install from https://github.com/allure-framework/allure2/releases
```

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Priyanka-456-Priya/playwright-python-automation.git
   cd API_Error_Codes_Validation
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

### Environment Variables

Set up environment variables for different environments:

```bash
# DEVTR Environment (default)
export SUREPREP_BASE_URL="https://devtr-api-iscrum.sureprep.com"

# V5 Credentials
export SUREPREP_V5_USERNAME="your_username"
export SUREPREP_V5_PASSWORD="your_password"
export SUREPREP_V5_API_KEY="your_api_key"

# V7 Credentials
export SUREPREP_V7_CLIENT_ID="your_client_id"
export SUREPREP_V7_CLIENT_SECRET="your_client_secret"
```

### Configuration Files

- **pytest.ini** - Pytest configuration with Allure settings
- **data/test_data.json** - Test data and expected responses
- **.env** (create this) - Environment-specific credentials

## 🧪 Running Tests

### Run All Tests
```bash
pytest tests/test_TY2025_swagger_apis.py
```

### Run with Verbose Output
```bash
pytest tests/test_TY2025_swagger_apis.py -v
```

### Run Specific Test
```bash
pytest tests/test_TY2025_swagger_apis.py::TestSwaggerAPIs::test_v5_0_authenticate_gettoken_1
```

### Run by Marker
```bash
# Run only authentication tests
pytest tests/test_TY2025_swagger_apis.py -m authentication

# Run only critical tests
pytest tests/test_TY2025_swagger_apis.py -m "severity:critical"
```

### Parallel Execution
```bash
# Install pytest-xdist first
pip install pytest-xdist

# Run tests in parallel
pytest tests/test_TY2025_swagger_apis.py -n auto
```

## 📊 Allure Reports

### Generate Report
```bash
# Run tests (results saved to reports/allure-results/)
pytest tests/test_TY2025_swagger_apis.py

# Generate HTML report
allure generate reports/allure-results -o reports/allure-report --clean

# Open report in browser
allure open reports/allure-report
```

### One-Liner: Run and View
```bash
pytest tests/test_TY2025_swagger_apis.py && allure serve reports/allure-results
```

### Report Features

- **Dashboard** - Test execution overview with charts
- **Suites** - All test cases organized by class
- **Graphs** - Status, severity, and duration visualizations
- **Timeline** - Execution timeline view
- **Behaviors** - Tests grouped by features and stories
- **Packages** - Test organization by package structure
- **Attachments** - Request/response details for each test

## 📈 Test Coverage

### API Endpoints Covered

| Category | Test Count | Severity |
|----------|------------|----------|
| Authentication | 2 | CRITICAL |
| Binder Operations | 45 | CRITICAL |
| Billing | 12 | NORMAL |
| Document Management | 15 | NORMAL |
| TaxCaddy API | 18 | NORMAL |
| DRL Operations | 8 | NORMAL |
| UT Integration | 10 | NORMAL |
| Lookup Services | 3 | NORMAL |
| **Total** | **113** | - |

### Status Code Coverage

- ✅ 200 OK
- ✅ 201 Created
- ✅ 400 Bad Request
- ✅ 401 Unauthorized
- ✅ 404 Not Found
- ✅ 405 Method Not Allowed
- ✅ 500 Internal Server Error

## 📁 Project Structure

```
API_Error_Codes_Validation/
├── tests/
│   └── test_TY2025_swagger_apis.py    # Main test suite (113 tests)
├── data/
│   └── test_data.json                  # Test data and expected responses
├── reports/
│   ├── allure-results/                 # Allure JSON results
│   └── allure-report/                  # Generated HTML report
├── utils/                              # Utility functions (if any)
├── add_allure_decorators.py           # Script to add Allure decorators
├── pytest.ini                          # Pytest configuration
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Git ignore rules
├── README.md                           # This file
└── ALLURE_REPORTING_GUIDE.md          # Detailed Allure guide
```

## 🔍 Test Structure

Each test includes:
- **Test ID** - Unique test case number (TC_001 to TC_113)
- **Endpoint** - API endpoint being tested
- **HTTP Method** - POST, GET, PUT, DELETE
- **Payload** - Request body/parameters
- **Expected Response** - Expected status code and response structure
- **Allure Annotations**:
  - `@allure.feature()` - Feature category
  - `@allure.story()` - Test story/group
  - `@allure.title()` - Test case title
  - `@allure.severity()` - Test importance
  - Request/Response attachments

## 📝 Example Test

```python
@allure.story("Authentication")
@allure.title("TC_001: POST /V5.0/Authenticate/GetToken")
@allure.description("Test authentication endpoint with invalid credentials")
@allure.severity(allure.severity_level.CRITICAL)
def test_v5_0_authenticate_gettoken_1(self):
    """TC_001: Test post /V5.0/Authenticate/GetToken"""
    url = f"{TestConfig.BASE_URL}/V5.0/Authenticate/GetToken"
    endpoint = "/V5.0/Authenticate/GetToken"

    payload = {
        "UserName": "PRIYA",
        "Password": "Abcd@12345",
        "APIKey": "24CDFF63-782A-4382-9F4B-0272C03ED095"
    }

    response = self.make_request(
        method='POST',
        url=url,
        payload=payload,
        api_version="v5"
    )

    self.display_test_result(endpoint, 'POST', response, payload)

    assert response.status_code == 401
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 Requirements

```txt
pytest==9.0.2
requests==2.31.0
allure-pytest==2.15.3
pytest-html==4.2.0
pytest-metadata==3.1.1
```

## 🛠️ Troubleshooting

### Common Issues

**1. Authentication Failures**
- Verify environment variables are set correctly
- Check if credentials are valid for the target environment
- Ensure API keys are not expired

**2. Timeout Errors**
- Increase timeout in `TestConfig.TIMEOUT` (default: 30s)
- Check network connectivity
- Verify API endpoint is accessible

**3. Allure Report Not Generating**
- Ensure Allure CLI is installed: `allure --version`
- Check if `reports/allure-results/` contains JSON files
- Try regenerating: `allure generate reports/allure-results -o reports/allure-report --clean`

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check [ALLURE_REPORTING_GUIDE.md](ALLURE_REPORTING_GUIDE.md) for detailed Allure documentation

## 📜 License

This project is part of the SurePrep API testing initiative.

## 🎯 Future Enhancements

- [ ] CI/CD pipeline integration (GitHub Actions)
- [ ] Performance testing with load tests
- [ ] API mocking for offline testing
- [ ] Automated test data generation
- [ ] Integration with test management tools
- [ ] Support for additional environments

---

**Last Updated**: February 2026
**Test Suite Version**: TY2025
**Total Tests**: 113
**Python Version**: 3.13+
