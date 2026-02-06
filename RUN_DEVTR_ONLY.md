# How to Run Tests ONLY for Devtr Environment

This guide shows multiple ways to ensure your tests run exclusively in the Devtr environment.

---

## Method 1: Dedicated Test Runner (Recommended) ✅

### Using Python Script
```bash
# Run all tests in Devtr (auto-switches if needed)
python run_devtr_tests.py

# Run with specific pytest arguments
python run_devtr_tests.py -v
python run_devtr_tests.py -k "test_authenticate"
python run_devtr_tests.py tests/test_TY2025_swagger_apis.py
python run_devtr_tests.py -m smoke
```

### Using Windows Batch File
```bash
# Simple run
run_devtr_tests.bat

# With arguments
run_devtr_tests.bat -v
run_devtr_tests.bat -k "test_v7"
```

### What This Does:
- ✅ Automatically checks if Devtr is active
- ✅ Switches to Devtr if needed
- ✅ Verifies authentication before running tests
- ✅ Runs tests only in Devtr environment
- ✅ Provides clear success/failure messages

---

## Method 2: Manual Environment Switch

```bash
# Step 1: Check current environment
python env_manager.py current

# Step 2: Switch to Devtr
python env_manager.py switch devtr

# Step 3: Verify authentication
python verify_auth.py

# Step 4: Run tests
pytest
pytest -v
pytest tests/test_TY2025_swagger_apis.py
```

---

## Method 3: Environment Markers (Prevent Tests from Running in Other Environments)

Mark specific tests to run ONLY in Devtr:

### Example 1: Single Test
```python
import pytest

@pytest.mark.env('devtr')
def test_devtr_only_feature():
    """This test will ONLY run in Devtr environment"""
    # Your test code
    pass
```

### Example 2: Test Class
```python
import pytest

@pytest.mark.env('devtr')
class TestDevtrOnlyFeatures:
    """All tests in this class run only in Devtr"""

    def test_feature_1(self):
        pass

    def test_feature_2(self):
        pass
```

### Example 3: Multiple Environments
```python
@pytest.mark.env('devtr', 'qa')  # Runs in Devtr OR QA
def test_safe_for_devtr_and_qa():
    """This runs in Devtr and QA, but NOT staging/prod"""
    pass
```

### How It Works:
- Tests with `@pytest.mark.env('devtr')` automatically **skip** in other environments
- Configured in [tests/conftest.py](tests/conftest.py) (already set up)

---

## Method 4: Conditional Test Logic

Use environment fixtures to skip tests programmatically:

```python
import pytest

def test_something(environment):
    """Test that checks environment before executing"""

    # Skip if not Devtr
    if environment['key'] != 'devtr':
        pytest.skip("This test only runs in Devtr")

    # Your test code here
    assert environment['url'] == 'https://devtr-api-iscrum.sureprep.com'
```

---

## Method 5: Environment Verification Before Tests

Create a conftest.py hook to block tests in wrong environment:

### Add to tests/conftest.py:
```python
def pytest_sessionstart(session):
    """Block tests if not in Devtr environment"""
    import os
    from dotenv import load_dotenv
    from pathlib import Path

    project_root = Path(__file__).parent.parent
    env_file = project_root / '.env'

    if env_file.exists():
        load_dotenv(env_file)
        current_env = os.getenv('TEST_ENVIRONMENT', '').lower()

        # Block tests if not Devtr
        if current_env != 'devtr':
            pytest.exit(
                f"Tests blocked: Current environment is '{current_env}', not 'devtr'. "
                f"Switch to Devtr with: python env_manager.py switch devtr",
                returncode=1
            )
```

---

## Comparison of Methods

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Dedicated Script** | Automatic, safest, includes auth check | Extra script | Daily use, CI/CD |
| **Manual Switch** | Full control, transparent | Manual steps | Understanding flow |
| **Markers** | Granular control per test | Need to mark each test | Specific test isolation |
| **Conditional Logic** | Flexible, runtime checks | More code in tests | Complex scenarios |
| **Session Block** | Blocks all tests if wrong env | All-or-nothing | Strict enforcement |

