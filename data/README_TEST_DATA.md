# Environment-Specific Test Data Guide

## Overview
This directory contains test data files that can be customized for different environments (devtr, qa, staging, prod).

## File Structure

```
data/
├── test_data.json                  # Default test data (used if environment-specific file not found)
├── test_data_devtr.json           # Devtr environment test data
├── test_data_qa.json              # QA environment test data
├── test_data_staging.json         # Staging environment test data
├── test_data_prod.json            # Production environment test data (use with caution)
└── README_TEST_DATA.md            # This file
```

## How It Works

The test framework (via `conftest.py`) automatically loads environment-specific test data based on the active environment:

1. It checks for `test_data_{environment}.json` (e.g., `test_data_qa.json`)
2. If not found, it falls back to `test_data.json`

## Creating Environment-Specific Test Data

### Option 1: Full Customization
Create separate test data files for each environment with different:
- Test user IDs
- Binder IDs
- Document IDs
- Resource identifiers

Example:
```bash
# Copy default test data to create environment-specific version
cp test_data.json test_data_qa.json
# Then edit test_data_qa.json with QA-specific IDs
```

### Option 2: Environment-Specific Overrides
Use the same structure but customize values that differ between environments:

**test_data_devtr.json:**
```json
{
  "common_test_ids": {
    "valid_binder_id": "12345",
    "valid_user_id": "test_user_devtr",
    "valid_domain_id": 100
  },
  "test_scenarios": {
    ...
  }
}
```

**test_data_prod.json:**
```json
{
  "common_test_ids": {
    "valid_binder_id": "67890",
    "valid_user_id": "prod_readonly_user",
    "valid_domain_id": 200
  },
  "test_scenarios": {
    ...
  }
}
```

## Best Practices

### 1. Environment Isolation
- **Devtr/QA**: Use test data freely, can be destructive
- **Staging**: Use production-like data, but non-critical
- **Production**: Use ONLY read-only operations, real IDs

### 2. Data Safety
```json
{
  "environments": {
    "devtr": {
      "allow_destructive_tests": true,
      "test_data_type": "synthetic"
    },
    "prod": {
      "allow_destructive_tests": false,
      "test_data_type": "real"
    }
  }
}
```

### 3. Test Data Categories

#### Safe for All Environments:
- Authentication tests (401, 403)
- Input validation tests (400, 422)
- Method not allowed tests (405)
- Rate limiting tests (429)

#### Use with Caution in Production:
- GET requests with valid IDs
- Status checks
- Health checks

#### NEVER in Production:
- POST/PUT/DELETE operations
- Bulk operations
- Stress tests
- Performance tests with high load

## Example: Environment-Specific Test Data

### test_data_devtr.json
```json
{
  "common_test_ids": {
    "valid_binder_id": "test_binder_123",
    "invalid_binder_id": "invalid_999",
    "test_user_email": "test@devtr.example.com"
  },
  "load_test": {
    "enabled": true,
    "concurrent_users": 100
  }
}
```

### test_data_prod.json
```json
{
  "common_test_ids": {
    "valid_binder_id": "prod_readonly_binder_456",
    "invalid_binder_id": "guaranteed_nonexistent_999",
    "test_user_email": "monitoring@prod.example.com"
  },
  "load_test": {
    "enabled": false,
    "concurrent_users": 5
  }
}
```

## Usage in Tests

### Accessing Test Data in Your Tests:

```python
import pytest
import json

@pytest.fixture
def test_data(test_data_path):
    """Load environment-specific test data"""
    with open(test_data_path, 'r') as f:
        return json.load(f)

def test_example(test_data, environment):
    """Example test using environment-specific data"""
    binder_id = test_data['common_test_ids']['valid_binder_id']

    # Skip destructive tests in production
    if environment['key'] == 'prod':
        pytest.skip("Destructive test - skipping in production")

    # Your test code here
    pass
```

### Environment-Conditional Tests:

```python
import pytest

@pytest.mark.env('devtr', 'qa')  # Only run in devtr and qa
def test_destructive_operation():
    # This test will be skipped in staging and prod
    pass

@pytest.mark.env('devtr')  # Only run in devtr
def test_dev_only_feature():
    # This test will be skipped in all other environments
    pass
```

## Switching Between Environments

```bash
# Switch to QA environment
python env_manager.py switch qa

# Run tests (will automatically use test_data_qa.json if it exists)
pytest

# Verify which environment is active
python env_manager.py current
```

## Security Notes

- ⚠️ Never commit real production data to version control
- ⚠️ Use sanitized/anonymized data for non-prod environments
- ⚠️ Keep production test data minimal and read-only
- ✅ Use synthetic data for dev/qa/staging when possible
- ✅ Document what data is safe to use in each environment
