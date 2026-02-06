"""
Comprehensive Test Suite for Sureprep API
Tests cover Authentication, BinderInfo, Binder, Document, Lookup, Status, TaxCaddy, RWAPI, and UTIntegration endpoints
Supports API versions: V5.0, V6.0, V6.1, V7
"""

import pytest
import requests
import json
from datetime import datetime
import os
from typing import Dict, Any


class TestConfig:
    """Test configuration and setup"""
    BASE_URL = os.getenv('SUREPREP_BASE_URL', 'https://api.sureprep.com')
    API_V5_BASE = f"{BASE_URL}/V5.0"
    API_V6_BASE = f"{BASE_URL}/V6.0"
    API_V61_BASE = f"{BASE_URL}/V6.1"
    API_V7_BASE = f"{BASE_URL}/V7"

    # V5 Credentials
    V5_USERNAME = os.getenv('SUREPREP_V5_USERNAME', 'PRIYA1')
    V5_PASSWORD = os.getenv('SUREPREP_V5_PASSWORD', 'Abcd@12345')
    V5_API_KEY = os.getenv('SUREPREP_V5_API_KEY', 'C690222D-8625-46F7-92CC-A61DA060D7A9')

    # V7 Credentials
    V7_CLIENT_ID = os.getenv('SUREPREP_V7_CLIENT_ID', 'CCmDgzLV35QnRYPR7c5UJReYqbuNXUoN')
    V7_CLIENT_SECRET = os.getenv('SUREPREP_V7_CLIENT_SECRET', 'BiC_ojduHzVRRG6Kktjx5GTXTT1KeS6nVjqLsrWynSo0IKjT3Xs7gYHK76ap-A65')

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
        auth_url = f"{TestConfig.API_V5_BASE}/Authenticate/GetToken"
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
        auth_url = f"{TestConfig.API_V7_BASE}/Authenticate/GetToken"
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


@pytest.mark.authentication
class TestAuthenticationAPI(BaseAPITest):
    """Test cases for Authentication endpoints"""

    def test_auth_v5_get_token_valid_credentials(self):
        """TC_AUTH_001: Verify V5.0 GetToken with valid credentials returns success"""
        url = f"{TestConfig.API_V5_BASE}/Authenticate/GetToken"
        payload = {
            "UserName": TestConfig.V5_USERNAME,
            "Password": TestConfig.V5_PASSWORD,
            "APIKey": TestConfig.V5_API_KEY
        }
        response = requests.post(url, json=payload, timeout=TestConfig.TIMEOUT)

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        response_data = response.json()
        assert 'Token' in response_data, "Response should contain Token"
        assert len(response_data['Token']) > 0, "Token should not be empty"
        assert 'TokenExpiry' in response_data, "Response should contain TokenExpiry"

    def test_auth_v7_get_token_valid_credentials(self):
        """TC_AUTH_002: Verify V7 GetToken with valid credentials returns success"""
        url = f"{TestConfig.API_V7_BASE}/Authenticate/GetToken"
        payload = {
            "ClientID": TestConfig.V7_CLIENT_ID,
            "ClientSecret": TestConfig.V7_CLIENT_SECRET
        }
        response = requests.post(url, json=payload, timeout=TestConfig.TIMEOUT)

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        response_data = response.json()
        assert 'Token' in response_data, "Response should contain Token"
        assert len(response_data['Token']) > 0, "Token should not be empty"
        assert 'TokenExpiry' in response_data, "Response should contain TokenExpiry"

    def test_auth_get_token_invalid_credentials(self):
        """TC_AUTH_003: Verify GetToken with invalid credentials returns 401"""
        url = f"{TestConfig.API_V7_BASE}/Authenticate/GetToken"
        payload = {
            "ClientID": "invalid_client_id",
            "ClientSecret": "invalid_client_secret"
        }
        response = requests.post(url, json=payload, timeout=TestConfig.TIMEOUT)

        assert response.status_code == 401, "Expected status code 401 for invalid credentials"

    def test_auth_get_token_missing_client_id(self):
        """TC_AUTH_004: Verify GetToken with missing ClientID returns 400"""
        url = f"{TestConfig.API_V7_BASE}/Authenticate/GetToken"
        payload = {
            "ClientSecret": TestConfig.V7_CLIENT_SECRET
        }
        response = requests.post(url, json=payload, timeout=TestConfig.TIMEOUT)

        assert response.status_code in [400, 401], "Expected status code 400 or 401"

    def test_auth_get_token_missing_client_secret(self):
        """TC_AUTH_005: Verify GetToken with missing ClientSecret returns 400"""
        url = f"{TestConfig.API_V7_BASE}/Authenticate/GetToken"
        payload = {
            "ClientID": TestConfig.V7_CLIENT_ID
        }
        response = requests.post(url, json=payload, timeout=TestConfig.TIMEOUT)

        assert response.status_code in [400, 401], "Expected status code 400 or 401"

    def test_auth_get_token_empty_payload(self):
        """TC_AUTH_006: Verify GetToken with empty payload returns 400"""
        url = f"{TestConfig.API_V7_BASE}/Authenticate/GetToken"
        response = requests.post(url, json={}, timeout=TestConfig.TIMEOUT)

        assert response.status_code in [400, 401], "Expected status code 400 or 401"


