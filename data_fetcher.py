import os
import json
import requests

# Configuration
api_key = ""
symbol = "GOOGL"  # You can replace this with any ticker or input() for user entry

# Folder to store financial data
output_folder = "Financial Position"
os.makedirs(output_folder, exist_ok=True)

# URLs for different statements & metadata
urls = {
    "balance_sheet": f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={api_key}",
    "income_statement": f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}",
    "cash_flow": f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={api_key}",
    "overview": f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}",
    "quote": f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
}

# Data container to hold all data
financial_data = {}

# Fetch and store each dataset
for data_type, url in urls.items():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "Information" in data or "Note" in data:
            print(f"Warning: API Limit or Data not available for {symbol} - {data_type}")
            financial_data[data_type] = {"error": data.get("Information", data.get("Note", "Unknown error"))}
        else:
            financial_data[data_type] = data
    else:
        print(f"Failed to fetch {data_type} for {symbol}")
        financial_data[data_type] = {"error": "Failed to fetch"}

# Output file path
output_file_path = os.path.join(output_folder, f"{symbol}_financials.json")

# Save all financials to one JSON file
with open(output_file_path, "w", encoding="utf-8") as f:
    json.dump(financial_data, f, indent=4)

print(f"✅ Full financial profile for {symbol} saved to: {output_file_path}")
