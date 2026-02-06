"""
Automatic Test Update Script
This script updates all test methods to use the new display_test_result() method
"""

import re

def update_all_test_methods():
    test_file_path = r"tests\test_auto_generated_swagger_apis.py"

    with open(test_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match test methods and extract necessary info
    # This pattern finds: method definition, url, payload, and response sections

    def process_test_method(match):
        full_method = match.group(0)

        # Skip if already updated (contains display_test_result)
        if 'display_test_result' in full_method:
            return full_method

        # Extract endpoint from URL line
        url_pattern = r'url = f"\{TestConfig\.BASE_URL\}(.*?)"'
        url_match = re.search(url_pattern, full_method)
        if not url_match:
            return full_method

        endpoint = url_match.group(1)

        # Find where to insert the display_test_result call
        # Insert after the response = self.make_request(...) block
        response_pattern = r'(response = self\.make_request\([^)]+?\n\s+\))\n'
        response_match = re.search(response_pattern, full_method, re.DOTALL)

        if not response_match:
            return full_method

        # Determine the method (GET or POST)
        method = 'POST'  # Default
        if "'GET'" in full_method or '"GET"' in full_method:
            method = 'GET'

        # Build the new content
        insertion_point = response_match.end()

        # Get indentation
        indent = '        '

        # Create the endpoint variable and display call
        endpoint_var = f'{indent}endpoint = "{endpoint}"\n'
        display_call = f'{indent}self.display_test_result(endpoint, \'{method}\', response, payload)\n'

        # Insert endpoint variable after url definition
        url_end = url_match.end()
        new_method = full_method[:url_end] + '\n' + endpoint_var + full_method[url_end:]

        # Now find the response block again in the modified content
        response_match = re.search(response_pattern, new_method, re.DOTALL)
        if response_match:
            insertion_point = response_match.end()
            new_method = new_method[:insertion_point] + '\n' + display_call + new_method[insertion_point:]

        # Remove old print statements
        new_method = re.sub(r'\s+print\(f["\']API:.*?\n', '', new_method)
        new_method = re.sub(r'\s+print\(f["\']Status:.*?\n', '', new_method)
        new_method = re.sub(r'\s+print\(f["\']Response keys:.*?\n', '', new_method)

        return new_method

    # Match all test methods (from def test_ to the next def or end of class)
    pattern = r'(    def test_\w+\(self\):.*?)(?=    def test_|class |$)'
    updated_content = re.sub(pattern, process_test_method, content, flags=re.DOTALL)

    # Write back
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("✓ All test methods have been updated!")
    print("✓ Added endpoint variable to each test")
    print("✓ Added display_test_result() call after each request")
    print("✓ Removed old print statements")
    print("\nPlease review the changes and run tests to verify.")

if __name__ == "__main__":
    update_all_test_methods()
