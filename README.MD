
# Valuation and Financial Modeling Dashboard

This repository contains a web-based financial modeling dashboard built with Streamlit, offering integrated Discounted Cash Flow (DCF) and Comparable Company Analysis (CCA) capabilities. The tool enables users to fetch, visualize, and analyze financial data for U.S. public companies. It also allows for the automation of Excel-based valuation models using real-time market and fundamental data retrieved via external APIs.

## Overview
![Demo](exampleUI.gif)


The application streamlines the valuation process by combining:

- Financial data fetching from Alpha Vantage and Financial Modeling Prep (FMP)
- Competitor peer identification via OpenAI GPT
- Interactive stock visualization using Altair
- Financial statement parsing and export to a macro-enabled Excel model
- Support for custom JSON uploads and dynamic metric generation

This project is ideal for financial analysts, students, and valuation professionals seeking an automated, data-driven workflow for public company valuations.

## Key Features

### 1. Streamlit Web Interface
- Intuitive dashboard with a left sidebar for fetching or uploading financial data
- Dynamic input fields for company tickers and JSON file uploads

### 2. Financial Data Retrieval
- Uses the Alpha Vantage API to gather:
  - Balance Sheet
  - Income Statement
  - Cash Flow Statement
  - Company Overview
  - Real-Time Quote
- Uses FMP for peer company financials

### 3. Comparable Company Analysis (CCA)
- Identifies similar companies using OpenAI's GPT models
- Fetches key financial metrics for each peer
- Displays peer overview, sector, and financial KPIs such as:
  - Market Capitalization
  - Enterprise Value
  - Revenue, EBITDA, EBIT, and Net Income

### 4. Discounted Cash Flow (DCF) Model Integration
- Extracts revenue, cost of goods sold (COGS), operating expenses (OPEX), D&A, CAPEX, and working capital from JSON
- Calculates the corporate tax rate from financials
- Writes peer company data and calculated metrics into a pre-formatted Excel model

### 5. Interactive Stock Charts
- Generates OHLC (Open, High, Low, Close) charts for the last 5 years using Yahoo Finance
- Users can toggle between different financial metrics in the visualization

### 6. Excel Automation (via xlwings)
- Populates two separate worksheets for DCF and CCA
- Automatically fills Excel formulas, valuation assumptions, and peer comparison tables
- Supports updating valuation.xlsm with new tickers and financials

## Folder Structure

```
.
├── dashboard.py                          # Main Streamlit application
├── data_fetcher.py                       # Alpha Vantage financial fetcher
├── comparable_company_analysis.py        # Peer analysis and OpenAI integration
├── stock_chart.py                        # OHLC chart data from yfinance
├── dcfExcel.py                           # DCF Excel automation
├── cca_excel.py                          # CCA Excel automation
├── style.css                             # Custom styling for Streamlit
├── data/                                 # Contains JSON files for charts and financials
│   ├── {TICKER}_financials.json
│   ├── {TICKER}_chart.json
│   └── {TICKER}_comparable_analysis.json
├── models/
│   └── valuation.xlsm                    # Macro-enabled Excel file used for modeling
```

## Getting Started

### Prerequisites

Install the necessary packages:

```bash
pip install streamlit pandas altair requests yfinance xlwings openai
```

Ensure Excel is installed on your machine to use the xlwings functionality. Enable macros in `valuation.xlsm` to support dynamic updates.

## Running the Application

To launch the dashboard locally:

```bash
streamlit run dashboard.py
```

The app will open in your default browser. From there, you can enter a ticker or upload a JSON file to begin the analysis.

## API Configuration

To use the financial and AI capabilities, API keys are required:

- Alpha Vantage API Key: Used for primary financial statement retrieval
- Financial Modeling Prep API Key: Used for peer company financials
- OpenAI API Key: Used to identify comparable companies

These keys can be stored in environment variables or hardcoded (not recommended for production). Make sure to remain within each API provider’s usage limits.

## Supported Workflows

### A. Fetch Financials via Ticker
1. Enter a U.S. ticker symbol (e.g., `GOOGL`)
2. Application fetches financials from Alpha Vantage and peer data from FMP
3. OHLC chart and company snapshot displayed
4. Peer companies fetched via OpenAI and displayed
5. CCA and DCF models auto-populated in Excel

### B. Upload Custom Financials
1. Upload a custom JSON file containing required keys:
   - `balance_sheet`, `income_statement`, `cash_flow`, `overview`, `quote`
2. Enter the ticker symbol
3. Data is processed and stored under the `data/` directory
4. Proceed with visualization and modeling as above

## Output

The application generates the following:

- `data/{TICKER}_financials.json`: Core financial statements
- `data/{TICKER}_chart.json`: OHLC chart data
- `data/{TICKER}_comparable_analysis.json`: Peer metrics and overview
- `models/valuation.xlsm`: Excel file updated with company and peer data

## Limitations

- API rate limits can throttle data fetches. Implement retry logic or caching for frequent use.
- Excel macros must be enabled manually; automation is limited to locally installed Excel environments.
- Peer selection relies on OpenAI's model and may vary based on API responses.

## License

This project is provided for educational and analytical purposes. Redistribution or commercial use should be authorized explicitly. No warranty is provided for data accuracy or valuation results.
