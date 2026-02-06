"""
API Client Utility
Handles HTTP requests for API testing with authentication, retries, and error handling
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, Any, Optional, Union
import logging
import time
from datetime import datetime


class APIClient:
    """Robust API client for testing with retry logic and authentication"""

    def __init__(
        self,
        base_url: str,
        auth_type: str = "none",
        auth_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key_header: Optional[str] = None,
        api_key_value: Optional[str] = None,
        timeout: int = 30,
        retry_count: int = 3,
        verify_ssl: bool = True,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize API Client

        Args:
            base_url: Base URL for the API
            auth_type: Authentication type (bearer, basic, api_key, none)
            auth_token: Bearer token for authentication
            username: Username for basic auth
            password: Password for basic auth
            api_key_header: Header name for API key auth
            api_key_value: API key value
            timeout: Request timeout in seconds
            retry_count: Number of retries for failed requests
            verify_ssl: Whether to verify SSL certificates
            logger: Optional logger instance
        """
        self.base_url = base_url.rstrip('/')
        self.auth_type = auth_type
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.logger = logger or logging.getLogger(__name__)

        # Setup session with retry strategy
        self.session = self._create_session(retry_count)

        # Setup authentication
        self._setup_authentication(
            auth_token, username, password, api_key_header, api_key_value
        )

    def _create_session(self, retry_count: int) -> requests.Session:
        """
        Create requests session with retry strategy

        Args:
            retry_count: Number of retries

        Returns:
            Configured requests session
        """
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=retry_count,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "PATCH", "DELETE"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _setup_authentication(
        self,
        auth_token: Optional[str],
        username: Optional[str],
        password: Optional[str],
        api_key_header: Optional[str],
        api_key_value: Optional[str]
    ):
        """Setup authentication headers based on auth type"""
        if self.auth_type == "bearer" and auth_token:
            self.session.headers.update({
                "Authorization": f"Bearer {auth_token}"
            })
        elif self.auth_type == "basic" and username and password:
            from requests.auth import HTTPBasicAuth
            self.session.auth = HTTPBasicAuth(username, password)
        elif self.auth_type == "api_key" and api_key_header and api_key_value:
            self.session.headers.update({
                api_key_header: api_key_value
            })

        # Common headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expect_error: bool = False,
        **kwargs
    ) -> requests.Response:
        """
        Make HTTP request

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data
            json: JSON request body
            headers: Additional headers
            expect_error: Whether we expect an error response
            **kwargs: Additional arguments for requests

        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}" if not endpoint.startswith('http') else endpoint

        # Merge headers
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)

        # Log request
        self.logger.info(f"Making {method} request to: {url}")
        if params:
            self.logger.debug(f"Query params: {params}")
        if json:
            self.logger.debug(f"JSON payload: {json}")

        start_time = time.time()

        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                params=params,
                data=data,
                json=json,
                headers=request_headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
                **kwargs
            )

            elapsed_time = time.time() - start_time

            # Log response
            self.logger.info(
                f"Response: {response.status_code} | Time: {elapsed_time:.2f}s"
            )

            if not expect_error and response.status_code >= 400:
                self.logger.warning(
                    f"Unexpected error response: {response.status_code} - {response.text[:200]}"
                )

            return response

        except requests.exceptions.RequestException as e:
            elapsed_time = time.time() - start_time
            self.logger.error(
                f"Request failed after {elapsed_time:.2f}s: {str(e)}"
            )
            raise

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Make GET request"""
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """Make POST request"""
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """Make PUT request"""
        return self.request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        """Make PATCH request"""
        return self.request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make DELETE request"""
        return self.request("DELETE", endpoint, **kwargs)

    def validate_error_code(
        self,
        method: str,
        endpoint: str,
        expected_status_code: int,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Validate that an endpoint returns a specific error code

        Args:
            method: HTTP method
            endpoint: API endpoint
            expected_status_code: Expected HTTP status code
            **kwargs: Additional request arguments

        Returns:
            Validation result dictionary
        """
        result = {
            "endpoint": endpoint,
            "method": method,
            "expected_status_code": expected_status_code,
            "actual_status_code": None,
            "passed": False,
            "response_time": None,
            "error_message": None,
            "response_body": None,
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            response = self.request(
                method=method,
                endpoint=endpoint,
                expect_error=True,
                **kwargs
            )

            result["actual_status_code"] = response.status_code
            result["response_time"] = response.elapsed.total_seconds()

            try:
                result["response_body"] = response.json()
            except:
                result["response_body"] = response.text[:500]

            # Check if status code matches
            if response.status_code == expected_status_code:
                result["passed"] = True
                self.logger.info(
                    f"✓ Validation passed: {method} {endpoint} returned {expected_status_code}"
                )
            else:
                result["error_message"] = (
                    f"Expected {expected_status_code}, got {response.status_code}"
                )
                self.logger.warning(
                    f"✗ Validation failed: {method} {endpoint} - {result['error_message']}"
                )

        except Exception as e:
            result["error_message"] = str(e)
            self.logger.error(f"Error during validation: {str(e)}")

        return result

    def close(self):
        """Close the session"""
        self.session.close()


class ErrorCodeTester:
    """Helper class for testing specific error code scenarios"""

    def __init__(self, api_client: APIClient):
        """
        Initialize ErrorCodeTester

        Args:
            api_client: APIClient instance
        """
        self.client = api_client

    def test_400_bad_request(self, endpoint: str, method: str = "POST") -> Dict[str, Any]:
        """Test 400 Bad Request by sending invalid data"""
        scenarios = [
            {"name": "malformed_json", "data": "{invalid_json}"},
            {"name": "missing_required_field", "json": {}},
            {"name": "invalid_data_type", "json": {"id": "not_a_number"}},
        ]

        results = []
        for scenario in scenarios:
            result = self.client.validate_error_code(
                method=method,
                endpoint=endpoint,
                expected_status_code=400,
                **{k: v for k, v in scenario.items() if k != "name"}
            )
            result["scenario"] = scenario["name"]
            results.append(result)

        return results

    def test_401_unauthorized(self, endpoint: str, method: str = "GET") -> Dict[str, Any]:
        """Test 401 Unauthorized by removing authentication"""
        # Temporarily remove auth headers
        original_headers = self.client.session.headers.copy()
        self.client.session.headers.pop("Authorization", None)

        result = self.client.validate_error_code(
            method=method,
            endpoint=endpoint,
            expected_status_code=401
        )

        # Restore headers
        self.client.session.headers.update(original_headers)

        return result

    def test_404_not_found(self, base_endpoint: str, method: str = "GET") -> Dict[str, Any]:
        """Test 404 Not Found with non-existent resource"""
        endpoint = f"{base_endpoint}/99999999"

        return self.client.validate_error_code(
            method=method,
            endpoint=endpoint,
            expected_status_code=404
        )

    def test_405_method_not_allowed(self, endpoint: str, wrong_method: str = "DELETE") -> Dict[str, Any]:
        """Test 405 Method Not Allowed with wrong HTTP method"""
        return self.client.validate_error_code(
            method=wrong_method,
            endpoint=endpoint,
            expected_status_code=405
        )


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    client = APIClient(
        base_url="https://api.sureprep.com",
        auth_type="none"
    )

    # Test a simple GET request
    try:
        response = client.get("/api/health")
        print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
