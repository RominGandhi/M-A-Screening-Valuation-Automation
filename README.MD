
# Valuation & Financial Modeling Platform (with DCF + CCA Automation)

This repository contains a web-based financial modeling dashboard built with Streamlit, offering integrated Discounted Cash Flow (DCF) and Comparable Company Analysis (CCA) capabilities. The tool enables users to fetch, visualize, and analyze financial data for U.S. public companies. It also allows for the automation of Excel-based valuation models using real-time market and fundamental data retrieved via external APIs.

## User Interface (UI)
![Demo](exampleUI.gif)


The application streamlines the valuation process by combining:

- Financial data fetching from Alpha Vantage, Financial Modeling Prep (FMP) and Yahoo Finance
- Competitor peer identification via OpenAI GPT 
- Interactive stock visualization using Altair
- Financial statement parsing and export to a macro-enabled Excel model
- Support for custom JSON uploads and dynamic metric generation


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
- Uses Yahoo Finance for generating stock charts

### 3. Comparable Company Analysis (CCA)
- Identifies similar companies using OpenAI's GPT models
- Calculates key financial metrics for each peer
- Displays peer overview, sector, and financial KPIs such as:
  - Market Capitalization
  - Enterprise Value
  - Revenue, EBITDA, EBIT, and Net Income

### 4. Discounted Cash Flow (DCF) Model Integration
- Extracts revenue, cost of goods sold (COGS), operating expenses (OPEX), D&A, CAPEX, and working capital from JSON
- Calculates other metrics from financials json
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
├── app.py                                # Main Streamlit application
├── data_fetcher.py                       # Alpha Vantage financial fetcher
├── comparable_company_analysis.py        # Peer analysis and OpenAI integration
├── stock_chart.py                        # OHLC chart data from yfinance
├── dcfExcel.py                           # DCF Excel automation
├── dcfModel.py                           # DCF calulations
├── style.css                             # Custom styling for Streamlit
├── ccaExcel.py                           # CCA Excel automation and calculation
├── data/                                 # Contains JSON files for charts and financials
│   ├── {TICKER}_financials.json
│   ├── {TICKER}_chart.json
│   └── {TICKER}_comparable_analysis.json
├── models/
│   └── valuation.xlsm                    # Macro-enabled Excel file used for modeling
├── log data/
│   └── {TICKER}_calculation_data.txt     # All raw calculations for DCF Model 
`
