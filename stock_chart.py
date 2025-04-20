import yfinance as yf
import pandas as pd
import json
import os
import sys

def fetch_ohlc_to_json(ticker):
    df = yf.download(ticker, period="5y", interval="1d", auto_adjust=False)

    # Reset index and flatten columns
    df.reset_index(inplace=True)

    # Rename columns to remove multi-index
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    # Format date
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime('%Y-%m-%d')

    # Select only necessary columns
    ohlc_df = df[["Date", "Open", "High", "Low", "Close"]].dropna()

    # Ensure the data folder exists
    os.makedirs("data", exist_ok=True)

    # Save to JSON
    file_path = f"data/{ticker}_chart.json"
    with open(file_path, "w") as f:
        json.dump(ohlc_df.to_dict(orient="records"), f, indent=4)

    print(f"Saved OHLC data for {ticker} to {file_path}")

# === Entry point when script is called directly ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Ticker symbol not provided.")
        sys.exit(1)

    ticker = sys.argv[1].upper()
    fetch_ohlc_to_json(ticker)