---

## Quick Commands Reference

### Dedicated Test Runner
```bash
python run_devtr_tests.py              # Run all Devtr tests
python run_devtr_tests.py -v           # Verbose
python run_devtr_tests.py -k "auth"    # Run tests matching "auth"
python run_devtr_tests.py --maxfail=1  # Stop after first failure
```

### Environment Management
```bash
python env_manager.py current          # Check environment
python env_manager.py switch devtr     # Switch to Devtr
python env_manager.py verify devtr     # Verify Devtr config
python verify_auth.py                  # Test authentication
```

### Direct Pytest (After Switching to Devtr)
```bash
pytest                                 # Run all tests
pytest -v                              # Verbose output
pytest -s                              # Show print statements
pytest -k "authenticate"               # Run tests matching pattern
pytest tests/test_TY2025_swagger_apis.py  # Specific file
pytest --maxfail=1                     # Stop after first fail
pytest -m smoke                        # Run smoke tests only
```

---

## Example Workflows

### Workflow 1: Quick Test Run
```bash
# One command - handles everything!
python run_devtr_tests.py -v
```

### Workflow 2: Specific Test File
```bash
# Run specific test file in Devtr
python run_devtr_tests.py tests/test_TY2025_swagger_apis.py -v
```

### Workflow 3: Test Matching Pattern
```bash
# Run all authentication tests in Devtr
python run_devtr_tests.py -k "authenticate" -v
```

### Workflow 4: Manual Control
```bash
# Full manual control
python env_manager.py switch devtr
python verify_auth.py
pytest -v -s
```

---

## Safety Features

The dedicated test runner ([run_devtr_tests.py](run_devtr_tests.py)) includes:

✅ **Auto Environment Check** - Verifies Devtr is active
✅ **Auto Environment Switch** - Switches to Devtr if needed
✅ **Authentication Verification** - Tests auth before running tests
✅ **Clear Status Messages** - Shows what's happening at each step
✅ **Exit Codes** - Proper exit codes for CI/CD integration

---

## Troubleshooting

### Issue: "Current environment is 'qa', not 'devtr'"
```bash
# Solution: Use the dedicated runner (auto-switches)
python run_devtr_tests.py

# Or manually switch
python env_manager.py switch devtr
```

### Issue: Authentication Failed
```bash
# Solution: Verify Devtr credentials
python env_manager.py verify devtr
python verify_auth.py
```

### Issue: Tests Running in Wrong Environment
```bash
# Solution: Check active environment
python env_manager.py current

# Expected output: "Currently active environment: DEVTR"
```

---

## Files Created for Devtr-Only Testing

| File | Purpose |
|------|---------|
| [run_devtr_tests.py](run_devtr_tests.py) | Python script for Devtr-only testing |
| [run_devtr_tests.bat](run_devtr_tests.bat) | Windows batch file for easy execution |
| [.env.devtr](.env.devtr) | Devtr environment credentials |
| [RUN_DEVTR_ONLY.md](RUN_DEVTR_ONLY.md) | This guide |

---

## Summary

**Simplest Method (Recommended):**
```bash
python run_devtr_tests.py
```

This single command:
- ✅ Checks if Devtr is active
- ✅ Switches to Devtr if needed
- ✅ Verifies authentication
- ✅ Runs all tests
- ✅ Reports results

**No manual steps needed!** 🎉

---

## Additional Resources

- [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) - Complete multi-environment guide
- [ENV_QUICK_REFERENCE.md](ENV_QUICK_REFERENCE.md) - Quick command reference
- [MULTI_ENV_SETUP_COMPLETE.md](MULTI_ENV_SETUP_COMPLETE.md) - Setup summary
