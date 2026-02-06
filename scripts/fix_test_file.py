"""
Fix syntax errors in generated test file (leading zeros in numbers)
"""
import re

def fix_leading_zeros(file_path):
    """Fix leading zeros in integer literals"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix patterns like "01" to "1" but preserve "0" and actual strings
    # This regex looks for numbers with leading zeros in dictionary values
    pattern = r':\s*0+(\d+)([,\s\}\]])'
    replacement = r': \1\2'

    fixed_content = re.sub(pattern, replacement, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f"Fixed leading zeros in {file_path}")

if __name__ == "__main__":
    file_path = r"c:\Users\6124481\VS_CODE Projects\API_Error_Codes_Validation\tests\test_auto_generated_swagger_apis.py"
    fix_leading_zeros(file_path)
