# Quick Reference Guide

## What Was Done

All **114 test methods** in [test_auto_generated_swagger_apis.py](tests/test_auto_generated_swagger_apis.py) now display:
- **INPUT**: Endpoint, method, and payload sent
- **ACTUAL OUTPUT**: Status code and response received
- **EXPECTED OUTPUT**: Expected results from [test_data.json](data/test_data.json)

## Running Tests

### View Output for One Test
```bash
pytest tests/test_auto_generated_swagger_apis.py::TestSwaggerAPIs::test_v7_authenticate_gettoken_2 -v -s
```

### Run Multiple Tests
```bash
pytest tests/test_auto_generated_swagger_apis.py -k "authenticate" -v -s
```

### Run All Tests
```bash
pytest tests/test_auto_generated_swagger_apis.py -v -s
```

### Generate HTML Report
```bash
pytest tests/test_auto_generated_swagger_apis.py -v -s --html=reports/results.html
```

**Note:** Always use `-s` flag to see the detailed output!

## Sample Output

```
================================================================================
TEST RESULT FOR: POST /V5.0/BinderInfo/GetBinderDetails
================================================================================

INPUT:
  Endpoint: /V5.0/BinderInfo/GetBinderDetails
  Method: POST
  Payload: {
    "TaxYear": 2025,
    "ClientID": ["2025UT7"],
    "BinderType": "1040",
    "OwnerEmail": "user@example.com"
  }

ACTUAL OUTPUT:
  Status Code: 401
  Response Body (Text): token not present in request

EXPECTED OUTPUT (from test_data.json):
  Expected Status Code: 401
  Description: Request without authentication token
================================================================================
```

## Key Features

✓ **Automatic Matching** - Finds expected output based on status code and endpoint
✓ **Clear Format** - Easy to read and understand
✓ **JSON Pretty Print** - Response bodies are formatted nicely
✓ **Error Handling** - Works with both JSON and text responses
✓ **Comprehensive** - Shows complete request/response cycle

## Customizing Expected Outputs

Edit [data/test_data.json](data/test_data.json) to add more expected outputs:

```json
{
  "test_scenarios": {
    "401_unauthorized": {
      "no_auth_token": {
        "description": "Request without authentication token",
        "endpoints": [
          {
            "path": "/V5.0/BinderInfo/GetBinderDetails",
            "method": "POST"
          }
        ]
      }
    }
  }
}
```

## Files Changed

- **[tests/test_auto_generated_swagger_apis.py](tests/test_auto_generated_swagger_apis.py)** - All 114 tests updated

## Documentation

- **[UPDATE_COMPLETE.md](UPDATE_COMPLETE.md)** - Complete update summary
- **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)** - Detailed technical changes
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - This file

## Support Scripts

- **[bulk_update_tests.py](bulk_update_tests.py)** - Script that performed the updates
- **[update_all_tests.py](update_all_tests.py)** - Helper instructions
