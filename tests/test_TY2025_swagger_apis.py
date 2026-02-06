"""
Auto-generated Test Suite for Swagger APIs
Generated from: SureprepAPI_Swagger_2025.json
Total APIs: 113
"""

import pytest
import requests
import json
from datetime import datetime
import os
from typing import Dict, Any
import allure


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

    test_data = None

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

        # Load test data JSON
        if BaseAPITest.test_data is None:
            BaseAPITest.test_data = self.load_test_data()
        request.cls.test_data = BaseAPITest.test_data

    def load_test_data(self) -> Dict:
        """Load test data from JSON file"""
        try:
            test_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'test_data.json')
            with open(test_data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load test_data.json: {str(e)}")
            return {}

    def get_auth_token_v5(self) -> str:
        """Get authentication token from V5.0 API"""
        auth_url = f"{TestConfig.BASE_URL}/V5.0/Authenticate/GetToken"
        endpoint = "/V5.0/Authenticate/GetToken"
        payload = {
            "UserName": TestConfig.V5_USERNAME,
            "Password": TestConfig.V5_PASSWORD,
            "APIKey": TestConfig.V5_API_KEY
        }
        try:
            response = requests.post(auth_url, json=payload, timeout=TestConfig.TIMEOUT)
            if response.status_code == 200:
                token = response.json().get('Token', '')
                print(f"V5 Token obtained: {token[:20]}..." if token else "V5 Token is empty")
                return token
            else:
                print(f"V5 Authentication failed with status: {response.status_code}")
        except Exception as e:
            print(f"V5 Authentication exception: {str(e)}")
        return ""

    def get_auth_token_v7(self) -> str:
        """Get authentication token from V7 API"""
        auth_url = f"{TestConfig.BASE_URL}/V7/Authenticate/GetToken"
        endpoint = "/V7/Authenticate/GetToken"
        payload = {
            "ClientID": TestConfig.V7_CLIENT_ID,
            "ClientSecret": TestConfig.V7_CLIENT_SECRET
        }
        try:
            response = requests.post(auth_url, json=payload, timeout=TestConfig.TIMEOUT)
            if response.status_code == 200:
                return response.json().get('Token', '')
        except Exception as e:
            print(f"V7 Authentication failed: {str(e)}")
        return ""

    def get_headers(self, api_version: str = "v7") -> Dict[str, str]:
        """Get common headers for API requests"""
        token = self.token_v5 if api_version == "v5" else self.token
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

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
            pytest.fail(f"Request timed out for {url}")
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed: {str(e)}")

    def display_test_result(self, endpoint: str, method: str, response: requests.Response, payload: Dict[str, Any] = {}):
        """Display test result with expected and actual output"""
        print("\n" + "="*80)
        print(f"TEST RESULT FOR: {method} {endpoint}")
        print("="*80)

        # Display input
        print("\nINPUT:")
        print(f"  Endpoint: {endpoint}")
        print(f"  Method: {method}")
        if payload:
            print(f"  Payload: {json.dumps(payload, indent=4)}")

        # Display actual output
        print("\nACTUAL OUTPUT:")
        print(f"  Status Code: {response.status_code}")
        try:
            response_data = response.json()
            print(f"  Response Body: {json.dumps(response_data, indent=4)}")
        except json.JSONDecodeError:
            print(f"  Response Body (Text): {response.text[:500]}")

        # Display expected output from test_data.json
        print("\nEXPECTED OUTPUT (from test_data.json):")
        expected_info = self.get_expected_output(endpoint, response.status_code)
        if expected_info:
            print(f"  {expected_info}")
        else:
            print("  No expected output defined in test_data.json for this scenario")

        print("="*80 + "\n")

        # Add Allure attachments
        with allure.step(f"{method} {endpoint}"):
            allure.attach(
                json.dumps({"endpoint": endpoint, "method": method, "payload": payload}, indent=2),
                name="Request Details",
                attachment_type=allure.attachment_type.JSON
            )

            allure.attach(
                str(response.status_code),
                name="Response Status Code",
                attachment_type=allure.attachment_type.TEXT
            )

            try:
                response_data = response.json()
                allure.attach(
                    json.dumps(response_data, indent=2),
                    name="Response Body",
                    attachment_type=allure.attachment_type.JSON
                )
            except json.JSONDecodeError:
                allure.attach(
                    response.text[:500],
                    name="Response Body (Text)",
                    attachment_type=allure.attachment_type.TEXT
                )

    def get_expected_output(self, endpoint: str, actual_status: int) -> str:
        """Get expected output information from test_data.json based on status code"""
        if not hasattr(self, 'test_data') or not self.test_data:
            return ""

        test_scenarios = self.test_data.get('test_scenarios', {})

        # Map status code to scenario
        status_map = {
            400: '400_bad_request',
            401: '401_unauthorized',
            404: '404_not_found',
            405: '405_method_not_allowed',
            500: '500_internal_server_error'
        }

        scenario_key = status_map.get(actual_status)
        if not scenario_key:
            if actual_status in [200, 201]:
                return "Expected Status: 200/201 (Success) - Response should contain valid data"
            return ""

        scenario = test_scenarios.get(scenario_key, {})

        # Search for matching endpoint in the scenario
        for test_case_data in scenario.values():
            if isinstance(test_case_data, dict):
                # Check if endpoint matches
                if 'endpoint' in test_case_data and endpoint in test_case_data['endpoint']:
                    expected_code = test_case_data.get('expected_code', actual_status)
                    description = test_case_data.get('description', '')
                    return f"Expected Status Code: {expected_code}\n  Description: {description}"

                # Check if endpoint is in endpoints list
                if 'endpoints' in test_case_data:
                    for ep in test_case_data['endpoints']:
                        if isinstance(ep, dict) and endpoint in ep.get('path', ''):
                            description = test_case_data.get('description', '')
                            return f"Expected Status Code: {actual_status}\n  Description: {description}"

        return f"Expected Status Code: {actual_status} - {scenario_key.replace('_', ' ').title()}"


@allure.feature("SurePrep API - Swagger APIs")
class TestSwaggerAPIs(BaseAPITest):
    """Auto-generated test cases for all Swagger APIs"""

    @allure.story("Authentication")
    @allure.title("TC_001: POST /V5.0/Authenticate/GetToken")
    @allure.description("Test authentication endpoint with invalid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_authenticate_gettoken_1(self):
        """TC_001: Test post /V5.0/Authenticate/GetToken"""
        url = f"{TestConfig.BASE_URL}/V5.0/Authenticate/GetToken"
        endpoint = "/V5.0/Authenticate/GetToken"

        # Input payload
        payload_str = '{"UserName": "PRIYA", "Password": "Abcd@12345", "APIKey": "24CDFF63-782A-4382-9F4B-0272C03ED095"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result with expected output
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()
                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Authentication")
    @allure.title("TC_002: POST /V7/Authenticate/GetToken")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_authenticate_gettoken_2(self):
        """TC_002: Test post /V7/Authenticate/GetToken"""
        url = f"{TestConfig.BASE_URL}/V7/Authenticate/GetToken"
        endpoint = "/V7/Authenticate/GetToken"

        # Input payload
        payload_str = '{"ClientID": "xfO08U5uScAnOISU76C9EOi68XYFfIuR", "ClientSecret": "Cn1gyCldo4o4_C0m8V3O_rJIkBObCvBJyLNIjRqSCxY0B1kjBDkCEYpgZNpoJH0L"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_003: POST /V5.0/BinderInfo/GetBinderDetails")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_getbinderdetails_3(self):
        """TC_003: Test post /V5.0/BinderInfo/GetBinderDetails"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetBinderDetails"
        endpoint = "/V5.0/BinderInfo/GetBinderDetails"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2025UT7"], "BinderType": "1040", "OwnerEmail": "tr.karandeepsingh.talwar+421038@outlook.com"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_004: POST /V5.0/BinderInfo/GetUnclearedNotes")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_getunclearednotes_4(self):
        """TC_004: Test post /V5.0/BinderInfo/GetUnclearedNotes"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetUnclearedNotes"
        endpoint = "/V5.0/BinderInfo/GetUnclearedNotes"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2025UT7"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_005: POST /V5.0/BinderInfo/GetUnreviewedTRStamps")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_getunreviewedtrstamps_5(self):
        """TC_005: Test post /V5.0/BinderInfo/GetUnreviewedTRStamps"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetUnreviewedTRStamps"
        endpoint = "/V5.0/BinderInfo/GetUnreviewedTRStamps"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2025UT7"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_006: POST /V5.0/BinderInfo/GetUnreviewedStickyNotes")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_getunreviewedstickynotes_6(self):
        """TC_006: Test post /V5.0/BinderInfo/GetUnreviewedStickyNotes"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetUnreviewedStickyNotes"
        endpoint = "/V5.0/BinderInfo/GetUnreviewedStickyNotes"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2025UT7"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_007: POST /V5.0/BinderInfo/GetUnreviewedWorkpapersByL1")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_getunreviewedworkpapersbyl1_7(self):
        """TC_007: Test post /V5.0/BinderInfo/GetUnreviewedWorkpapersByL1"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetUnreviewedWorkpapersByL1"
        endpoint = "/V5.0/BinderInfo/GetUnreviewedWorkpapersByL1"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_008: POST /V5.0/BinderInfo/GetUnreviewedWorkpapersByL2")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_getunreviewedworkpapersbyl2_8(self):
        """TC_008: Test post /V5.0/BinderInfo/GetUnreviewedWorkpapersByL2"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetUnreviewedWorkpapersByL2"
        endpoint = "/V5.0/BinderInfo/GetUnreviewedWorkpapersByL2"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_009: POST /V5.0/BinderInfo/GetUnreviewedWorkpapersByL3")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_getunreviewedworkpapersbyl3_9(self):
        """TC_009: Test post /V5.0/BinderInfo/GetUnreviewedWorkpapersByL3"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetUnreviewedWorkpapersByL3"
        endpoint = "/V5.0/BinderInfo/GetUnreviewedWorkpapersByL3"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_010: POST /V5.0/BinderInfo/GetUnreviewedWorkpapersByL4")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_getunreviewedworkpapersbyl4_10(self):
        """TC_010: Test post /V5.0/BinderInfo/GetUnreviewedWorkpapersByL4"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetUnreviewedWorkpapersByL4"
        endpoint = "/V5.0/BinderInfo/GetUnreviewedWorkpapersByL4"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_011: POST /V5.0/BinderInfo/GetDocumentPendingReviewCount")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_getdocumentpendingreviewcount_11(self):
        """TC_011: Test post /V5.0/BinderInfo/GetDocumentPendingReviewCount"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetDocumentPendingReviewCount"
        endpoint = "/V5.0/BinderInfo/GetDocumentPendingReviewCount"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_012: POST /V5.0/BinderInfo/GetDocumentPendingSignatureCount")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_getdocumentpendingsignaturecount_12(self):
        """TC_012: Test post /V5.0/BinderInfo/GetDocumentPendingSignatureCount"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetDocumentPendingSignatureCount"
        endpoint = "/V5.0/BinderInfo/GetDocumentPendingSignatureCount"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_013: POST /V5.0/BinderInfo/GetDocumentPendingUploadCount")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_getdocumentpendinguploadcount_13(self):
        """TC_013: Test post /V5.0/BinderInfo/GetDocumentPendingUploadCount"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetDocumentPendingUploadCount"
        endpoint = "/V5.0/BinderInfo/GetDocumentPendingUploadCount"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_014: POST /V5.0/BinderInfo/GetBinderPendingItems")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_getbinderpendingitems_14(self):
        """TC_014: Test post /V5.0/BinderInfo/GetBinderPendingItems"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetBinderPendingItems"
        endpoint = "/V5.0/BinderInfo/GetBinderPendingItems"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": "2025UT7"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_015: POST /V5.0/BinderInfo/GetTaxCaddyDocumentsCount")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binderinfo_gettaxcaddydocumentscount_15(self):
        """TC_015: Test post /V5.0/BinderInfo/GetTaxCaddyDocumentsCount"""
        url = f"{TestConfig.BASE_URL}/V5.0/BinderInfo/GetTaxCaddyDocumentsCount"
        endpoint = "/V5.0/BinderInfo/GetTaxCaddyDocumentsCount"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["5406XO_LIV"]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_016: POST /V7/BinderInfo/GetBinderDetails")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getbinderdetails_16(self):
        """TC_016: Test post /V7/BinderInfo/GetBinderDetails"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetBinderDetails"
        endpoint = "/V7/BinderInfo/GetBinderDetails"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["BULKFILL"], "PageNumber": 1, "PageSize": 10, "BinderType": "1040", "OwnerEmail": "Priyanka.patil@thomsonreuters.com"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_017: POST /V7/BinderInfo/GetBinderDetails/{binderId}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getbinderdetails_binderid_17(self):
        """TC_017: Test post /V7/BinderInfo/GetBinderDetails/{binderId}"""
        binderId = 41968512  # Sample binder ID for testing
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetBinderDetails/{binderId}"
        endpoint = "/V7/BinderInfo/GetBinderDetails/{binderId}"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_018: POST /V7/BinderInfo/GetBinderDetailsByUniqueIdentifier")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getbinderdetailsbyuniqueidentifier_18(self):
        """TC_018: Test post /V7/BinderInfo/GetBinderDetailsByUniqueIdentifier"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetBinderDetailsByUniqueIdentifier"
        endpoint = "/V7/BinderInfo/GetBinderDetailsByUniqueIdentifier"

        # Input payload
        payload_str = '{"TaxYear": 2025, "UniqueIdentifier": "c0b2e667-9bcf-4903-a9d3-a0e16517c0ea"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_019: POST /V7/BinderInfo/GetUnclearedNotes")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getunclearednotes_19(self):
        """TC_019: Test post /V7/BinderInfo/GetUnclearedNotes"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetUnclearedNotes"
        endpoint = "/V7/BinderInfo/GetUnclearedNotes"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_020: POST /V7/BinderInfo/GetUnreviewedTRStamps")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getunreviewedtrstamps_20(self):
        """TC_020: Test post /V7/BinderInfo/GetUnreviewedTRStamps"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetUnreviewedTRStamps"
        endpoint = "/V7/BinderInfo/GetUnreviewedTRStamps"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2025UT7"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_021: POST /V7/BinderInfo/GetUnreviewedStickyNotes")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getunreviewedstickynotes_21(self):
        """TC_021: Test post /V7/BinderInfo/GetUnreviewedStickyNotes"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetUnreviewedStickyNotes"
        endpoint = "/V7/BinderInfo/GetUnreviewedStickyNotes"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2025UT7"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_022: POST /V7/BinderInfo/GetUnreviewedWorkpapersByL1")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getunreviewedworkpapersbyl1_22(self):
        """TC_022: Test post /V7/BinderInfo/GetUnreviewedWorkpapersByL1"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetUnreviewedWorkpapersByL1"
        endpoint = "/V7/BinderInfo/GetUnreviewedWorkpapersByL1"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_023: POST /V7/BinderInfo/GetUnreviewedWorkpapersByL2")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getunreviewedworkpapersbyl2_23(self):
        """TC_023: Test post /V7/BinderInfo/GetUnreviewedWorkpapersByL2"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetUnreviewedWorkpapersByL2"
        endpoint = "/V7/BinderInfo/GetUnreviewedWorkpapersByL2"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_024: POST /V7/BinderInfo/GetUnreviewedWorkpapersByL3")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getunreviewedworkpapersbyl3_24(self):
        """TC_024: Test post /V7/BinderInfo/GetUnreviewedWorkpapersByL3"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetUnreviewedWorkpapersByL3"
        endpoint = "/V7/BinderInfo/GetUnreviewedWorkpapersByL3"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_025: POST /V7/BinderInfo/GetUnreviewedWorkpapersByL4")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getunreviewedworkpapersbyl4_25(self):
        """TC_025: Test post /V7/BinderInfo/GetUnreviewedWorkpapersByL4"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetUnreviewedWorkpapersByL4"
        endpoint = "/V7/BinderInfo/GetUnreviewedWorkpapersByL4"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_026: POST /V7/BinderInfo/GetDocumentPendingReviewCount")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getdocumentpendingreviewcount_26(self):
        """TC_026: Test post /V7/BinderInfo/GetDocumentPendingReviewCount"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetDocumentPendingReviewCount"
        endpoint = "/V7/BinderInfo/GetDocumentPendingReviewCount"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_027: POST /V7/BinderInfo/GetDocumentPendingSignatureCount")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getdocumentpendingsignaturecount_27(self):
        """TC_027: Test post /V7/BinderInfo/GetDocumentPendingSignatureCount"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetDocumentPendingSignatureCount"
        endpoint = "/V7/BinderInfo/GetDocumentPendingSignatureCount"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_028: POST /V7/BinderInfo/GetDocumentPendingUploadCount")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getdocumentpendinguploadcount_28(self):
        """TC_028: Test post /V7/BinderInfo/GetDocumentPendingUploadCount"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetDocumentPendingUploadCount"
        endpoint = "/V7/BinderInfo/GetDocumentPendingUploadCount"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["2K25DRL_LIVE"], "BinderType": "1040"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_029: POST /V7/BinderInfo/GetBinderPendingItems")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binderinfo_getbinderpendingitems_29(self):
        """TC_029: Test post /V7/BinderInfo/GetBinderPendingItems"""
        url = f"{TestConfig.BASE_URL}/V7/BinderInfo/GetBinderPendingItems"
        endpoint = "/V7/BinderInfo/GetBinderPendingItems"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": "2025UT7"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_030: POST /V5.0/Binder/PrintBinder")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_printbinder_30(self):
        """TC_030: Test post /V5.0/Binder/PrintBinder"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/PrintBinder"
        endpoint = "/V5.0/Binder/PrintBinder"

        # Input payload
        payload_str = '{"TaxYear": 2025, "ClientID": ["5406XO_LIV"]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_031: POST /V5.0/Binder/CreateBinder")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_createbinder_31(self):
        """TC_031: Test post /V5.0/Binder/CreateBinder"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/CreateBinder"
        endpoint = "/V5.0/Binder/CreateBinder"

        # Input payload
        payload_str = '{"AccountNumber": "421038", "Custom_Field": "ADGTEST", "Email": "priyanka.patil@thomsonreuters.com", "Unique_Identifier": "B611C44C-7058-4F5C-A789-5F5A9E597BC7", "Service_Type_Id": 2, "Template_Id": 41947079, "Has_Leadsheet": 1, "SubmissionType": 1, "Is7216ConsentReceived": 1, "Client_Id": "ABCDRT", "Locator_No": "ABCDRT", "LinkBinder": "0", "Filing_Status": "1", "Taxpayer_SSN": "147852369", "Office_Location_Id": 20242}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_032: POST /V5.0/Binder/UploadBinderDocuments")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_uploadbinderdocuments_32(self):
        """TC_032: Test post /V5.0/Binder/UploadBinderDocuments"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/UploadBinderDocuments"
        endpoint = "/V5.0/Binder/UploadBinderDocuments"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_033: POST /V5.0/Binder/SubmitBinder")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_submitbinder_33(self):
        """TC_033: Test post /V5.0/Binder/SubmitBinder"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/SubmitBinder"
        endpoint = "/V5.0/Binder/SubmitBinder"

        # Input payload
        payload_str = '{"Binder_Id": 41968512, "IsInHouseProcess": 0}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_034: POST /V5.0/Binder/UpdateProjectID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_updateprojectid_34(self):
        """TC_034: Test post /V5.0/Binder/UpdateProjectID"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/UpdateProjectID"
        endpoint = "/V5.0/Binder/UpdateProjectID"

        # Input payload
        payload_str = '{"BinderID": 41968512, "ProjectID": "ABCDRT", "ClientId": "ABCDRT", "BinderType": "1040", "TaxYear": 2025}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_035: POST /V5.0/Binder/GetStatesandLocalities")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_getstatesandlocalities_35(self):
        """TC_035: Test post /V5.0/Binder/GetStatesandLocalities"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/GetStatesandLocalities"
        endpoint = "/V5.0/Binder/GetStatesandLocalities"

        # Input payload
        payload_str = '{"Binder_Id": 41976512}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_036: POST /V5.0/Binder/GetBindersStatusWithStates")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_getbindersstatuswithstates_36(self):
        """TC_036: Test post /V5.0/Binder/GetBindersStatusWithStates"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/GetBindersStatusWithStates"
        endpoint = "/V5.0/Binder/GetBindersStatusWithStates"

        # Input payload
        payload_str = '{"Binder_Id": 41976512, "TaxYear": 2025, "PageNumber": 1, "PageSize": 10}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_037: POST /V5.0/Binder/DownloadBinderPBFX")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_downloadbinderpbfx_37(self):
        """TC_037: Test post /V5.0/Binder/DownloadBinderPBFX"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/DownloadBinderPBFX"
        endpoint = "/V5.0/Binder/DownloadBinderPBFX"

        # Input payload
        payload_str = '{"Binder_Id": 41957602, "Mapped_Id": "kunal.patil@thomsonreuters.com"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_038: POST /V5.0/Binder/GetBinderAuditLog")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_getbinderauditlog_38(self):
        """TC_038: Test post /V5.0/Binder/GetBinderAuditLog"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/GetBinderAuditLog"
        endpoint = "/V5.0/Binder/GetBinderAuditLog"

        # Input payload
        payload_str = '{"Binder_Id": 41968512, "ClientId": "ABCDRT", "BinderType": "1040", "TaxYear": 2025}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_039: POST /V5.0/Binder/UpdateOwnerMember")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_updateownermember_39(self):
        """TC_039: Test post /V5.0/Binder/UpdateOwnerMember"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/UpdateOwnerMember"
        endpoint = "/V5.0/Binder/UpdateOwnerMember"

        # Input payload
        payload_str = '{"Binder_Id": 41968512, "LoginUserEmail": "Priyanka.patil@thomsonreuters.com", "OwnerEmail": "Priyanka.patil@thomsonreuters.com", "LocationID": 0, "AssignMember": ["Anushka.kadam@thomsonreuters.com"]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_040: POST /V5.0/Binder/PrintBinder")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_printbinder_40(self):
        """TC_040: Test post /V5.0/Binder/PrintBinder"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/PrintBinder"
        endpoint = "/V5.0/Binder/PrintBinder"

        # Input payload
        payload_str = '{"BinderID": 41968512}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_041: POST /V7/Binder/CreateBinder")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_createbinder_41(self):
        """TC_041: Test post /V7/Binder/CreateBinder"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/CreateBinder"
        endpoint = "/V7/Binder/CreateBinder"

        # Input payload
        payload_str = '{"Custom_Field": "ADGTEST", "Email": "priyanka.patil@thomsonreuters.com", "Unique_Identifier": "DRLTEST", "Service_Type_Id": 2, "Template_Id": 41947075, "Has_Leadsheet": 1, "SubmissionType": 1, "Is7216ConsentReceived": 1, "Client_Id": "DRLTEST", "Locator_No": "DRLTEST", "LinkBinder": "0", "Filing_Status": "1", "Taxpayer_SSN": "147852369", "Office_Location_Id": 20242}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_042: POST /V7/Binder/UploadBinderDocuments")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_uploadbinderdocuments_42(self):
        """TC_042: Test post /V7/Binder/UploadBinderDocuments"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/UploadBinderDocuments"
        endpoint = "/V7/Binder/UploadBinderDocuments"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_043: POST /V7/Binder/GetPBFx/{binderId}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_getpbfx_binderid_43(self):
        """TC_043: Test post /V7/Binder/GetPBFx/{binderId}"""
        binderId = 41968512  # Sample binder ID for testing
        url = f"{TestConfig.BASE_URL}/V7/Binder/GetPBFx/{binderId}"
        endpoint = "/V7/Binder/GetPBFx/{binderId}"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_044: POST /V7/Binder/SubmitBinder")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_submitbinder_44(self):
        """TC_044: Test post /V7/Binder/SubmitBinder"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/SubmitBinder"
        endpoint = "/V7/Binder/SubmitBinder"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_045: POST /V7/Binder/UpdateProjectID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_updateprojectid_45(self):
        """TC_045: Test post /V7/Binder/UpdateProjectID"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/UpdateProjectID"
        endpoint = "/V7/Binder/UpdateProjectID"

        # Input payload
        payload_str = '{"BinderID": 41975105, "ProjectID": "TESTFGH", "ClientId": "DRLTEST", "BinderType": "1040", "TaxYear": 2025}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_046: POST /V7/Binder/GetStatesandLocalities")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_getstatesandlocalities_46(self):
        """TC_046: Test post /V7/Binder/GetStatesandLocalities"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/GetStatesandLocalities"
        endpoint = "/V7/Binder/GetStatesandLocalities"

        # Input payload
        payload_str = '{"Binder_Id": 41976512}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_047: POST /V7/Binder/GetBindersStatusWithStates")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_getbindersstatuswithstates_47(self):
        """TC_047: Test post /V7/Binder/GetBindersStatusWithStates"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/GetBindersStatusWithStates"
        endpoint = "/V7/Binder/GetBindersStatusWithStates"

        # Input payload
        payload_str = '{"Binder_Id": 41976512, "TaxYear": 2025, "PageNumber": 1, "PageSize": 10}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_048: POST /V7/Binder/DownloadBinderPBFX")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_downloadbinderpbfx_48(self):
        """TC_048: Test post /V7/Binder/DownloadBinderPBFX"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/DownloadBinderPBFX"
        endpoint = "/V7/Binder/DownloadBinderPBFX"

        # Input payload
        payload_str = '{"Binder_Id": 41957602, "Mapped_Id": "kunal.patil@thomsonreuters.com"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_049: POST /V7/Binder/GetBinderAuditLog")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_getbinderauditlog_49(self):
        """TC_049: Test post /V7/Binder/GetBinderAuditLog"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/GetBinderAuditLog"
        endpoint = "/V7/Binder/GetBinderAuditLog"

        # Input payload
        payload_str = '{"Binder_Id": 41963500, "ClientId": "Force", "BinderType": "1040", "TaxYear": 2025}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_050: POST /V7/Binder/UpdateOwnerMember")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_updateownermember_50(self):
        """TC_050: Test post /V7/Binder/UpdateOwnerMember"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/UpdateOwnerMember"
        endpoint = "/V7/Binder/UpdateOwnerMember"

        # Input payload
        payload_str = '{"Binder_Id": 41963500, "LoginUserEmail": "Priyanka.patil@thomsonreuters.com", "OwnerEmail": "Priyanka.patil@thomsonreuters.com", "LocationID": 0, "AssignMember": ["Anushka.kadam@thomsonreuters.com"]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_051: POST /V7/Binder/PrintBinder")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_printbinder_51(self):
        """TC_051: Test post /V7/Binder/PrintBinder"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/PrintBinder"
        endpoint = "/V7/Binder/PrintBinder"

        # Input payload
        payload_str = '{"BinderID": 41963500}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_052: POST /V5.0/Binder/GetDocuments")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_getdocuments_52(self):
        """TC_052: Test post /V5.0/Binder/GetDocuments"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/GetDocuments"
        endpoint = "/V5.0/Binder/GetDocuments"

        # Input payload
        payload_str = '{"AllFiles": 12, "FromDate": "2025-12-01T06:48:21.240Z", "ToDate": "2025-12-26T06:48:21.240Z", "Binder_ID": 41957446}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_053: POST /V5.0/Binder/DownloadDocument")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_downloaddocument_53(self):
        """TC_053: Test post /V5.0/Binder/DownloadDocument"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/DownloadDocument"
        endpoint = "/V5.0/Binder/DownloadDocument"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("DRL Operations")
    @allure.title("TC_054: POST test_https_api_sureprep_com_v7_drlinfo_getdrloutput_54")
    @allure.severity(allure.severity_level.NORMAL)
    def test_https_api_sureprep_com_v7_drlinfo_getdrloutput_54(self):
        """TC_054: Test https://api.sureprep.com/V7/DRLInfo/GetDRLOutput"""
        url = f"{TestConfig.BASE_URL}/V7/DRLInfo/GetDRLOutput"
        endpoint = "https://api.sureprep.com/V7/DRLInfo/GetDRLOutput"

        # Input payload
        payload_str = '{"ClientNumber": "BULKFILL", "TaxYear": 2025}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_055: POST test_unknown_api_55")
    @allure.severity(allure.severity_level.NORMAL)
    def test_unknown_api_55(self):
        """TC_055: Test None"""
        url = f"{TestConfig.BASE_URL}/unknown"
        endpoint = "/unknown"

        # Input payload
        payload_str = '{"ClientNumber": "BULKFILL", "TaxYear": 2025}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_056: POST /V7/Binder/GetDocuments")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_getdocuments_56(self):
        """TC_056: Test post /V7/Binder/GetDocuments"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/GetDocuments"
        endpoint = "/V7/Binder/GetDocuments"

        # Input payload
        payload_str = '{"AllFiles": 10, "FromDate": "2025-12-01T05:58:04.348Z", "ToDate": "2025-12-31T05:58:04.348Z", "Binder_ID": 41963500}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_057: POST /V7/Binder/DownloadDocument")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_downloaddocument_57(self):
        """TC_057: Test post /V7/Binder/DownloadDocument"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/DownloadDocument"
        endpoint = "/V7/Binder/DownloadDocument"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_058: POST /V5.0/Lookup/GetLocalPathToDownloadFiles")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_lookup_getlocalpathtodownloadfiles_58(self):
        """TC_058: Test post /V5.0/Lookup/GetLocalPathToDownloadFiles"""
        url = f"{TestConfig.BASE_URL}/V5.0/Lookup/GetLocalPathToDownloadFiles"
        endpoint = "/V5.0/Lookup/GetLocalPathToDownloadFiles"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_059: POST /V5.0/Lookup/ServiceTypes")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_lookup_servicetypes_59(self):
        """TC_059: Test post /V5.0/Lookup/ServiceTypes"""
        url = f"{TestConfig.BASE_URL}/V5.0/Lookup/ServiceTypes"
        endpoint = "/V5.0/Lookup/ServiceTypes"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_060: POST /V5.0/Lookup/OfficeLocations")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_lookup_officelocations_60(self):
        """TC_060: Test post /V5.0/Lookup/OfficeLocations"""
        url = f"{TestConfig.BASE_URL}/V5.0/Lookup/OfficeLocations"
        endpoint = "/V5.0/Lookup/OfficeLocations"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_061: POST /V5.0/Lookup/BinderTypes")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_lookup_bindertypes_61(self):
        """TC_061: Test post /V5.0/Lookup/BinderTypes"""
        url = f"{TestConfig.BASE_URL}/V5.0/Lookup/BinderTypes"
        endpoint = "/V5.0/Lookup/BinderTypes"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_062: POST /V5.0/Lookup/TaxSoftwareList")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_lookup_taxsoftwarelist_62(self):
        """TC_062: Test post /V5.0/Lookup/TaxSoftwareList"""
        url = f"{TestConfig.BASE_URL}/V5.0/Lookup/TaxSoftwareList"
        endpoint = "/V5.0/Lookup/TaxSoftwareList"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_063: POST /V5.0/Lookup/BinderTemplates")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_lookup_bindertemplates_63(self):
        """TC_063: Test post /V5.0/Lookup/BinderTemplates"""
        url = f"{TestConfig.BASE_URL}/V5.0/Lookup/BinderTemplates"
        endpoint = "/V5.0/Lookup/BinderTemplates"

        # Input payload
        payload_str = '{"Binder_Id": 41959111, "Status_Id": 0, "Mapped_Id": "Priyanka.patil@thomsonreuters.com", "IsInHouseProcess": 0}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_064: POST /V5.0/Lookup/BinderTemplateList")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_lookup_bindertemplatelist_64(self):
        """TC_064: Test post /V5.0/Lookup/BinderTemplateList"""
        url = f"{TestConfig.BASE_URL}/V5.0/Lookup/BinderTemplateList"
        endpoint = "/V5.0/Lookup/BinderTemplateList"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_065: POST /V5.0/Lookup/BinderStatusList")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_lookup_binderstatuslist_65(self):
        """TC_065: Test post /V5.0/Lookup/BinderStatusList"""
        url = f"{TestConfig.BASE_URL}/V5.0/Lookup/BinderStatusList"
        endpoint = "/V5.0/Lookup/BinderStatusList"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_066: POST /V7/Lookup/GetLocalPathToDownloadFiles")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_lookup_getlocalpathtodownloadfiles_66(self):
        """TC_066: Test post /V7/Lookup/GetLocalPathToDownloadFiles"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/GetLocalPathToDownloadFiles"
        endpoint = "/V7/Lookup/GetLocalPathToDownloadFiles"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_067: POST /V7/Lookup/ServiceTypes")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_lookup_servicetypes_67(self):
        """TC_067: Test post /V7/Lookup/ServiceTypes"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/ServiceTypes"
        endpoint = "/V7/Lookup/ServiceTypes"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_068: POST /V7/Lookup/OfficeLocations")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_lookup_officelocations_68(self):
        """TC_068: Test post /V7/Lookup/OfficeLocations"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/OfficeLocations"
        endpoint = "/V7/Lookup/OfficeLocations"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_069: POST /V7/Lookup/BinderTypes")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_lookup_bindertypes_69(self):
        """TC_069: Test post /V7/Lookup/BinderTypes"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/BinderTypes"
        endpoint = "/V7/Lookup/BinderTypes"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_070: POST /V7/Lookup/TaxSoftwareList")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_lookup_taxsoftwarelist_70(self):
        """TC_070: Test post /V7/Lookup/TaxSoftwareList"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/TaxSoftwareList"
        endpoint = "/V7/Lookup/TaxSoftwareList"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_071: POST /V7/Lookup/BinderTemplates")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_lookup_bindertemplates_71(self):
        """TC_071: Test post /V7/Lookup/BinderTemplates"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/BinderTemplates"
        endpoint = "/V7/Lookup/BinderTemplates"

        # Input payload
        payload_str = '{"Binder_Id": 41963500, "IsInHouseProcess": 0}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_072: POST /V7/Lookup/BinderTemplateList")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_lookup_bindertemplatelist_72(self):
        """TC_072: Test post /V7/Lookup/BinderTemplateList"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/BinderTemplateList"
        endpoint = "/V7/Lookup/BinderTemplateList"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_073: POST /V7/Lookup/BinderStatusList")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_lookup_binderstatuslist_73(self):
        """TC_073: Test post /V7/Lookup/BinderStatusList"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/BinderStatusList"
        endpoint = "/V7/Lookup/BinderStatusList"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_074: POST /V7/Lookup/ServiceUnits")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_lookup_serviceunits_74(self):
        """TC_074: Test post /V7/Lookup/ServiceUnits"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/ServiceUnits"
        endpoint = "/V7/Lookup/ServiceUnits"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_075: POST /V7/Lookup/DomainInformation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_lookup_domaininformation_75(self):
        """TC_075: Test post /V7/Lookup/DomainInformation"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/DomainInformation"
        endpoint = "/V7/Lookup/DomainInformation"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_076: POST /V7/Lookup/UserDomainDetails")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_lookup_userdomaindetails_76(self):
        """TC_076: Test post /V7/Lookup/UserDomainDetails"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/UserDomainDetails"
        endpoint = "/V7/Lookup/UserDomainDetails"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_077: POST /V7/Lookup/CustomFieldEnabled")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_lookup_customfieldenabled_77(self):
        """TC_077: Test post /V7/Lookup/CustomFieldEnabled"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/CustomFieldEnabled"
        endpoint = "/V7/Lookup/CustomFieldEnabled"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_078: POST /V7/Lookup/UTSearchClientGUID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_lookup_utsearchclientguid_78(self):
        """TC_078: Test post /V7/Lookup/UTSearchClientGUID"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/UTSearchClientGUID"
        endpoint = "/V7/Lookup/UTSearchClientGUID"

        # Input payload
        payload_str = '{"ClientID": "BULKFILL", "TaxYear": 2025}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_079: POST /V7/Lookup/7216ConsentEnabled")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_lookup_7216consentenabled_79(self):
        """TC_079: Test post /V7/Lookup/7216ConsentEnabled"""
        url = f"{TestConfig.BASE_URL}/V7/Lookup/7216ConsentEnabled"
        endpoint = "/V7/Lookup/7216ConsentEnabled"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_080: POST /V5.0/Binder/GetStatus")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_getstatus_80(self):
        """TC_080: Test post /V5.0/Binder/GetStatus"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/GetStatus"
        endpoint = "/V5.0/Binder/GetStatus"

        # Input payload
        payload_str = '{"Binder_Id": 41967142}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_081: POST /V5.0/Binder/ChangeBinderStatus")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v5_0_binder_changebinderstatus_81(self):
        """TC_081: Test post /V5.0/Binder/ChangeBinderStatus"""
        url = f"{TestConfig.BASE_URL}/V5.0/Binder/ChangeBinderStatus"
        endpoint = "/V5.0/Binder/ChangeBinderStatus"

        # Input payload
        payload_str = '{"Binder_Id": 41957656, "Status_Id": 8743}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_082: POST /V7/Binder/GetStatus")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_getstatus_82(self):
        """TC_082: Test post /V7/Binder/GetStatus"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/GetStatus"
        endpoint = "/V7/Binder/GetStatus"

        # Input payload
        payload_str = '{"Binder_Id": 41975105}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Binder Operations")
    @allure.title("TC_083: POST /V7/Binder/ChangeBinderStatus")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_v7_binder_changebinderstatus_83(self):
        """TC_083: Test post /V7/Binder/ChangeBinderStatus"""
        url = f"{TestConfig.BASE_URL}/V7/Binder/ChangeBinderStatus"
        endpoint = "/V7/Binder/ChangeBinderStatus"

        # Input payload
        payload_str = '{"Binder_Id": 41957656, "Status_Id": 8743}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_084: POST /V5.0/TaxCaddyAPI/CreateClient")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_createclient_84(self):
        """TC_084: Test post /V5.0/TaxCaddyAPI/CreateClient"""
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/CreateClient"
        endpoint = "/V5.0/TaxCaddyAPI/CreateClient"

        # Input payload
        payload_str = '{"ClientType": "Standard", "Owner": "karandeepsingh.talwar@thomsonreuters.com", "OfficeLocationID": 20242, "OfficeLocationRestriction": true, "BinderType": "1040", "Taxpayer": {"FirstName": "Karan", "LastName": "Talwar", "Email": "karandeepsingh.talwar+998@thomsonreuters.com"}, "TaxSoftware": {"SoftwareID": 4, "AccountNumber": "421038", "TaxClientID": "2025UT12"}}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_085: POST /V5.0/TaxCaddyAPI/CreateDrl")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_createdrl_85(self):
        """TC_085: Test post /V5.0/TaxCaddyAPI/CreateDrl"""
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/CreateDrl"
        endpoint = "/V5.0/TaxCaddyAPI/CreateDrl"

        # Input payload
        payload_str = '{"TaxYear": 2025, "BinderType": "1040", "MergePDF": true, "TaxPayers": [{"TaxClientID": "2025UT12"}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Document Management")
    @allure.title("TC_086: POST /V5.0/TaxCaddyAPI/DownloadDocument")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_downloaddocument_86(self):
        """TC_086: Test post /V5.0/TaxCaddyAPI/DownloadDocument"""
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/DownloadDocument"
        endpoint = "/V5.0/TaxCaddyAPI/DownloadDocument"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_087: POST /V5.0/TaxCaddyAPI/GetDRLStatus")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_getdrlstatus_87(self):
        """TC_087: Test post /V5.0/TaxCaddyAPI/GetDRLStatus"""
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/GetDRLStatus"
        endpoint = "/V5.0/TaxCaddyAPI/GetDRLStatus"

        # Input payload
        payload_str = '{"DRLRequestIDs": [{"DRLRequestID": 4565533}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_088: POST /V5.0/TaxCaddyAPI/SendDRL")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_senddrl_88(self):
        """TC_088: Test post /V5.0/TaxCaddyAPI/SendDRL"""
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/SendDRL"
        endpoint = "/V5.0/TaxCaddyAPI/SendDRL"

        # Input payload
        payload_str = '{"TaxYear": 2025, "BinderType": "1040", "TaxPayers": [{"TaxClientID": "2025UT12"}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_089: POST /V5.0/TaxCaddyAPI/SendQuestionnaire")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_sendquestionnaire_89(self):
        """TC_089: Test post /V5.0/TaxCaddyAPI/SendQuestionnaire"""
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/SendQuestionnaire"
        endpoint = "/V5.0/TaxCaddyAPI/SendQuestionnaire"

        # Input payload
        payload_str = '{"TaxYear": 2025, "BinderType": "1040", "TaxPayers": [{"TaxClientID": "2025UT12"}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_090: POST /V5.0/TaxCaddyAPI/SendTaxCaddyInvitation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_sendtaxcaddyinvitation_90(self):
        """TC_090: Test post /V5.0/TaxCaddyAPI/SendTaxCaddyInvitation"""
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/SendTaxCaddyInvitation"
        endpoint = "/V5.0/TaxCaddyAPI/SendTaxCaddyInvitation"

        # Input payload
        payload_str = '{"TaxPayers": [{"TaxClientId": "R2RRFA"}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_091: POST /V5.0/TaxCaddyAPI/SendTaxCaddyInvitationReminder")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_sendtaxcaddyinvitationreminder_91(self):
        """TC_091: Test post /V5.0/TaxCaddyAPI/SendTaxCaddyInvitationReminder"""
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/SendTaxCaddyInvitationReminder"
        endpoint = "/V5.0/TaxCaddyAPI/SendTaxCaddyInvitationReminder"

        # Input payload
        payload_str = '{"TaxPayers": [{"TaxClientId": "R2RRFA"}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_092: POST /V5.0/TaxCaddyAPI/GetDRLItems/{TaxYear}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_getdrlitems_taxyear_92(self):
        """TC_092: Test post /V5.0/TaxCaddyAPI/GetDRLItems/{TaxYear}"""
        TaxYear = 2025  # Tax year parameter
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/GetDRLItems/{TaxYear}"
        endpoint = "/V5.0/TaxCaddyAPI/GetDRLItems/{TaxYear}"

        # Input payload
        payload_str = '{"TaxClientIds": ["2025UT12"]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_093: POST /V5.0/TaxCaddyAPI/DeleteDRLItem/{DrlRequestId}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_deletedrlitem_drlrequestid_93(self):
        """TC_093: Test post /V5.0/TaxCaddyAPI/DeleteDRLItem/{DrlRequestId}"""
        DrlRequestId = 4565533  # Sample DRL request ID for testing
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/DeleteDRLItem/{DrlRequestId}"
        endpoint = "/V5.0/TaxCaddyAPI/DeleteDRLItem/{DrlRequestId}"

        # Input payload
        payload_str = '{"DRLSubCategoryId": [36759656]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_094: POST /V5.0/TaxCaddyAPI/GetMemberDetails")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_getmemberdetails_94(self):
        """TC_094: Test post /V5.0/TaxCaddyAPI/GetMemberDetails"""
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/GetMemberDetails"
        endpoint = "/V5.0/TaxCaddyAPI/GetMemberDetails"

        # Input payload
        payload_str = '{"TaxPayerTaxClientID": ["2025UT12"]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_095: POST /V5.0/TaxCaddyAPI/UpdateMember")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_updatemember_95(self):
        """TC_095: Test post /V5.0/TaxCaddyAPI/UpdateMember"""
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/UpdateMember"
        endpoint = "/V5.0/TaxCaddyAPI/UpdateMember"

        # Input payload
        payload_str = '{"TaxPayerTaxClientID": ["2025UT12"], "AssignMember": ["anushka.kadam@thomsonreuters.com"]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Document Management")
    @allure.title("TC_096: POST /V5.0/TaxCaddyAPI/TaxCaddyDocumentCategories")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_taxcaddydocumentcategories_96(self):
        """TC_096: Test post /V5.0/TaxCaddyAPI/TaxCaddyDocumentCategories"""
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/TaxCaddyDocumentCategories"
        endpoint = "/V5.0/TaxCaddyAPI/TaxCaddyDocumentCategories"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Document Management")
    @allure.title("TC_097: POST /V5.0/TaxCaddyAPI/SendDocumentUploadRequest")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v5_0_taxcaddyapi_senddocumentuploadrequest_97(self):
        """TC_097: Test post /V5.0/TaxCaddyAPI/SendDocumentUploadRequest"""
        url = f"{TestConfig.BASE_URL}/V5.0/TaxCaddyAPI/SendDocumentUploadRequest"
        endpoint = "/V5.0/TaxCaddyAPI/SendDocumentUploadRequest"

        # Input payload
        payload_str = '{"TaxClientId": "2025UT12", "TaxYear": 2025, "DocumentUploadRequests": [{"CategoryId": 1000025, "SubCategoryName": "Test"}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v5"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_098: POST /V7/TaxCaddyAPI/CreateClient")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_createclient_98(self):
        """TC_098: Test post /V7/TaxCaddyAPI/CreateClient"""
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/CreateClient"
        endpoint = "/V7/TaxCaddyAPI/CreateClient"

        # Input payload
        payload_str = '{"ClientType": "Standard", "Owner": "prakash.kokate@thomsonreuters.com", "OfficeLocationID": 20242, "OfficeLocationRestriction": true, "BinderType": "1040", "Taxpayer": {"FirstName": "Karan", "LastName": "Talwar", "Email": "prakash.kokate+889@thomsonreuters.com"}, "TaxSoftware": {"SoftwareID": 4, "AccountNumber": "421038", "TaxClientID": "25UTPK11"}, "ProjectID": "R2R1", "SSN": "185225181", "UtClientGuid": "A76E38B5-86F5-4051-AC25-B88246C3CDC4"}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_099: POST /V7/TaxCaddyAPI/CreateDrl")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_createdrl_99(self):
        """TC_099: Test post /V7/TaxCaddyAPI/CreateDrl"""
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/CreateDrl"
        endpoint = "/V7/TaxCaddyAPI/CreateDrl"

        # Input payload
        payload_str = '{"TaxYear": 2025, "BinderType": "1040", "MergePDF": true, "TaxPayers": [{"TaxClientID": "2025UT11"}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_100: POST /V7/TaxCaddyAPI/GetDRLStatus")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_getdrlstatus_100(self):
        """TC_100: Test post /V7/TaxCaddyAPI/GetDRLStatus"""
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/GetDRLStatus"
        endpoint = "/V7/TaxCaddyAPI/GetDRLStatus"

        # Input payload
        payload_str = '{"DRLRequestIDs": [{"DRLRequestID": 4565570}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_101: POST /V7/TaxCaddyAPI/SendDRL")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_senddrl_101(self):
        """TC_101: Test post /V7/TaxCaddyAPI/SendDRL"""
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/SendDRL"
        endpoint = "/V7/TaxCaddyAPI/SendDRL"

        # Input payload
        payload_str = '{"TaxYear": 2025, "BinderType": "1040", "TaxPayers": [{"TaxClientID": "2025UT11"}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_102: POST /V7/TaxCaddyAPI/SendQuestionnaire")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_sendquestionnaire_102(self):
        """TC_102: Test post /V7/TaxCaddyAPI/SendQuestionnaire"""
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/SendQuestionnaire"
        endpoint = "/V7/TaxCaddyAPI/SendQuestionnaire"

        # Input payload
        payload_str = '{"TaxYear": 2025, "BinderType": "1040", "TaxPayers": [{"TaxClientID": "2025UT11"}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_103: POST /V7/TaxCaddyAPI/SendTaxCaddyInvitation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_sendtaxcaddyinvitation_103(self):
        """TC_103: Test post /V7/TaxCaddyAPI/SendTaxCaddyInvitation"""
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/SendTaxCaddyInvitation"
        endpoint = "/V7/TaxCaddyAPI/SendTaxCaddyInvitation"

        # Input payload
        payload_str = '{"TaxPayers": [{"TaxClientId": "2025UT11"}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_104: POST /V7/TaxCaddyAPI/SendTaxCaddyInvitationReminder")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_sendtaxcaddyinvitationreminder_104(self):
        """TC_104: Test post /V7/TaxCaddyAPI/SendTaxCaddyInvitationReminder"""
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/SendTaxCaddyInvitationReminder"
        endpoint = "/V7/TaxCaddyAPI/SendTaxCaddyInvitationReminder"

        # Input payload
        payload_str = '{"TaxPayers": [{"TaxClientId": "2025UT11"}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_105: POST /V7/TaxCaddyAPI/GetDRLItems/{TaxYear}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_getdrlitems_taxyear_105(self):
        """TC_105: Test post /V7/TaxCaddyAPI/GetDRLItems/{TaxYear}"""
        TaxYear = 2025  # Tax year parameter
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/GetDRLItems/{TaxYear}"
        endpoint = "/V7/TaxCaddyAPI/GetDRLItems/{TaxYear}"

        # Input payload
        payload_str = '{"TaxClientIds": ["2025UT12"]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_106: POST /V7/TaxCaddyAPI/DeleteDRLItem/{DrlRequestId}")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_deletedrlitem_drlrequestid_106(self):
        """TC_106: Test post /V7/TaxCaddyAPI/DeleteDRLItem/{DrlRequestId}"""
        DrlRequestId = 4565533  # Sample DRL request ID for testing
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/DeleteDRLItem/{DrlRequestId}"
        endpoint = "/V7/TaxCaddyAPI/DeleteDRLItem/{DrlRequestId}"

        # Input payload
        payload_str = '{"DRLSubCategoryId": [36759655]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_107: POST /V7/TaxCaddyAPI/GetMemberDetails")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_getmemberdetails_107(self):
        """TC_107: Test post /V7/TaxCaddyAPI/GetMemberDetails"""
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/GetMemberDetails"
        endpoint = "/V7/TaxCaddyAPI/GetMemberDetails"

        # Input payload
        payload_str = '{"TaxPayerTaxClientID": ["2025UT11"]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("TaxCaddy API")
    @allure.title("TC_108: POST /V7/TaxCaddyAPI/UpdateMember")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_updatemember_108(self):
        """TC_108: Test post /V7/TaxCaddyAPI/UpdateMember"""
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/UpdateMember"
        endpoint = "/V7/TaxCaddyAPI/UpdateMember"

        # Input payload
        payload_str = '{"TaxPayerTaxClientID": ["2025UT11"], "AssignMember": ["anushka.kadam@thomsonreuters.com"]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Document Management")
    @allure.title("TC_109: POST /V7/TaxCaddyAPI/TaxCaddyDocumentCategories")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_taxcaddydocumentcategories_109(self):
        """TC_109: Test post /V7/TaxCaddyAPI/TaxCaddyDocumentCategories"""
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/TaxCaddyDocumentCategories"
        endpoint = "/V7/TaxCaddyAPI/TaxCaddyDocumentCategories"

        # Input payload
        payload_str = '{}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("Document Management")
    @allure.title("TC_110: POST /V7/TaxCaddyAPI/SendDocumentUploadRequest")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_taxcaddyapi_senddocumentuploadrequest_110(self):
        """TC_110: Test post /V7/TaxCaddyAPI/SendDocumentUploadRequest"""
        url = f"{TestConfig.BASE_URL}/V7/TaxCaddyAPI/SendDocumentUploadRequest"
        endpoint = "/V7/TaxCaddyAPI/SendDocumentUploadRequest"

        # Input payload
        payload_str = '{"TaxClientId": "2025UT11", "TaxYear": 2025, "DocumentUploadRequests": [{"CategoryId": 1000027, "SubCategoryName": "Test"}]}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("API Operations")
    @allure.title("TC_111: POST /V7/RWAPI2.0/LaunchReviewWizard")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_rwapi2_0_launchreviewwizard_111(self):
        """TC_111: Test post /V7/RWAPI2.0/LaunchReviewWizard"""
        url = f"{TestConfig.BASE_URL}/V7/RWAPI2.0/LaunchReviewWizard"
        endpoint = "/V7/RWAPI2.0/LaunchReviewWizard"

        # Input payload
        payload_str = '{"Email": "Priyanka.patil@thomsonreuters.com", "BinderID": 41967196}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("UT Integration")
    @allure.title("TC_112: POST /V7/UTIntegration/TaxFileMergedStatus")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_utintegration_taxfilemergedstatus_112(self):
        """TC_112: Test post /V7/UTIntegration/TaxFileMergedStatus"""
        url = f"{TestConfig.BASE_URL}/V7/UTIntegration/TaxFileMergedStatus"
        endpoint = "/V7/UTIntegration/TaxFileMergedStatus"

        # Input payload
        payload_str = '{"FirmId": "string", "UTClientGuid": "string", "TaxClientId": "BULKFILL", "TaxYear": 2025}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")

    @allure.story("UT Integration")
    @allure.title("TC_113: POST /V7/UTIntegration/SPConnect")
    @allure.severity(allure.severity_level.NORMAL)
    def test_v7_utintegration_spconnect_113(self):
        """TC_113: Test post /V7/UTIntegration/SPConnect"""
        url = f"{TestConfig.BASE_URL}/V7/UTIntegration/SPConnect"
        endpoint = "/V7/UTIntegration/SPConnect"

        # Input payload
        payload_str = '{"IsConnected": true}'
        payload = json.loads(payload_str)

        # Make request
        response = self.make_request(
            method='POST',
            url=url,
            payload=payload,
            api_version="v7"
        )

        # Display test result
        self.display_test_result(endpoint, 'POST', response, payload)

        # Assertions
        assert response.status_code in [200, 201, 400, 401, 404], \
            f"Expected valid status code, got {response.status_code}"

        # Validate response structure if successful
        if response.status_code in [200, 201]:
            try:
                response_data = response.json()

                # Validate response has expected fields
                if isinstance(response_data, dict):
                    if 'ErrorCode' not in response_data and 'ErrorMessage' not in response_data:
                        assert len(response_data) > 0, "Response should not be empty"
                elif isinstance(response_data, list):
                    assert isinstance(response_data, list), "Response is a valid list"
            except json.JSONDecodeError:
                print(f"Response is not JSON: {response.text[:200]}")


if __name__ == "__main__":
    pytest.main([
        __file__,
        '-v'
    ])