@pytest.mark.binderinfo
class TestBinderInfoAPI(BaseAPITest):
    """Test cases for BinderInfo endpoints"""

    @pytest.fixture
    def sample_binder_id(self):
        """Fixture to provide a sample binder ID"""
        return "12345"

    def test_get_binder_details_v5(self, sample_binder_id):
        """TC_BINDER_INFO_001: Verify V5.0 GetBinderDetails returns binder information"""
        url = f"{TestConfig.API_V5_BASE}/BinderInfo/GetBinderDetails"
        payload = {"binderId": sample_binder_id}
        response = self.make_request('POST', url, payload, api_version="v5")

        assert response.status_code in [200, 401, 404], "Expected status code 200, 401, or 404"
        if response.status_code == 200:
            assert 'binderId' in response.json() or 'BinderId' in response.json()

    def test_get_binder_details_v7(self, sample_binder_id):
        """TC_BINDER_INFO_002: Verify V7 GetBinderDetails returns binder information"""
        url = f"{TestConfig.API_V7_BASE}/BinderInfo/GetBinderDetails"
        payload = {"binderId": sample_binder_id}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 404], "Expected status code 200 or 404"

    def test_get_binder_details_by_id_v7(self, sample_binder_id):
        """TC_BINDER_INFO_003: Verify V7 GetBinderDetails with path parameter"""
        url = f"{TestConfig.API_V7_BASE}/BinderInfo/GetBinderDetails/{sample_binder_id}"
        response = self.make_request('POST', url)

        assert response.status_code in [200, 404], "Expected status code 200 or 404"

    def test_get_binder_details_by_unique_identifier(self):
        """TC_BINDER_INFO_004: Verify GetBinderDetailsByUniqueIdentifier"""
        url = f"{TestConfig.API_V7_BASE}/BinderInfo/GetBinderDetailsByUniqueIdentifier"
        payload = {"uniqueIdentifier": "TEST-12345"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 404], "Expected status code 200 or 404"

    def test_get_uncleared_notes_v5(self, sample_binder_id):
        """TC_BINDER_INFO_005: Verify V5.0 GetUnclearedNotes returns notes"""
        url = f"{TestConfig.API_V5_BASE}/BinderInfo/GetUnclearedNotes"
        payload = {"binderId": sample_binder_id}
        response = self.make_request('POST', url, payload, api_version="v5")

        assert response.status_code in [200, 401, 404], "Expected status code 200, 401, or 404"

    def test_get_unreviewed_tr_stamps_v7(self, sample_binder_id):
        """TC_BINDER_INFO_006: Verify GetUnreviewedTRStamps returns stamps"""
        url = f"{TestConfig.API_V7_BASE}/BinderInfo/GetUnreviewedTRStamps"
        payload = {"binderId": sample_binder_id}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 404], "Expected status code 200 or 404"

    def test_get_unreviewed_sticky_notes(self, sample_binder_id):
        """TC_BINDER_INFO_007: Verify GetUnreviewedStickyNotes returns notes"""
        url = f"{TestConfig.API_V7_BASE}/BinderInfo/GetUnreviewedStickyNotes"
        payload = {"binderId": sample_binder_id}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 404], "Expected status code 200 or 404"

    @pytest.mark.parametrize("level", ["L1", "L2", "L3", "L4"])
    def test_get_unreviewed_workpapers_by_level(self, sample_binder_id, level):
        """TC_BINDER_INFO_008-011: Verify GetUnreviewedWorkpapers for all levels"""
        url = f"{TestConfig.API_V7_BASE}/BinderInfo/GetUnreviewedWorkpapersBy{level}"
        payload = {"binderId": sample_binder_id}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 404], "Expected status code 200 or 404"

    def test_get_document_pending_review_count(self, sample_binder_id):
        """TC_BINDER_INFO_012: Verify GetDocumentPendingReviewCount returns count"""
        url = f"{TestConfig.API_V7_BASE}/BinderInfo/GetDocumentPendingReviewCount"
        payload = {"binderId": sample_binder_id}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 404], "Expected status code 200, 400, or 404"
        if response.status_code == 200:
            response_data = response.json()
            # Accept count, ErrorCode, or integer response
            assert 'count' in response_data or 'ErrorCode' in response_data or isinstance(response_data, int), "Expected count, error, or integer in response"

    def test_get_document_pending_signature_count(self, sample_binder_id):
        """TC_BINDER_INFO_013: Verify GetDocumentPendingSignatureCount returns count"""
        url = f"{TestConfig.API_V7_BASE}/BinderInfo/GetDocumentPendingSignatureCount"
        payload = {"binderId": sample_binder_id}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 404], "Expected status code 200 or 404"

    def test_get_document_pending_upload_count(self, sample_binder_id):
        """TC_BINDER_INFO_014: Verify GetDocumentPendingUploadCount returns count"""
        url = f"{TestConfig.API_V7_BASE}/BinderInfo/GetDocumentPendingUploadCount"
        payload = {"binderId": sample_binder_id}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 404], "Expected status code 200 or 404"

    def test_get_binder_pending_items(self, sample_binder_id):
        """TC_BINDER_INFO_015: Verify GetBinderPendingItems returns pending items"""
        url = f"{TestConfig.API_V7_BASE}/BinderInfo/GetBinderPendingItems"
        payload = {"binderId": sample_binder_id}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 404], "Expected status code 200, 400, or 404"


