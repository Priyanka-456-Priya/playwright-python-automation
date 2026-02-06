"""
Parse Excel file containing Swagger API specifications to JSON
"""
import pandas as pd
import json
import sys

def parse_excel_to_json(excel_path, output_json_path):
    """Parse Excel file and convert to JSON format"""
    try:
        # Read Excel file
        df = pd.read_excel(excel_path)

        print(f"Excel file loaded successfully!")
        print(f"Columns: {list(df.columns)}")
        print(f"Total rows: {len(df)}")
        print(f"\nFirst few rows:")
        print(df.head())

        # Convert to JSON
        apis = []
        for index, row in df.iterrows():
            api_entry = {}
            for col in df.columns:
                # Convert to native Python types
                value = row[col]
                if pd.isna(value):
                    api_entry[col] = None
                elif isinstance(value, (pd.Timestamp, pd.DatetimeTZDtype)):
                    api_entry[col] = str(value)
                else:
                    api_entry[col] = value
            apis.append(api_entry)

        # Write to JSON file
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(apis, f, indent=2, ensure_ascii=False)

        print(f"\nSuccessfully converted to JSON: {output_json_path}")
        print(f"Total APIs extracted: {len(apis)}")

        return apis

    except Exception as e:
        print(f"Error parsing Excel file: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    excel_path = r"C:\Users\6124481\VS_CODE Projects\SureprepAPI_Swagger_2025.json"
    output_path = r"c:\Users\6124481\VS_CODE Projects\API_Error_Codes_Validation\testData\swagger_apis.json"

    parse_excel_to_json(excel_path, output_path)
