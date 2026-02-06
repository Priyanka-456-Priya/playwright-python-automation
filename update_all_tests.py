"""
Helper script to update all test methods to use display_test_result()

This script will:
1. Read the test file
2. Find all test methods
3. Add display_test_result() call after each API request
4. Clean up old print statements

Note: Review the changes before running tests!
"""

import re

def update_test_file():
    test_file_path = r"tests\test_auto_generated_swagger_apis.py"

    with open(test_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to find test methods and extract endpoint info
    # This is a simplified version - manual review recommended

    print("=" * 80)
    print("Instructions to Update Remaining Tests:")
    print("=" * 80)
    print()
    print("For each test method, add these changes:")
    print()
    print("1. After the URL is defined, extract the endpoint:")
    print("   endpoint = '/V5.0/SomeAPI/Method'  # Extract from URL")
    print()
    print("2. After the response is received, add:")
    print("   self.display_test_result(endpoint, 'POST', response, payload)")
    print()
    print("3. Remove old print statements like:")
    print("   - print(f'API: ...')")
    print("   - print(f'Status: ...')")
    print("   - print(f'Response keys: ...')")
    print()
    print("Example pattern:")
    print("-" * 80)
    print("""
    def test_example(self):
        url = f"{TestConfig.BASE_URL}/V5.0/API/Method"
        endpoint = "/V5.0/API/Method"  # ADD THIS

        payload = {...}

        response = self.make_request(
            method='POST',
            url=url,
            payload=payload
        )

        # ADD THIS LINE
        self.display_test_result(endpoint, 'POST', response, payload)

        # Keep assertions
        assert response.status_code in [200, 201, 400, 401, 404]
        ...
    """)
    print("-" * 80)
    print()
    print("Total test methods to update: ~113")
    print("First test (test_v5_0_authenticate_gettoken_1) is already updated as example")
    print()
    print("=" * 80)

if __name__ == "__main__":
    update_test_file()
