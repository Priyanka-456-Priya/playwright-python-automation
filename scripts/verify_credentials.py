"""
Credential Verification Script for Sureprep API
This script tests V5 and V7 authentication endpoints to verify credentials are working
"""

import requests
import json
from datetime import datetime


class CredentialVerifier:
    """Verify Sureprep API credentials"""

    def __init__(self):
        self.base_url = "https://api.sureprep.com"
        self.results = {
            "v5": {"status": "Not Tested", "token": None, "error": None},
            "v7": {"status": "Not Tested", "token": None, "error": None}
        }

    def verify_v5_credentials(self, username, password, api_key):
        """Verify V5.0 API credentials"""
        print("\n" + "=" * 60)
        print("Testing V5.0 API Credentials")
        print("=" * 60)

        url = f"{self.base_url}/V5.0/Authenticate/GetToken"
        payload = {
            "UserName": username,
            "Password": password,
            "APIKey": api_key
        }

        print(f"\nEndpoint: {url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")

        try:
            response = requests.post(url, json=payload, timeout=30)
            print(f"\nStatus Code: {response.status_code}")

            if response.status_code == 200:
                token_data = response.json()
                token = token_data.get('token', '')
                print(f"[OK] SUCCESS: Token received")
                print(f"Token (first 50 chars): {token[:50]}...")
                self.results["v5"]["status"] = "[OK] PASSED"
                self.results["v5"]["token"] = token[:50] + "..."
                return True
            else:
                error_msg = response.text
                print(f"[FAIL] FAILED: {error_msg}")
                self.results["v5"]["status"] = "[FAIL] FAILED"
                self.results["v5"]["error"] = f"Status {response.status_code}"
                return False

        except requests.exceptions.Timeout:
            print("[FAIL] FAILED: Request timed out")
            self.results["v5"]["status"] = "[FAIL] FAILED"
            self.results["v5"]["error"] = "Timeout"
            return False
        except Exception as e:
            print(f"[FAIL] FAILED: {str(e)}")
            self.results["v5"]["status"] = "[FAIL] FAILED"
            self.results["v5"]["error"] = str(e)
            return False

    def verify_v7_credentials(self, client_id, client_secret):
        """Verify V7 API credentials"""
        print("\n" + "=" * 60)
        print("Testing V7 API Credentials")
        print("=" * 60)

        url = f"{self.base_url}/V7/Authenticate/GetToken"
        payload = {
            "ClientID": client_id,
            "ClientSecret": client_secret
        }

        print(f"\nEndpoint: {url}")
        print(f"Payload: {json.dumps({'ClientID': client_id, 'ClientSecret': client_secret[:20] + '...'}, indent=2)}")

        try:
            response = requests.post(url, json=payload, timeout=30)
            print(f"\nStatus Code: {response.status_code}")

            if response.status_code == 200:
                token_data = response.json()
                token = token_data.get('token', '')
                print(f"[OK] SUCCESS: Token received")
                print(f"Token (first 50 chars): {token[:50]}...")
                self.results["v7"]["status"] = "[OK] PASSED"
                self.results["v7"]["token"] = token[:50] + "..."
                return True
            else:
                error_msg = response.text
                print(f"[FAIL] FAILED: {error_msg}")
                self.results["v7"]["status"] = "[FAIL] FAILED"
                self.results["v7"]["error"] = f"Status {response.status_code}"
                return False

        except requests.exceptions.Timeout:
            print("[FAIL] FAILED: Request timed out")
            self.results["v7"]["status"] = "[FAIL] FAILED"
            self.results["v7"]["error"] = "Timeout"
            return False
        except Exception as e:
            print(f"[FAIL] FAILED: {str(e)}")
            self.results["v7"]["status"] = "[FAIL] FAILED"
            self.results["v7"]["error"] = str(e)
            return False

    def print_summary(self):
        """Print verification summary"""
        print("\n" + "=" * 60)
        print("CREDENTIAL VERIFICATION SUMMARY")
        print("=" * 60)
        print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\nV5.0 API: {self.results['v5']['status']}")
        if self.results['v5']['error']:
            print(f"  Error: {self.results['v5']['error']}")
        if self.results['v5']['token']:
            print(f"  Token: {self.results['v5']['token']}")

        print(f"\nV7 API: {self.results['v7']['status']}")
        if self.results['v7']['error']:
            print(f"  Error: {self.results['v7']['error']}")
        if self.results['v7']['token']:
            print(f"  Token: {self.results['v7']['token']}")

        print("\n" + "=" * 60)

        # Overall status
        if self.results['v5']['status'] == "[OK] PASSED" and self.results['v7']['status'] == "[OK] PASSED":
            print("[OK] ALL CREDENTIALS VERIFIED SUCCESSFULLY")
            print("You can now run the test suite!")
            return True
        else:
            print("[FAIL] SOME CREDENTIALS FAILED VERIFICATION")
            print("Please check the errors above and update credentials")
            return False


def main():
    """Main execution"""
    print("\n" + "=" * 60)
    print("SUREPREP API CREDENTIAL VERIFICATION")
    print("=" * 60)
    print("\nThis script will verify your V5 and V7 API credentials")
    print("by attempting to get authentication tokens.\n")

    # V5 Credentials
    print("V5.0 API Credentials:")
    print("-" * 60)
    v5_username = "PRIYA1"
    v5_password = "Abcd@12345"
    v5_api_key = "C690222D-8625-46F7-92CC-A61DA060D7A9"

    print(f"Username: {v5_username}")
    print(f"Password: {'*' * len(v5_password)}")
    print(f"API Key: {v5_api_key[:20]}...")

    # V7 Credentials
    print("\nV7 API Credentials:")
    print("-" * 60)
    v7_client_id = "CCmDgzLV35QnRYPR7c5UJReYqbuNXUoN"
    v7_client_secret = "BiC_ojduHzVRRG6Kktjx5GTXTT1KeS6nVjqLsrWynSo0IKjT3Xs7gYHK76ap-A65"

    print(f"Client ID: {v7_client_id[:20]}...")
    print(f"Client Secret: {'*' * 40}...")

    # Create verifier and test credentials
    verifier = CredentialVerifier()

    # Verify V5 credentials
    v5_success = verifier.verify_v5_credentials(v5_username, v5_password, v5_api_key)

    # Verify V7 credentials
    v7_success = verifier.verify_v7_credentials(v7_client_id, v7_client_secret)

    # Print summary
    verifier.print_summary()

    # Return exit code
    if v5_success and v7_success:
        print("\n[OK] Ready to run tests!")
        print("\nNext steps:")
        print("1. Run: pytest tests/test_sureprep_api_suite.py -v -m authentication")
        print("2. Or run: run_sureprep_tests.bat")
        return 0
    else:
        print("\n[FAIL] Please fix credential issues before running tests")
        return 1


if __name__ == "__main__":
    exit(main())
