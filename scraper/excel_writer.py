"""In this file the output of the scraped data will be properly navigated to the provided .xslx file with proper format"""
import pandas as pd
import json
from pathlib import Path
from openpyxl.workbook import Workbook

def json_to_excel(file_path_json: Path = "outputs/book_data.json", file_path_xlsx: Path = "outputs/book_data.xlsx", sheet_name: str = "Book Data") -> None:
    """This code snippet is a Python function that reads data from a JSON file, converts it into a
    pandas DataFrame, and then saves that DataFrame into an Excel file"""
    try:
        json_file = file_path_json
        with open(json_file, "r", encoding = "utf-8") as file:
            data = json.load(file)

        df1 = pd.DataFrame(data)
        df1.to_excel(file_path_xlsx, index = False, sheet_name = sheet_name)

    except Exception as e:
        print(f"Error parsing json data to excel: {e}")