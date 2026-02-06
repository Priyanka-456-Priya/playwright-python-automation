"""
Bulk Update Script for Test Methods
Updates all 113 test methods systematically
"""

import re

def main():
    test_file = r"tests\test_auto_generated_swagger_apis.py"

    print("Reading test file...")
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Step 1: Add endpoint variable after each url definition
    print("Step 1: Adding endpoint variables...")

    # Pattern: url = f"{TestConfig.BASE_URL}/some/path"
    # We want to add: endpoint = "/some/path" right after
    def add_endpoint_var(match):
        url_line = match.group(0)
        full_url = match.group(1)
        endpoint_path = match.group(2)

        # Check if endpoint already exists in the next few characters
        # by looking at what comes after this match in the full content

        endpoint_var = f'\n        endpoint = "{endpoint_path}"'

        return url_line + endpoint_var

    # This pattern captures the URL line
    pattern1 = r'(url = f"\{TestConfig\.BASE_URL\}([^"]+)")'

    # Find all matches and their positions
    matches = list(re.finditer(pattern1, content))
    print(f"Found {len(matches)} URL definitions")

    # Process in reverse to maintain positions
    for match in reversed(matches):
        start, end = match.span()
        endpoint_path = match.group(2)

        # Check if endpoint variable already exists nearby
        check_region = content[end:end+100]
        if f'endpoint = "{endpoint_path}"' in check_region:
            continue  # Already has endpoint

        # Insert endpoint variable
        insertion = f'\n        endpoint = "{endpoint_path}"'
        content = content[:end] + insertion + content[end:]

    print("Step 1 complete!")

    # Step 2: Add display_test_result() call after each make_request block
    print("\nStep 2: Adding display_test_result() calls...")

    # Pattern to find make_request blocks and add display call after
    # We need to find: response = self.make_request(...) including multi-line

    pattern2 = r'(response = self\.make_request\(\s*\n(?:.*?\n)*?\s*\))'

    matches = list(re.finditer(pattern2, content, re.MULTILINE))
    print(f"Found {len(matches)} make_request calls")

    # Process in reverse
    for match in reversed(matches):
        start, end = match.span()
        request_block = match.group(0)

        # Check if display_test_result already exists nearby
        check_region = content[end:end+200]
        if 'display_test_result' in check_region:
            continue  # Already has display call

        # Determine method type from the request block
        method = 'POST'
        if "'GET'" in request_block or '"GET"' in request_block:
            method = 'GET'

        # Add display call
        insertion = f'\n\n        # Display test result\n        self.display_test_result(endpoint, \'{method}\', response, payload)'
        content = content[:end] + insertion + content[end:]

    print("Step 2 complete!")

    # Step 3: Remove old print statements
    print("\nStep 3: Removing old print statements...")

    # Remove these specific patterns
    content = re.sub(r'\s+print\(f["\']API:.*?\n', '\n', content)
    content = re.sub(r'\s+print\(f["\']Status:.*?\n', '\n', content)
    content = re.sub(r'\s+print\(f["\']Response keys:.*?\n', '\n', content)

    print("Step 3 complete!")

    # Write back
    print("\nWriting updated file...")
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(content)

    # Count changes
    changes = len(content) - len(original_content)
    print(f"\n{'='*70}")
    print("✓ Update Complete!")
    print(f"{'='*70}")
    print(f"File size changed by: {changes:+d} characters")
    print(f"Test methods processed: ~113")
    print("\nNext steps:")
    print("1. Review the changes in your IDE")
    print("2. Run a sample test:")
    print("   pytest tests/test_auto_generated_swagger_apis.py::TestSwaggerAPIs::test_v7_authenticate_gettoken_2 -v -s")
    print("3. Run all tests:")
    print("   pytest tests/test_auto_generated_swagger_apis.py -v -s")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
