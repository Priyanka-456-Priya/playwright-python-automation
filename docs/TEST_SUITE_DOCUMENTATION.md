# Auto-Generated Swagger API Test Suite Documentation

## Overview
This test suite was automatically generated from your Swagger API specification Excel file containing 113 API endpoints.

## Test Suite Details

### Total Coverage
- **Total API Endpoints**: 113
- **API Versions Covered**: V5.0, V6.0, V7
- **Test Framework**: pytest
- **Report Format**: HTML (self-contained)

### API Categories Covered

1. **Authentication APIs**
   - V5.0/Authenticate/GetToken
   - V7/Authenticate/GetToken

2. **BinderInfo APIs**
   - GetBinderDetails
   - GetUnclearedNotes
   - GetUnreviewedTRStamps
   - GetUnreviewedStickyNotes
   - GetUnreviewedWorkpapersByL1/L2/L3/L4
   - GetDocumentPendingReviewCount
   - GetDocumentPendingSignatureCount
   - GetDocumentPendingUploadCount
   - GetBinderPendingItems

3. **Binder APIs**
   - CreateBinder
   - SubmitBinder
   - UploadBinderDocuments
   - UpdateProjectID
   - GetStatesandLocalities
   - GetBindersStatusWithStates
   - DownloadBinderPBFX
   - GetBinderAuditLog
   - UpdateOwnerMember
   - PrintBinder

4. **Document APIs**
   - GetDocuments
   - DownloadDocument

5. **Lookup APIs**
   - GetLocalPathToDownloadFiles
   - ServiceTypes
   - OfficeLocations
   - BinderTypes
   - TaxSoftwareList
   - BinderTemplates
   - BinderStatusList
   - ServiceUnits
   - DomainInformation
   - UserDomainDetails
   - CustomFieldEnabled

6. **Status APIs**
   - GetStatus
   - ChangeBinderStatus

7. **TaxCaddy APIs**
   - CreateClient
   - CreateDrl
   - GetClientDetails
   - DomainSubscribe/Unsubscribe
   - ClientSubscribe/Unsubscribe
   - DownloadDocument
   - GetDRLStatus
   - SendDRL
   - DisconnectDevices
   - SendQuestionnaire
   - PrintQuestionnaire
   - GetMemberDetails
   - UpdateMember

8. **Review Wizard APIs**
   - LaunchReviewWizard

9. **UT Integration APIs**
   - DRLCallBack
   - BinderCallBack
   - TaxFileMergedStatus
   - SPConnect

## Configuration

### Base URL
```
https://devtr-api-iscrum.sureprep.com
```

### V5 Credentials
- **Username**: PRIYA1
- **Password**: Abcd@12345
- **API Key**: C690222D-8625-46F7-92CC-A61DA060D7A9

### V7 Credentials
- **Client ID**: GxJQo22jTg9koTeDtbIHpg8nmWdns9cu
- **Client Secret**: yZdKNGi2b-Fsp1uWZllPnST7VM2PdSc3hDC4_rZ5tfGektIltwkfYPLLDEGD6f_M

## Test Execution

### Running Tests

#### Option 1: Using Batch Script (Recommended)
```batch
run_swagger_tests.bat
```

#### Option 2: Using pytest Directly
```bash
# Activate virtual environment
call venv\Scripts\activate.bat

# Set environment variables
set SUREPREP_BASE_URL=https://devtr-api-iscrum.sureprep.com
set SUREPREP_V5_USERNAME=PRIYA1
set SUREPREP_V5_PASSWORD=Abcd@12345
set SUREPREP_V5_API_KEY=C690222D-8625-46F7-92CC-A61DA060D7A9
set SUREPREP_V7_CLIENT_ID=GxJQo22jTg9koTeDtbIHpg8nmWdns9cu
set SUREPREP_V7_CLIENT_SECRET=yZdKNGi2b-Fsp1uWZllPnST7VM2PdSc3hDC4_rZ5tfGektIltwkfYPLLDEGD6f_M

# Run tests
pytest tests\test_auto_generated_swagger_apis.py -v --html=reports\swagger_api_test_report.html --self-contained-html
```

