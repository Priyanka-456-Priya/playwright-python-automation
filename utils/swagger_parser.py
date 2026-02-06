"""
Swagger/OpenAPI Parser Utility
Parses Swagger/OpenAPI specifications to extract endpoints, methods, and error codes
"""

import json
import requests
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin
import logging


class SwaggerParser:
    """Parse and extract information from Swagger/OpenAPI specifications"""

    def __init__(self, swagger_url: str, logger: Optional[logging.Logger] = None):
        """
        Initialize SwaggerParser

        Args:
            swagger_url: URL to the Swagger JSON specification
            logger: Optional logger instance
        """
        self.swagger_url = swagger_url
        self.logger = logger or logging.getLogger(__name__)
        self.spec = None
        self.base_url = None

    def fetch_swagger_spec(self) -> Dict[str, Any]:
        """
        Fetch Swagger specification from URL

        Returns:
            Dictionary containing the Swagger specification
        """
        try:
            self.logger.info(f"Fetching Swagger spec from: {self.swagger_url}")
            response = requests.get(self.swagger_url, timeout=30)
            response.raise_for_status()
            self.spec = response.json()

            # Extract base URL
            if 'servers' in self.spec:
                # OpenAPI 3.0
                self.base_url = self.spec['servers'][0]['url']
            elif 'host' in self.spec:
                # Swagger 2.0
                scheme = self.spec.get('schemes', ['https'])[0]
                host = self.spec['host']
                base_path = self.spec.get('basePath', '')
                self.base_url = f"{scheme}://{host}{base_path}"

            self.logger.info(f"Successfully fetched Swagger spec. Base URL: {self.base_url}")
            return self.spec

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch Swagger spec: {e}")
            raise

    def get_all_endpoints(self) -> List[Dict[str, Any]]:
        """
        Extract all API endpoints from the Swagger spec

        Returns:
            List of endpoint dictionaries with path, method, and details
        """
        if not self.spec:
            self.fetch_swagger_spec()

        endpoints = []
        paths = self.spec.get('paths', {})

        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.upper() in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']:
                    endpoint = {
                        'path': path,
                        'method': method.upper(),
                        'operation_id': operation.get('operationId', ''),
                        'summary': operation.get('summary', ''),
                        'description': operation.get('description', ''),
                        'tags': operation.get('tags', []),
                        'parameters': operation.get('parameters', []),
                        'responses': operation.get('responses', {}),
                        'security': operation.get('security', []),
                        'full_url': urljoin(self.base_url, path) if self.base_url else path
                    }
                    endpoints.append(endpoint)

        self.logger.info(f"Extracted {len(endpoints)} endpoints from Swagger spec")
        return endpoints

    def get_error_codes_for_endpoint(self, endpoint: Dict[str, Any]) -> List[int]:
        """
        Extract error status codes defined for a specific endpoint

        Args:
            endpoint: Endpoint dictionary from get_all_endpoints()

        Returns:
            List of HTTP error status codes
        """
        error_codes = []
        responses = endpoint.get('responses', {})

        for status_code in responses.keys():
            try:
                code = int(status_code)
                if 400 <= code < 600:
                    error_codes.append(code)
            except ValueError:
                # Handle 'default' or other non-numeric response codes
                continue

        return sorted(error_codes)

    def get_all_documented_error_codes(self) -> Dict[int, List[Dict[str, Any]]]:
        """
        Get all documented error codes across all endpoints

        Returns:
            Dictionary mapping error codes to list of endpoints that document them
        """
        error_code_map = {}
        endpoints = self.get_all_endpoints()

        for endpoint in endpoints:
            error_codes = self.get_error_codes_for_endpoint(endpoint)
            for code in error_codes:
                if code not in error_code_map:
                    error_code_map[code] = []
                error_code_map[code].append({
                    'path': endpoint['path'],
                    'method': endpoint['method'],
                    'operation_id': endpoint['operation_id']
                })

        self.logger.info(f"Found {len(error_code_map)} unique error codes in Swagger spec")
        return error_code_map

    def get_request_schema(self, endpoint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Extract request body schema for an endpoint

        Args:
            endpoint: Endpoint dictionary from get_all_endpoints()

        Returns:
            Request schema dictionary or None
        """
        # OpenAPI 3.0
        if 'requestBody' in endpoint:
            content = endpoint['requestBody'].get('content', {})
            if 'application/json' in content:
                return content['application/json'].get('schema')

        # Swagger 2.0
        for param in endpoint.get('parameters', []):
            if param.get('in') == 'body':
                return param.get('schema')

        return None

    def get_required_parameters(self, endpoint: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get required parameters for an endpoint

        Args:
            endpoint: Endpoint dictionary from get_all_endpoints()

        Returns:
            List of required parameter dictionaries
        """
        required_params = []

        for param in endpoint.get('parameters', []):
            if param.get('required', False):
                required_params.append({
                    'name': param.get('name'),
                    'in': param.get('in'),
                    'type': param.get('type'),
                    'schema': param.get('schema')
                })

        return required_params

    def generate_test_matrix(self) -> List[Dict[str, Any]]:
        """
        Generate a test matrix for error code validation

        Returns:
            List of test cases with endpoint and error code combinations
        """
        test_matrix = []
        endpoints = self.get_all_endpoints()

        for endpoint in endpoints:
            error_codes = self.get_error_codes_for_endpoint(endpoint)
            required_params = self.get_required_parameters(endpoint)

            test_case = {
                'endpoint': endpoint['path'],
                'method': endpoint['method'],
                'operation_id': endpoint['operation_id'],
                'full_url': endpoint['full_url'],
                'documented_error_codes': error_codes,
                'required_parameters': required_params,
                'request_schema': self.get_request_schema(endpoint)
            }
            test_matrix.append(test_case)

        return test_matrix

    def save_endpoints_to_file(self, filename: str = "extracted_endpoints.json"):
        """
        Save extracted endpoints to a JSON file

        Args:
            filename: Output filename
        """
        endpoints = self.get_all_endpoints()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(endpoints, f, indent=2, ensure_ascii=False)
        self.logger.info(f"Saved {len(endpoints)} endpoints to {filename}")


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)

    swagger_url = "https://api.sureprep.com/swagger/v1/swagger.json"
    parser = SwaggerParser(swagger_url)

    # Fetch and parse
    parser.fetch_swagger_spec()

    # Get all endpoints
    endpoints = parser.get_all_endpoints()
    print(f"\nFound {len(endpoints)} endpoints")

    # Get error codes
    error_codes = parser.get_all_documented_error_codes()
    print(f"\nDocumented error codes: {list(error_codes.keys())}")

    # Generate test matrix
    test_matrix = parser.generate_test_matrix()
    print(f"\nGenerated {len(test_matrix)} test cases")