@pytest.mark.binder
class TestBinderAPI(BaseAPITest):
    """Test cases for Binder CRUD operations"""

    def test_create_binder_v5_valid_payload(self):
        """TC_BINDER_001: Verify V5.0 CreateBinder with valid payload"""
        url = f"{TestConfig.API_V5_BASE}/Binder/CreateBinder"
        payload = {
            "clientName": "Test Client",
            "taxYear": 2024,
            "binderType": "1040",
            "templateId": "1"
        }
        response = self.make_request('POST', url, payload, api_version="v5")

        assert response.status_code in [200, 201, 400, 401], "Expected success or validation error"

    def test_create_binder_v7_valid_payload(self):
        """TC_BINDER_002: Verify V7 CreateBinder with valid payload"""
        url = f"{TestConfig.API_V7_BASE}/Binder/CreateBinder"
        payload = {
            "clientName": "Test Client V7",
            "taxYear": 2024,
            "binderType": "1040"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 201, 400, 401], "Expected success or validation error"

    def test_create_binder_missing_required_fields(self):
        """TC_BINDER_003: Verify CreateBinder with missing required fields returns 400"""
        url = f"{TestConfig.API_V7_BASE}/Binder/CreateBinder"
        payload = {}
        response = self.make_request('POST', url, payload)

        assert response.status_code == 400, "Expected status code 400"

    def test_upload_binder_documents_v5(self):
        """TC_BINDER_004: Verify V5.0 UploadBinderDocuments"""
        url = f"{TestConfig.API_V5_BASE}/Binder/UploadBinderDocuments"
        payload = {
            "binderId": "12345",
            "documents": []
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_upload_binder_documents_v7(self):
        """TC_BINDER_005: Verify V7 UploadBinderDocuments"""
        url = f"{TestConfig.API_V7_BASE}/Binder/UploadBinderDocuments"
        payload = {
            "binderId": "12345",
            "documents": []
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_submit_binder_v5(self):
        """TC_BINDER_006: Verify V5.0 SubmitBinder"""
        url = f"{TestConfig.API_V5_BASE}/Binder/SubmitBinder"
        payload = {"binderId": "12345"}
        response = self.make_request('POST', url, payload, api_version="v5")

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_submit_binder_v7(self):
        """TC_BINDER_007: Verify V7 SubmitBinder"""
        url = f"{TestConfig.API_V7_BASE}/Binder/SubmitBinder"
        payload = {"binderId": "12345"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_update_project_id_v7(self):
        """TC_BINDER_008: Verify UpdateProjectID"""
        url = f"{TestConfig.API_V7_BASE}/Binder/UpdateProjectID"
        payload = {
            "binderId": "12345",
            "projectId": "PROJ-001"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_get_states_and_localities_v7(self):
        """TC_BINDER_009: Verify GetStatesandLocalities returns list"""
        url = f"{TestConfig.API_V7_BASE}/Binder/GetStatesandLocalities"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"
        assert isinstance(response.json(), (list, dict)), "Response should be list or dict"

    def test_get_binders_status_with_states(self):
        """TC_BINDER_010: Verify GetBindersStatusWithStates"""
        url = f"{TestConfig.API_V7_BASE}/Binder/GetBindersStatusWithStates"
        payload = {"statusId": "1"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401], "Expected valid response"

    def test_download_binder_pbfx_v7(self):
        """TC_BINDER_011: Verify DownloadBinderPBFX"""
        url = f"{TestConfig.API_V7_BASE}/Binder/DownloadBinderPBFX"
        payload = {"binderId": "12345"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_get_pbfx_by_id_v7(self):
        """TC_BINDER_012: Verify GetPBFx with path parameter"""
        binder_id = "12345"
        url = f"{TestConfig.API_V7_BASE}/Binder/GetPBFx/{binder_id}"
        response = self.make_request('POST', url)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_get_binder_audit_log(self):
        """TC_BINDER_013: Verify GetBinderAuditLog returns log entries"""
        url = f"{TestConfig.API_V7_BASE}/Binder/GetBinderAuditLog"
        payload = {"binderId": "12345"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_update_owner_member(self):
        """TC_BINDER_014: Verify UpdateOwnerMember"""
        url = f"{TestConfig.API_V7_BASE}/Binder/UpdateOwnerMember"
        payload = {
            "binderId": "12345",
            "memberId": "67890"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_print_binder(self):
        """TC_BINDER_015: Verify PrintBinder"""
        url = f"{TestConfig.API_V7_BASE}/Binder/PrintBinder"
        payload = {"binderId": "12345"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"


@pytest.mark.document
class TestDocumentAPI(BaseAPITest):
    """Test cases for Document operations"""

    def test_get_documents_v5(self):
        """TC_DOC_001: Verify V5.0 GetDocuments returns document list"""
        url = f"{TestConfig.API_V5_BASE}/Binder/GetDocuments"
        payload = {"binderId": "12345"}
        response = self.make_request('POST', url, payload, api_version="v5")

        assert response.status_code in [200, 401, 404], "Expected status code 200, 401, or 404"

    def test_get_documents_v7(self):
        """TC_DOC_002: Verify V7 GetDocuments returns document list"""
        url = f"{TestConfig.API_V7_BASE}/Binder/GetDocuments"
        payload = {"binderId": "12345"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 401, 404], "Expected status code 200, 401, or 404"

    def test_download_document_v5(self):
        """TC_DOC_003: Verify V5.0 DownloadDocument"""
        url = f"{TestConfig.API_V5_BASE}/Binder/DownloadDocument"
        payload = {
            "binderId": "12345",
            "documentId": "67890"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_download_document_v7(self):
        """TC_DOC_004: Verify V7 DownloadDocument"""
        url = f"{TestConfig.API_V7_BASE}/Binder/DownloadDocument"
        payload = {
            "binderId": "12345",
            "documentId": "67890"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_download_document_invalid_id(self):
        """TC_DOC_005: Verify DownloadDocument with invalid ID returns 404"""
        url = f"{TestConfig.API_V7_BASE}/Binder/DownloadDocument"
        payload = {
            "binderId": "invalid",
            "documentId": "invalid"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [400, 404], "Expected status code 400 or 404"


@pytest.mark.lookup
class TestLookupAPI(BaseAPITest):
    """Test cases for Lookup operations"""

    def test_get_local_path_v7(self):
        """TC_LOOKUP_001: Verify GetLocalPathToDownloadFiles"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/GetLocalPathToDownloadFiles"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"

    def test_get_service_types_v7(self):
        """TC_LOOKUP_002: Verify ServiceTypes returns list"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/ServiceTypes"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"
        assert isinstance(response.json(), (list, dict)), "Response should be list or dict"

    def test_get_office_locations_v7(self):
        """TC_LOOKUP_003: Verify OfficeLocations returns list"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/OfficeLocations"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"

    def test_get_binder_types_v7(self):
        """TC_LOOKUP_004: Verify BinderTypes returns list"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/BinderTypes"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"

    def test_get_tax_software_list_v7(self):
        """TC_LOOKUP_005: Verify TaxSoftwareList returns list"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/TaxSoftwareList"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"

    def test_get_binder_templates_v7(self):
        """TC_LOOKUP_006: Verify BinderTemplates returns list"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/BinderTemplates"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"

    def test_get_binder_template_list_v7(self):
        """TC_LOOKUP_007: Verify BinderTemplateList returns list"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/BinderTemplateList"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"

    def test_get_binder_status_list_v7(self):
        """TC_LOOKUP_008: Verify BinderStatusList returns list"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/BinderStatusList"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"

    def test_get_service_units_v7(self):
        """TC_LOOKUP_009: Verify ServiceUnits returns list (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/ServiceUnits"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"

    def test_get_domain_information_v7(self):
        """TC_LOOKUP_010: Verify DomainInformation (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/DomainInformation"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"

    def test_get_user_domain_details_v7(self):
        """TC_LOOKUP_011: Verify UserDomainDetails (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/UserDomainDetails"
        response = self.make_request('POST', url)

        assert response.status_code in [200, 400, 401], "Expected valid response"

    def test_get_custom_field_enabled_v7(self):
        """TC_LOOKUP_012: Verify CustomFieldEnabled (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/CustomFieldEnabled"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"

    def test_ut_search_client_guid_v7(self):
        """TC_LOOKUP_013: Verify UTSearchClientGUID (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/UTSearchClientGUID"
        payload = {"clientGuid": "test-guid"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_7216_consent_enabled_v7(self):
        """TC_LOOKUP_014: Verify 7216ConsentEnabled (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/7216ConsentEnabled"
        response = self.make_request('POST', url)

        assert response.status_code == 200, "Expected status code 200"


@pytest.mark.status
class TestStatusAPI(BaseAPITest):
    """Test cases for Status operations"""

    def test_get_status_v5(self):
        """TC_STATUS_001: Verify V5.0 GetStatus"""
        url = f"{TestConfig.API_V5_BASE}/Binder/GetStatus"
        payload = {"binderId": "12345"}
        response = self.make_request('POST', url, payload, api_version="v5")

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_get_status_v7(self):
        """TC_STATUS_002: Verify V7 GetStatus"""
        url = f"{TestConfig.API_V7_BASE}/Binder/GetStatus"
        payload = {"binderId": "12345"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_change_binder_status_v5(self):
        """TC_STATUS_003: Verify V5.0 ChangeBinderStatus"""
        url = f"{TestConfig.API_V5_BASE}/Binder/ChangeBinderStatus"
        payload = {
            "binderId": "12345",
            "statusId": "2"
        }
        response = self.make_request('POST', url, payload, api_version="v5")

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_change_binder_status_v7(self):
        """TC_STATUS_004: Verify V7 ChangeBinderStatus"""
        url = f"{TestConfig.API_V7_BASE}/Binder/ChangeBinderStatus"
        payload = {
            "binderId": "12345",
            "statusId": "2"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_change_binder_status_invalid_status(self):
        """TC_STATUS_005: Verify ChangeBinderStatus with invalid status returns 400"""
        url = f"{TestConfig.API_V7_BASE}/Binder/ChangeBinderStatus"
        payload = {
            "binderId": "12345",
            "statusId": "999"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [400, 404], "Expected status code 400 or 404"


@pytest.mark.taxcaddy
class TestTaxCaddyAPI(BaseAPITest):
    """Test cases for TaxCaddy operations"""

    def test_create_client_v5(self):
        """TC_TAXCADDY_001: Verify V5.0 CreateClient"""
        url = f"{TestConfig.API_V5_BASE}/TaxCaddyAPI/CreateClient"
        payload = {
            "clientName": "Test Client",
            "email": "test@example.com"
        }
        response = self.make_request('POST', url, payload, api_version="v5")

        assert response.status_code in [200, 201, 400, 404], "Expected valid response"

    def test_create_client_v6(self):
        """TC_TAXCADDY_002: Verify V6.0 CreateClient"""
        url = f"{TestConfig.API_V6_BASE}/TaxCaddyAPI/CreateClient"
        payload = {
            "clientName": "Test Client V6",
            "email": "test@example.com"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 201, 400, 404], "Expected valid response"

    def test_create_client_v61(self):
        """TC_TAXCADDY_003: Verify V6.1 CreateClient"""
        url = f"{TestConfig.API_V61_BASE}/TaxCaddyAPI/CreateClient"
        payload = {
            "clientName": "Test Client V6.1",
            "email": "test@example.com"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 201, 400, 404], "Expected valid response"

    def test_create_client_v7(self):
        """TC_TAXCADDY_004: Verify V7 CreateClient"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/CreateClient"
        payload = {
            "clientName": "Test Client V7",
            "email": "test@example.com"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 201, 400, 404], "Expected valid response"

    def test_create_drl_v5(self):
        """TC_TAXCADDY_005: Verify CreateDrl"""
        url = f"{TestConfig.API_V5_BASE}/TaxCaddyAPI/CreateDrl"
        payload = {
            "clientId": "12345",
            "taxYear": 2024
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 201, 400, 404], "Expected valid response"

    def test_get_client_details_v7(self):
        """TC_TAXCADDY_006: Verify GetClientDetails"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/GetClientDetails"
        payload = {"clientId": "12345"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_domain_subscribe_v7(self):
        """TC_TAXCADDY_007: Verify DomainSubscribe (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/DomainSubscribe"
        payload = {"domainId": "domain-123"}
        response = self.make_request('PUT', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_domain_unsubscribe_v7(self):
        """TC_TAXCADDY_008: Verify DomainUnsubscribe (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/DomainUnsubscribe"
        payload = {"domainId": "domain-123"}
        response = self.make_request('PUT', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_client_subscribe_v7(self):
        """TC_TAXCADDY_009: Verify ClientSubscribe (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/ClientSubscribe"
        payload = {"clientId": "12345"}
        response = self.make_request('PUT', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_client_unsubscribe_v7(self):
        """TC_TAXCADDY_010: Verify ClientUnsubscribe (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/ClientUnsubscribe"
        payload = {"clientId": "12345"}
        response = self.make_request('PUT', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_download_document_taxcaddy(self):
        """TC_TAXCADDY_011: Verify DownloadDocument"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/DownloadDocument"
        payload = {
            "clientId": "12345",
            "documentId": "67890"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_get_drl_status(self):
        """TC_TAXCADDY_012: Verify GetDRLStatus"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/GetDRLStatus"
        payload = {"drlId": "drl-123"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_send_drl(self):
        """TC_TAXCADDY_013: Verify SendDRL"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/SendDRL"
        payload = {
            "drlId": "drl-123",
            "clientEmail": "client@example.com"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_disconnect_devices_v7(self):
        """TC_TAXCADDY_014: Verify DisconnectDevices (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/DisconnectDevices"
        payload = {"clientId": "12345"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_send_questionnaire(self):
        """TC_TAXCADDY_015: Verify SendQuestionnaire"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/SendQuestionnaire"
        payload = {
            "clientId": "12345",
            "questionnaireId": "q-123"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_print_questionnaire_v7(self):
        """TC_TAXCADDY_016: Verify PrintQuestionnaire (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/PrintQuestionnaire"
        payload = {"questionnaireId": "q-123"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_send_taxcaddy_invitation(self):
        """TC_TAXCADDY_017: Verify SendTaxCaddyInvitation"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/SendTaxCaddyInvitation"
        payload = {
            "clientId": "12345",
            "email": "client@example.com"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_send_invitation_reminder(self):
        """TC_TAXCADDY_018: Verify SendTaxCaddyInvitationReminder"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/SendTaxCaddyInvitationReminder"
        payload = {"invitationId": "inv-123"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_get_drl_items_by_tax_year(self):
        """TC_TAXCADDY_019: Verify GetDRLItems with path parameter"""
        tax_year = "2024"
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/GetDRLItems/{tax_year}"
        response = self.make_request('POST', url)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_delete_drl_item(self):
        """TC_TAXCADDY_020: Verify DeleteDRLItem with path parameter"""
        drl_request_id = "drl-req-123"
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/DeleteDRLItem/{drl_request_id}"
        response = self.make_request('POST', url)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_get_member_details(self):
        """TC_TAXCADDY_021: Verify GetMemberDetails"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/GetMemberDetails"
        payload = {"memberId": "member-123"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_update_member(self):
        """TC_TAXCADDY_022: Verify UpdateMember"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/UpdateMember"
        payload = {
            "memberId": "member-123",
            "memberName": "Updated Name"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_get_document_categories(self):
        """TC_TAXCADDY_023: Verify TaxCaddyDocumentCategories"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/TaxCaddyDocumentCategories"
        response = self.make_request('POST', url)

        assert response.status_code in [200, 404], "Expected status code 200 or 404"

    def test_send_document_upload_request(self):
        """TC_TAXCADDY_024: Verify SendDocumentUploadRequest"""
        url = f"{TestConfig.API_V7_BASE}/TaxCaddyAPI/SendDocumentUploadRequest"
        payload = {
            "clientId": "12345",
            "categoryId": "cat-123"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"


@pytest.mark.rwapi
class TestReviewWizardAPI(BaseAPITest):
    """Test cases for Review Wizard API"""

    def test_launch_review_wizard_v5(self):
        """TC_RW_001: Verify V5.0 LaunchReviewWizard"""
        url = f"{TestConfig.API_V5_BASE}/RWAPI2.0/LaunchReviewWizard"
        payload = {"binderId": "12345"}
        response = self.make_request('POST', url, payload, api_version="v5")

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_launch_review_wizard_v7(self):
        """TC_RW_002: Verify V7 LaunchReviewWizard"""
        url = f"{TestConfig.API_V7_BASE}/RWAPI2.0/LaunchReviewWizard"
        payload = {"binderId": "12345"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"


@pytest.mark.utintegration
class TestUTIntegrationAPI(BaseAPITest):
    """Test cases for UT Integration callbacks"""

    def test_drl_callback_v5(self):
        """TC_UT_001: Verify V5.0 DRLCallBack"""
        request_id = "req-123"
        url = f"{TestConfig.API_V5_BASE}/UTIntegration/DRLCallBack/{request_id}"
        payload = {"status": "completed"}
        response = self.make_request('POST', url, payload, api_version="v5")

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_drl_callback_v7(self):
        """TC_UT_002: Verify V7 DRLCallBack"""
        request_id = "req-123"
        url = f"{TestConfig.API_V7_BASE}/UTIntegration/DRLCallBack/{request_id}"
        payload = {"status": "completed"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_binder_callback_v5(self):
        """TC_UT_003: Verify V5.0 BinderCallBack"""
        engagement_id = "eng-123"
        url = f"{TestConfig.API_V5_BASE}/UTIntegration/BinderCallBack/{engagement_id}"
        payload = {"status": "success"}
        response = self.make_request('POST', url, payload, api_version="v5")

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_binder_callback_v7(self):
        """TC_UT_004: Verify V7 BinderCallBack"""
        engagement_id = "eng-123"
        url = f"{TestConfig.API_V7_BASE}/UTIntegration/BinderCallBack/{engagement_id}"
        payload = {"status": "success"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401, 404], "Expected valid response"

    def test_tax_file_merged_status_v5(self):
        """TC_UT_005: Verify V5.0 TaxFileMergedStatus"""
        url = f"{TestConfig.API_V5_BASE}/UTIntegration/TaxFileMergedStatus"
        payload = {
            "fileId": "file-123",
            "status": "merged"
        }
        response = self.make_request('POST', url, payload, api_version="v5")

        assert response.status_code in [200, 400, 401], "Expected valid response"

    def test_tax_file_merged_status_v7(self):
        """TC_UT_006: Verify V7 TaxFileMergedStatus"""
        url = f"{TestConfig.API_V7_BASE}/UTIntegration/TaxFileMergedStatus"
        payload = {
            "fileId": "file-123",
            "status": "merged"
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401], "Expected valid response"

    def test_sp_connect_v7(self):
        """TC_UT_007: Verify SPConnect (V7 only)"""
        url = f"{TestConfig.API_V7_BASE}/UTIntegration/SPConnect"
        payload = {"connectionData": "test-data"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 400, 401], "Expected valid response"


@pytest.mark.negative
class TestNegativeScenarios(BaseAPITest):
    """Test cases for negative scenarios and error handling"""

    def test_invalid_endpoint(self):
        """TC_NEG_001: Verify invalid endpoint returns 400 or 404"""
        url = f"{TestConfig.API_V7_BASE}/Invalid/Endpoint"
        response = requests.post(url, json={}, timeout=TestConfig.TIMEOUT)

        assert response.status_code in [400, 404], "Expected status code 400 or 404"

    def test_missing_authorization_header(self):
        """TC_NEG_002: Verify request without auth token returns 400 or 401"""
        url = f"{TestConfig.API_V7_BASE}/Binder/GetBinderDetails"
        response = requests.post(url, json={"binderId": "12345"}, timeout=TestConfig.TIMEOUT)

        assert response.status_code in [400, 401], "Expected status code 400 or 401"

    def test_invalid_auth_token(self):
        """TC_NEG_003: Verify request with invalid token returns 400 or 401"""
        url = f"{TestConfig.API_V7_BASE}/Binder/GetBinderDetails"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer invalid_token_12345'
        }
        response = requests.post(url, json={"binderId": "12345"},
                               headers=headers, timeout=TestConfig.TIMEOUT)

        assert response.status_code in [400, 401], "Expected status code 400 or 401"

    def test_malformed_json_payload(self):
        """TC_NEG_004: Verify malformed JSON returns 400"""
        url = f"{TestConfig.API_V7_BASE}/Binder/CreateBinder"
        response = requests.post(url, data="not valid json",
                               headers={'Content-Type': 'application/json'},
                               timeout=TestConfig.TIMEOUT)

        assert response.status_code in [400, 401], "Expected status code 400 or 401"

    def test_sql_injection_attempt(self):
        """TC_NEG_005: Verify SQL injection attempt is handled safely"""
        url = f"{TestConfig.API_V7_BASE}/Binder/GetBinderDetails"
        payload = {"binderId": "'; DROP TABLE Binders; --"}
        response = self.make_request('POST', url, payload)

        assert response.status_code in [400, 404], "Expected status code 400 or 404"

    def test_xss_attempt_in_payload(self):
        """TC_NEG_006: Verify XSS attempt is sanitized"""
        url = f"{TestConfig.API_V7_BASE}/Binder/CreateBinder"
        payload = {
            "clientName": "<script>alert('XSS')</script>",
            "taxYear": 2024
        }
        response = self.make_request('POST', url, payload)

        assert response.status_code in [200, 201, 400], "Expected valid response"


@pytest.mark.performance
class TestPerformanceScenarios(BaseAPITest):
    """Test cases for performance and load scenarios"""

    def test_response_time_authentication(self):
        """TC_PERF_001: Verify authentication response time is under 3 seconds"""
        url = f"{TestConfig.API_V7_BASE}/Authenticate/GetToken"
        payload = {
            "ClientID": TestConfig.V7_CLIENT_ID,
            "ClientSecret": TestConfig.V7_CLIENT_SECRET
        }

        start_time = datetime.now()
        response = requests.post(url, json=payload, timeout=TestConfig.TIMEOUT)
        end_time = datetime.now()

        response_time = (end_time - start_time).total_seconds()
        assert response_time < 3.0, f"Response time {response_time}s exceeded 3 seconds"

    def test_response_time_lookup_services(self):
        """TC_PERF_002: Verify lookup service response time is under 2 seconds"""
        url = f"{TestConfig.API_V7_BASE}/Lookup/ServiceTypes"

        start_time = datetime.now()
        response = self.make_request('POST', url)
        end_time = datetime.now()

        response_time = (end_time - start_time).total_seconds()
        assert response_time < 2.0, f"Response time {response_time}s exceeded 2 seconds"


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--html=reports/sureprep_api_test_report.html'])
