import pandas as pd
import json
import os

def parse_swagger_excel(file_path):
    """Parse Swagger API specification from Excel file"""
    try:
        # Read all sheets from Excel file
        excel_file = pd.ExcelFile(file_path)

        print(f"Found sheets: {excel_file.sheet_names}")

        api_specs = {}

        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"\n{'='*60}")
            print(f"Sheet: {sheet_name}")
            print(f"{'='*60}")
            print(f"Columns: {df.columns.tolist()}")
            print(f"Rows: {len(df)}")
            print("\nFirst few rows:")
            print(df.head(10).to_string())

            api_specs[sheet_name] = df.to_dict('records')

        # Save parsed data to JSON for easier inspection
        output_file = 'parsed_swagger_spec.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(api_specs, f, indent=2, default=str)

        print(f"\n\nParsed data saved to: {output_file}")
        return api_specs

    except Exception as e:
        print(f"Error parsing Excel file: {str(e)}")
        return None

if __name__ == "__main__":
    file_path = r"c:\Users\6124481\Downloads\SureprepAPI_Swagger 1.xlsx"
    parse_swagger_excel(file_path)
