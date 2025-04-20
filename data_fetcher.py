import os
import json
import requests
from dotenv import load_dotenv

# === Load API key from keys.env ===
load_dotenv("keys.env")
alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")

def fetch_and_save_financials(symbol: str, api_key=alpha_vantage_key, output_folder="data"):
    """
    Fetches financial statements and metadata for a given ticker using Alpha Vantage API
    and saves them into a single JSON file.

    Parameters:
    - symbol: Ticker symbol (e.g., 'GOOGL')
    - api_key: Your Alpha Vantage API key (defaults to env)
    - output_folder: Directory where the JSON file will be saved
    """
    os.makedirs(output_folder, exist_ok=True)

    urls = {
        "balance_sheet": f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={api_key}",
        "income_statement": f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}",
        "cash_flow": f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={api_key}",
        "overview": f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}",
        "quote": f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    }

    financial_data = {}

    for data_type, url in urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "Information" in data or "Note" in data:
                print(f"⚠️ API limit reached or data unavailable for {symbol} - {data_type}")
                financial_data[data_type] = {"error": data.get("Information", data.get("Note", "Unknown error"))}
            else:
                financial_data[data_type] = data
        else:
            print(f"Failed to fetch {data_type} for {symbol}")
            financial_data[data_type] = {"error": "Failed to fetch"}

    output_file = os.path.join(output_folder, f"{symbol.upper()}_financials.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(financial_data, f, indent=4)

    print(f"✅ Financials saved to {output_file}")
    return output_file
