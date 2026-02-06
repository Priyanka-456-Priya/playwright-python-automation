"""
Pytest configuration file for loading environment variables and shared fixtures.
This file is automatically loaded by pytest before running tests.
"""

import os
import sys
import pytest
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Environment configuration mapping
ENVIRONMENT_MAPPING = {
    'devtr': {
        'name': 'Development/Test',
        'url': 'https://devtr-api-iscrum.sureprep.com',
        'safe': True
    },
    'qa': {
        'name': 'Quality Assurance',
        'url': 'https://qa-api-iscrum.sureprep.com',
        'safe': True
    },
    'staging': {
        'name': 'Staging',
        'url': 'https://staging-api-iscrum.sureprep.com',
        'safe': True
    },
    'prod': {
        'name': 'Production',
        'url': 'https://api-iscrum.sureprep.com',
        'safe': False
    }
}


def get_environment_info():
    """Get current environment information"""
    env_file = project_root / '.env'

    if not env_file.exists():
        return None, None

    load_dotenv(env_file, override=True)
    test_env = os.getenv('TEST_ENVIRONMENT', 'unknown').lower()

    return test_env, ENVIRONMENT_MAPPING.get(test_env, {'name': 'Unknown', 'url': 'Unknown', 'safe': True})


def print_environment_banner():
    """Print environment configuration banner"""
    env_key, env_info = get_environment_info()

    if not env_key:
        print(f"\n{'='*70}")
        print("  WARNING: No .env file found!")
        print("  Using default hardcoded credentials from TestConfig")
        print("  Run: python env_manager.py switch devtr")
        print(f"{'='*70}\n")
        return

    print(f"\n{'='*70}")
    print(f"  PYTEST SESSION STARTED")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    print(f"  Environment: {env_key.upper()} ({env_info['name']})")
    print(f"  Base URL: {os.getenv('SUREPREP_BASE_URL', 'Not set')}")
    print(f"  V5 User: {os.getenv('SUREPREP_V5_USERNAME', 'Not set')}")

    v7_client_id = os.getenv('SUREPREP_V7_CLIENT_ID', 'Not set')
    if v7_client_id != 'Not set' and len(v7_client_id) > 20:
        print(f"  V7 Client: {v7_client_id[:20]}...")
    else:
        print(f"  V7 Client: {v7_client_id}")

    # Production warning
    if not env_info.get('safe', True):
        print(f"  {'='*70}")
        print("  WARNING: RUNNING TESTS AGAINST PRODUCTION!")
        print("  Please ensure you have proper authorization.")
        print(f"  {'='*70}")

    print(f"{'='*70}\n")


# Load environment variables
env_file = project_root / '.env'
if env_file.exists():
    load_dotenv(env_file, override=True)
    print_environment_banner()
else:
    print_environment_banner()


# Pytest hooks
def pytest_configure(config):
    """Pytest configuration hook"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on specific environment"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on environment"""
    current_env = os.getenv('TEST_ENVIRONMENT', '').lower()

    for item in items:
        # Check if test has environment marker
        env_marker = item.get_closest_marker('env')
        if env_marker:
            # Get required environments from marker
            required_envs = env_marker.args
            if current_env not in required_envs:
                item.add_marker(
                    pytest.mark.skip(
                        reason=f"Test only runs on {', '.join(required_envs)} (current: {current_env})"
                    )
                )


@pytest.fixture(scope='session')
def environment():
    """Fixture to provide current environment information"""
    env_key, env_info = get_environment_info()
    return {
        'key': env_key,
        'name': env_info['name'] if env_info else 'Unknown',
        'url': os.getenv('SUREPREP_BASE_URL'),
        'safe': env_info.get('safe', True) if env_info else True
    }


@pytest.fixture(scope='session')
def test_data_path():
    """Fixture to provide environment-specific test data path"""
    env_key = os.getenv('TEST_ENVIRONMENT', 'devtr').lower()

    # Check both 'data' and 'test_data' directories for backwards compatibility
    data_dir = project_root / 'data'
    test_data_dir = project_root / 'test_data'

    # Try environment-specific test data first in 'data' directory
    env_test_data = data_dir / f'test_data_{env_key}.json'
    if env_test_data.exists():
        print(f"[INFO] Using environment-specific test data: {env_test_data}")
        return env_test_data

    # Try 'test_data' directory for backwards compatibility
    env_test_data_alt = test_data_dir / f'test_data_{env_key}.json'
    if env_test_data_alt.exists():
        print(f"[INFO] Using environment-specific test data: {env_test_data_alt}")
        return env_test_data_alt

    # Fall back to default test data in 'data' directory
    default_test_data = data_dir / 'test_data.json'
    if default_test_data.exists():
        print(f"[WARNING] Environment-specific test data not found. Using default: {default_test_data}")
        return default_test_data

    # Final fallback to 'test_data' directory
    default_test_data_alt = test_data_dir / 'test_data.json'
    print(f"[WARNING] Using fallback test data: {default_test_data_alt}")
    return default_test_data_alt


@pytest.fixture(scope='session')
def test_data(test_data_path):
    """Fixture to load and provide test data as dictionary"""
    import json

    try:
        with open(test_data_path, 'r') as f:
            data = json.load(f)
        print(f"[SUCCESS] Test data loaded from: {test_data_path}")

        # Display environment info if available
        if 'environment' in data:
            print(f"[INFO] Test data environment: {data.get('environment_name', data['environment'])}")

        return data
    except FileNotFoundError:
        print(f"[WARNING] Test data file not found: {test_data_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in test data file: {e}")
        return {}
    except Exception as e:
        print(f"[ERROR] Failed to load test data: {e}")
        return {}
