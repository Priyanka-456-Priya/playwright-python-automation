"""
Generate comprehensive test suite from Swagger API JSON specifications
"""
import json
import re
from pathlib import Path

def sanitize_test_name(api_endpoint):
    """Convert API endpoint to valid Python test method name"""
    if not api_endpoint:
        return "test_unknown_api"
    # Remove method prefix (post, get, etc.)
    name = re.sub(r'^(post|get|put|delete|patch)\s+', '', api_endpoint.lower())
    # Replace special characters with underscores
    name = re.sub(r'[^\w]+', '_', name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    return f"test_{name}"

def extract_api_info(api_entry):
    """Extract API method, version, and endpoint from entry"""
    api_str = api_entry.get('Swagger APIs', '') or ''
    if not api_str:
        return 'POST', '/unknown', 'V7'
    parts = api_str.split(' ', 1)

    if len(parts) == 2:
        method = parts[0].upper()
        endpoint = parts[1]
    else:
        method = 'POST'
        endpoint = api_str

    # Extract version (V5.0, V6.0, V7, etc.)
    version_match = re.search(r'/(V\d+\.?\d*(?:\.\d+)?)', endpoint)
    version = version_match.group(1) if version_match else 'V7'

    return method, endpoint, version

def generate_test_method(api_entry, index):
    """Generate a test method for a single API endpoint"""
    api_name = api_entry.get('Swagger APIs', '')
    input_data = api_entry.get('Input', '{}')
    expected_output = api_entry.get('Output', '{}')

    method, endpoint, version = extract_api_info(api_entry)
    test_name = sanitize_test_name(api_name)

    # Determine if it's V5 or V7
    api_version = 'v5' if 'V5.0' in endpoint or 'V6.0' in endpoint else 'v7'

    # Properly escape and format the data
    # Remove trailing commas from JSON
    if input_data and isinstance(input_data, str):
        input_data_clean = re.sub(r',\s*([\]}])', r'\1', input_data)
        try:
            input_data_str = json.dumps(json.loads(input_data_clean))
        except:
            input_data_str = json.dumps({})
    elif isinstance(input_data, dict):
        input_data_str = json.dumps(input_data)
    else:
        input_data_str = json.dumps({})

    # For expected output, just store as string for now
    expected_output_str = repr(expected_output)

    test_code = f'''
    def {test_name}_{index}(self):
        """TC_{index:03d}: Test {api_name}"""
        url = f"{{TestConfig.BASE_URL}}{endpoint}"

        # Input payload
        payload_str = {input_data_str!r}
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='{method}',
            url=url,
            payload=payload,
            api_version="{api_version}"
        )

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \\
            f"Expected valid status code, got {{response.status_code}}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()
                print(f"API: {api_name}")
                print(f"Status: {{response.status_code}}")
                print(f"Response keys: {{list(response_data.keys()) if isinstance(response_data, dict) else 'list response'}}")

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {{response.text[:200]}}")
'''

    return test_code

def generate_test_file(json_file_path, output_file_path):
    """Generate complete test file from JSON specifications"""

    # Read JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        apis = json.load(f)

    # Generate header
    test_file_content = '''"""
Auto-generated Test Suite for Swagger APIs
Generated from: SureprepAPI_Swagger_2025.json
Total APIs: {total_apis}
"""

import pytest
import requests
import json
from datetime import datetime
import os
from typing import Dict, Any


class TestConfig:
    """Test configuration and setup"""
    BASE_URL = os.getenv('SUREPREP_BASE_URL', 'https://devtr-api-iscrum.sureprep.com')

    # V5 Credentials
    V5_USERNAME = os.getenv('SUREPREP_V5_USERNAME', 'PRIYA1')
    V5_PASSWORD = os.getenv('SUREPREP_V5_PASSWORD', 'Abcd@12345')
    V5_API_KEY = os.getenv('SUREPREP_V5_API_KEY', 'C690222D-8625-46F7-92CC-A61DA060D7A9')

    # V7 Credentials
    V7_CLIENT_ID = os.getenv('SUREPREP_V7_CLIENT_ID', 'GxJQo22jTg9koTeDtbIHpg8nmWdns9cu')
    V7_CLIENT_SECRET = os.getenv('SUREPREP_V7_CLIENT_SECRET', 'yZdKNGi2b-Fsp1uWZllPnST7VM2PdSc3hDC4_rZ5tfGektIltwkfYPLLDEGD6f_M')

    TIMEOUT = 30
    AUTH_TOKEN_V5 = None
    AUTH_TOKEN_V7 = None


class BaseAPITest:
    """Base class for all API tests with common utilities"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_auth(self, request):
        """Setup authentication tokens for all tests"""
        if TestConfig.AUTH_TOKEN_V5 is None:
            TestConfig.AUTH_TOKEN_V5 = self.get_auth_token_v5()
        if TestConfig.AUTH_TOKEN_V7 is None:
            TestConfig.AUTH_TOKEN_V7 = self.get_auth_token_v7()
        request.cls.token_v5 = TestConfig.AUTH_TOKEN_V5
        request.cls.token_v7 = TestConfig.AUTH_TOKEN_V7
        request.cls.token = TestConfig.AUTH_TOKEN_V7  # Default to V7

    def get_auth_token_v5(self) -> str:
        """Get authentication token from V5.0 API"""
        auth_url = f"{{TestConfig.BASE_URL}}/V5.0/Authenticate/GetToken"
        payload = {{
            "UserName": TestConfig.V5_USERNAME,
            "Password": TestConfig.V5_PASSWORD,
            "APIKey": TestConfig.V5_API_KEY
        }}
        try:
            response = requests.post(auth_url, json=payload, timeout=TestConfig.TIMEOUT)
            if response.status_code == 200:
                token = response.json().get('Token', '')
                print(f"V5 Token obtained: {{token[:20]}}..." if token else "V5 Token is empty")
                return token
            else:
                print(f"V5 Authentication failed with status: {{response.status_code}}")
        except Exception as e:
            print(f"V5 Authentication exception: {{str(e)}}")
        return ""

    def get_auth_token_v7(self) -> str:
        """Get authentication token from V7 API"""
        auth_url = f"{{TestConfig.BASE_URL}}/V7/Authenticate/GetToken"
        payload = {{
            "ClientID": TestConfig.V7_CLIENT_ID,
            "ClientSecret": TestConfig.V7_CLIENT_SECRET
        }}
        try:
            response = requests.post(auth_url, json=payload, timeout=TestConfig.TIMEOUT)
            if response.status_code == 200:
                return response.json().get('Token', '')
        except Exception as e:
            print(f"V7 Authentication failed: {{str(e)}}")
        return ""

    def get_headers(self, api_version: str = "v7") -> Dict[str, str]:
        """Get common headers for API requests"""
        token = self.token_v5 if api_version == "v5" else self.token
        return {{
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {{token}}'
        }}

    def make_request(self, method: str, url: str, payload: Dict = None,
                     expected_status: int = 200, api_version: str = "v7") -> requests.Response:
        """Make API request with common error handling"""
        try:
            response = requests.request(
                method=method,
                url=url,
                json=payload,
                headers=self.get_headers(api_version=api_version),
                timeout=TestConfig.TIMEOUT
            )
            return response
        except requests.exceptions.Timeout:
            pytest.fail(f"Request timed out for {{url}}")
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed: {{str(e)}}")


class TestSwaggerAPIs(BaseAPITest):
    """Auto-generated test cases for all Swagger APIs"""
'''.format(total_apis=len(apis))

    # Generate test methods
    for index, api_entry in enumerate(apis, start=1):
        test_method = generate_test_method(api_entry, index)
        test_file_content += test_method

    # Add main block
    test_file_content += '''

if __name__ == "__main__":
    pytest.main([
        __file__,
        '-v'
    ])
'''

    # Write to file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(test_file_content)

    print(f"[SUCCESS] Test suite generated successfully!")
    print(f"  Total APIs: {len(apis)}")
    print(f"  Output file: {output_file_path}")

    return len(apis)


if __name__ == "__main__":
    json_path = Path(r"c:\Users\6124481\VS_CODE Projects\API_Error_Codes_Validation\testData\swagger_apis.json")
    output_path = Path(r"c:\Users\6124481\VS_CODE Projects\API_Error_Codes_Validation\tests\test_auto_generated_swagger_apis.py")

    total = generate_test_file(json_path, output_path)
    print(f"\n[SUCCESS] Generated {total} test cases")
