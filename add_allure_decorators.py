#!/usr/bin/env python3
"""
Script to add Allure decorators to all test methods in test_TY2025_swagger_apis.py
"""

import re
import os


def extract_test_info(method_name, docstring):
    """Extract test case info from method name and docstring"""
    # Extract TC number from docstring
    tc_match = re.search(r'TC_(\d+):', docstring) if docstring else None
    tc_number = tc_match.group(1) if tc_match else "000"

    # Extract endpoint from docstring
    endpoint_match = re.search(r'Test \w+ (.+)', docstring) if docstring else None
    endpoint = endpoint_match.group(1) if endpoint_match else method_name

    # Determine story/category based on method name
    if 'authenticate' in method_name:
        story = "Authentication"
        severity = "CRITICAL"
    elif 'binderinfo' in method_name or 'binder' in method_name:
        story = "Binder Operations"
        severity = "CRITICAL"
    elif 'billing' in method_name:
        story = "Billing"
        severity = "NORMAL"
    elif 'document' in method_name:
        story = "Document Management"
        severity = "NORMAL"
    elif 'taxcaddy' in method_name:
        story = "TaxCaddy API"
        severity = "NORMAL"
    elif 'drl' in method_name:
        story = "DRL Operations"
        severity = "NORMAL"
    elif 'utintegration' in method_name:
        story = "UT Integration"
        severity = "NORMAL"
    else:
        story = "API Operations"
        severity = "NORMAL"

    # Extract HTTP method from docstring
    method_match = re.search(r'Test (post|get|put|delete|patch)', docstring, re.IGNORECASE) if docstring else None
    http_method = method_match.group(1).upper() if method_match else "POST"

    return {
        'tc_number': tc_number,
        'endpoint': endpoint,
        'story': story,
        'severity': severity,
        'http_method': http_method
    }


def add_allure_decorators_to_file(file_path):
    """Add Allure decorators to all test methods"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match test method definitions with docstrings
    pattern = r'(\n    def (test_\w+)\(self\):)\n(        """(.+?)"""\n)'

    def replace_func(match):
        full_match = match.group(0)
        method_def = match.group(1)
        method_name = match.group(2)
        docstring_part = match.group(3)
        docstring_content = match.group(4)

        # Skip if already has Allure decorators
        if '@allure.' in content[max(0, match.start() - 500):match.start()]:
            return full_match

        # Extract test info
        info = extract_test_info(method_name, docstring_content)

        # Build decorators
        decorators = f"""
    @allure.story("{info['story']}")
    @allure.title("TC_{info['tc_number']}: {info['http_method']} {info['endpoint']}")
    @allure.severity(allure.severity_level.{info['severity']})"""

        # Return with decorators
        return f"{decorators}{method_def}\n{docstring_part}"

    # Apply replacements
    new_content = re.sub(pattern, replace_func, content)

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    # Count decorators added
    original_count = content.count('@allure.')
    new_count = new_content.count('@allure.')
    added_count = new_count - original_count

    return added_count


if __name__ == "__main__":
    test_file = os.path.join(os.path.dirname(__file__), 'tests', 'test_TY2025_swagger_apis.py')

    print(f"Adding Allure decorators to: {test_file}")
    count = add_allure_decorators_to_file(test_file)
    print(f"[OK] Added Allure decorators to {count // 3} test methods")
    print("[OK] All test methods now have Allure reporting!")
