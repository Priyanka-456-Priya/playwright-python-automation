"""
Authentication Verification Script
Tests V5 and V7 API authentication with credentials from .env file
Supports multiple environments: devtr, qa, staging, prod
"""

import os
import sys
import requests
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# Load environment variables from .env file
project_root = Path(__file__).parent
env_file = project_root / '.env'

if not env_file.exists():
    print("\n[ERROR] No .env file found!")
    print("Please switch to an environment first using:")
    print("  python env_manager.py switch devtr")
    sys.exit(1)

load_dotenv(env_file, override=True)

# Configuration
BASE_URL = os.getenv('SUREPREP_BASE_URL', 'https://devtr-api-iscrum.sureprep.com')
V5_USERNAME = os.getenv('SUREPREP_V5_USERNAME')
V5_PASSWORD = os.getenv('SUREPREP_V5_PASSWORD')
V5_API_KEY = os.getenv('SUREPREP_V5_API_KEY')
V7_CLIENT_ID = os.getenv('SUREPREP_V7_CLIENT_ID')
V7_CLIENT_SECRET = os.getenv('SUREPREP_V7_CLIENT_SECRET')
TIMEOUT = 30


def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def print_result(status, message, details=None):
    """Print formatted result"""
    symbol = "[PASS]" if status == "SUCCESS" else "[FAIL]"
    print(f"\n{symbol} [{status}] {message}")
    if details:
        for key, value in details.items():
            print(f"  {key}: {value}")


def verify_v5_authentication():
    """Verify V5 API authentication"""
    print_header("Testing V5 API Authentication")

    auth_url = f"{BASE_URL}/V5.0/Authenticate/GetToken"
    payload = {
        "UserName": V5_USERNAME,
        "Password": V5_PASSWORD,
        "APIKey": V5_API_KEY
    }

    print(f"Endpoint: {auth_url}")
    print(f"Username: {V5_USERNAME}")
    print(f"API Key: {V5_API_KEY[:20]}...")

    try:
        response = requests.post(auth_url, json=payload, timeout=TIMEOUT)

        if response.status_code == 200:
            token = response.json().get('Token', '')
            if token:
                print_result("SUCCESS", "V5 Authentication Successful", {
                    "Status Code": response.status_code,
                    "Token Preview": f"{token[:30]}...",
                    "Token Length": len(token)
                })
                return True, token
            else:
                print_result("FAILED", "V5 Authentication Failed - Empty Token", {
                    "Status Code": response.status_code,
                    "Response": response.text
                })
                return False, None
        else:
            print_result("FAILED", "V5 Authentication Failed", {
                "Status Code": response.status_code,
                "Response": response.text[:200]
            })
            return False, None

    except Exception as e:
        print_result("ERROR", "V5 Authentication Error", {
            "Exception": str(e)
        })
        return False, None


def verify_v7_authentication():
    """Verify V7 API authentication"""
    print_header("Testing V7 API Authentication")

    auth_url = f"{BASE_URL}/V7/Authenticate/GetToken"
    payload = {
        "ClientID": V7_CLIENT_ID,
        "ClientSecret": V7_CLIENT_SECRET
    }

    print(f"Endpoint: {auth_url}")
    print(f"Client ID: {V7_CLIENT_ID[:20]}...")

    try:
        response = requests.post(auth_url, json=payload, timeout=TIMEOUT)

        if response.status_code == 200:
            token = response.json().get('Token', '')
            if token:
                print_result("SUCCESS", "V7 Authentication Successful", {
                    "Status Code": response.status_code,
                    "Token Preview": f"{token[:30]}...",
                    "Token Length": len(token)
                })
                return True, token
            else:
                print_result("FAILED", "V7 Authentication Failed - Empty Token", {
                    "Status Code": response.status_code,
                    "Response": response.text
                })
                return False, None
        else:
            print_result("FAILED", "V7 Authentication Failed", {
                "Status Code": response.status_code,
                "Response": response.text[:200]
            })
            return False, None

    except Exception as e:
        print_result("ERROR", "V7 Authentication Error", {
            "Exception": str(e)
        })
        return False, None


def main():
    """Main verification function"""
    current_env = os.getenv('TEST_ENVIRONMENT', 'Unknown').upper()

    print_header(f"SurePrep API Authentication Verification - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Environment: {current_env}")
    print(f"Base URL: {BASE_URL}")

    # Environment-specific warnings
    if current_env.lower() == 'prod':
        print("\n" + "!"*70)
        print("  WARNING: Testing against PRODUCTION environment!")
        print("  Please ensure you have proper authorization.")
        print("!"*70)

    # Verify credentials are loaded
    if not all([V5_USERNAME, V5_PASSWORD, V5_API_KEY, V7_CLIENT_ID, V7_CLIENT_SECRET]):
        print("\n[ERROR] Missing credentials in .env file!")
        print("Please ensure all required credentials are set:")
        print(f"  V5_USERNAME: {'Set' if V5_USERNAME else 'Missing'}")
        print(f"  V5_PASSWORD: {'Set' if V5_PASSWORD else 'Missing'}")
        print(f"  V5_API_KEY: {'Set' if V5_API_KEY else 'Missing'}")
        print(f"  V7_CLIENT_ID: {'Set' if V7_CLIENT_ID else 'Missing'}")
        print(f"  V7_CLIENT_SECRET: {'Set' if V7_CLIENT_SECRET else 'Missing'}")
        return

    # Test V5 authentication
    v5_success, v5_token = verify_v5_authentication()

    # Test V7 authentication
    v7_success, v7_token = verify_v7_authentication()

    # Summary
    print_header("Verification Summary")
    print(f"V5 Authentication: {'PASSED' if v5_success else 'FAILED'}")
    print(f"V7 Authentication: {'PASSED' if v7_success else 'FAILED'}")

    if v5_success and v7_success:
        print("\n[SUCCESS] All authentication tests passed!")
        print("You can now run your test suite with: pytest")
    else:
        print("\n[FAILED] Some authentication tests failed.")
        print("Please verify your credentials in the .env file.")


if __name__ == "__main__":
    main()
