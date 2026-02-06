"""
Reliable Test Update Script
Processes the test file line by line to add display_test_result() calls
"""

import re

def update_test_file():
    test_file_path = r"tests\test_auto_generated_swagger_apis.py"

    with open(test_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    updates_count = 0

    while i < len(lines):
        line = lines[i]
        new_lines.append(line)

        # Check if this is a test method definition
        if line.strip().startswith('def test_') and '(self):' in line:
            # Look ahead for the url line and extract endpoint
            j = i + 1
            endpoint = None
            url_line_index = None

            while j < len(lines) and j < i + 20:  # Look within next 20 lines
                if 'url = f"{TestConfig.BASE_URL}' in lines[j]:
                    # Extract endpoint
                    match = re.search(r'url = f"\{TestConfig\.BASE_URL\}(.*?)"', lines[j])
                    if match:
                        endpoint = match.group(1)
                        url_line_index = j
                    break
                j += 1

            # If we found the URL, add endpoint variable after it
            if endpoint and url_line_index:
                # Check if endpoint variable already exists
                already_has_endpoint = False
                for k in range(url_line_index, min(url_line_index + 5, len(lines))):
                    if 'endpoint = ' in lines[k] and endpoint in lines[k]:
                        already_has_endpoint = True
                        break

                if not already_has_endpoint:
                    # Copy lines up to url_line
                    while i < url_line_index:
                        i += 1
                        new_lines.append(lines[i])

                    # Add endpoint variable after URL line
                    indent = '        '
                    endpoint_line = f'{indent}endpoint = "{endpoint}"\n'
                    new_lines.append(endpoint_line)

                    # Now look for the response = self.make_request block
                    j = i + 1
                    response_end_index = None

                    while j < len(lines) and j < i + 30:
                        if 'response = self.make_request(' in lines[j]:
                            # Find the closing parenthesis
                            k = j
                            paren_count = lines[j].count('(') - lines[j].count(')')
                            while paren_count > 0 and k < len(lines):
                                k += 1
                                paren_count += lines[k].count('(') - lines[k].count(')')
                            response_end_index = k
                            break
                        j += 1

                    if response_end_index:
                        # Copy lines up to and including response block
                        while i < response_end_index:
                            i += 1
                            new_lines.append(lines[i])

                        # Check if display_test_result already exists
                        already_has_display = False
                        for k in range(response_end_index, min(response_end_index + 5, len(lines))):
                            if 'display_test_result' in lines[k]:
                                already_has_display = True
                                break

                        if not already_has_display:
                            # Determine method type (GET or POST)
                            method = 'POST'
                            for k in range(max(0, response_end_index - 10), response_end_index + 1):
                                if "'GET'" in lines[k] or '"GET"' in lines[k]:
                                    method = 'GET'
                                    break

                            # Add blank line and display call
                            display_line = f'\n{indent}# Display test result\n{indent}self.display_test_result(endpoint, \'{method}\', response, payload)\n'
                            new_lines.append(display_line)
                            updates_count += 1

        i += 1

    # Remove old print statements
    final_lines = []
    skip_next = False
    for line in new_lines:
        if skip_next:
            skip_next = False
            continue
        # Remove specific old print statements
        if re.match(r'\s+print\(f["\']API:', line):
            continue
        elif re.match(r'\s+print\(f["\']Status:', line):
            continue
        elif re.match(r'\s+print\(f["\']Response keys:', line):
            continue
        else:
            final_lines.append(line)

    # Write the updated content
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)

    print(f"✓ Successfully updated {updates_count} test methods!")
    print("✓ Added endpoint variable to each test")
    print("✓ Added display_test_result() call after each request")
    print("✓ Removed old print statements")
    print("\nReview the changes and run a test to verify:")
    print("pytest tests/test_auto_generated_swagger_apis.py::TestSwaggerAPIs::test_v5_0_authenticate_gettoken_1 -v -s")

if __name__ == "__main__":
    update_test_file()