### Test Features

1. **Automatic Authentication**
   - Tests automatically obtain V5 and V7 authentication tokens
   - Tokens are reused across all test cases in the session
   - No manual token management required

2. **Input Validation**
   - Each test uses the exact input parameters from your Excel file
   - Payload validation against API specifications

3. **Output Validation**
   - Response status code validation (200, 201, 400, 401, 404)
   - Response structure validation
   - Error code and message validation
   - Field presence validation

4. **Comprehensive Reporting**
   - HTML report with pass/fail status for each API
   - Detailed error messages for failed tests
   - Request/response logging
   - Execution time tracking

## Report Location

After test execution, reports are generated in:
```
reports/swagger_api_test_report_<timestamp>.html
```

The report includes:
- Overall test summary (passed/failed/skipped)
- Individual test results with details
- Request/response data for debugging
- Execution time for each test
- Failure stack traces (if any)

## File Structure

```
API_Error_Codes_Validation/
├── testData/
│   └── swagger_apis.json                    # Parsed API specifications
├── tests/
│   └── test_auto_generated_swagger_apis.py  # Auto-generated test suite (113 tests)
├── scripts/
│   ├── parse_excel_to_json.py              # Excel parser
│   └── generate_test_suite.py              # Test generator
├── reports/
│   └── swagger_api_test_report_*.html      # Test reports
├── docs/
│   └── TEST_SUITE_DOCUMENTATION.md         # This file
└── run_swagger_tests.bat                    # Test execution script
```

## Test Case Naming Convention

Each test case follows this naming pattern:
```python
test_<api_endpoint>_<index>
```

Examples:
- `test_v5_0_authenticate_gettoken_1`
- `test_v7_authenticate_gettoken_2`
- `test_v5_0_binderinfo_getbinderdetails_3`

## Assertions in Tests

Each test performs the following validations:

1. **Status Code Validation**
   ```python
   assert response.status_code in [200, 201, 400, 401, 404]
   ```

2. **Response Structure Validation**
   - Validates response is valid JSON
   - Checks for expected fields
   - Validates data types

3. **Error Handling**
   - Validates error responses contain ErrorCode and ErrorMessage
   - Ensures appropriate error codes are returned

## Updating Tests

### To Add New APIs
1. Update the Excel file with new API endpoints
2. Run the parser:
   ```bash
   python scripts/parse_excel_to_json.py
   ```
3. Regenerate tests:
   ```bash
   python scripts/generate_test_suite.py
   ```
4. Run the updated test suite

### To Modify Credentials
Edit the `run_swagger_tests.bat` file or set environment variables:
```batch
set SUREPREP_V5_USERNAME=<new_username>
set SUREPREP_V5_PASSWORD=<new_password>
set SUREPREP_V7_CLIENT_ID=<new_client_id>
set SUREPREP_V7_CLIENT_SECRET=<new_secret>
```

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Verify credentials are correct
   - Check if tokens have expired
   - Ensure base URL is accessible

2. **Import Errors**
   - Ensure virtual environment is activated
   - Install required packages: `pip install -r requirements.txt`

3. **Test Failures**
   - Check the HTML report for detailed error messages
   - Verify API endpoints are accessible
   - Ensure test data is valid

### Debug Mode

Run tests with verbose output:
```bash
pytest tests\test_auto_generated_swagger_apis.py -vv -s
```

## Continuous Integration

This test suite can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run API Tests
  run: |
    call venv\Scripts\activate.bat
    pytest tests\test_auto_generated_swagger_apis.py --html=reports/api_tests.html
```

## Contact & Support

For issues or questions about this test suite:
- Check the HTML report for detailed error information
- Review the test file: `tests/test_auto_generated_swagger_apis.py`
- Examine logs in the `logs/` directory

---

**Generated on**: January 15, 2026
**Total Test Cases**: 113
**API Versions**: V5.0, V6.0, V7
