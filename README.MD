
# 💼 Valuation & Financial Modeling Platform  

This repository hosts a powerful **web-based financial modeling dashboard** built with **Streamlit**, offering automated **Discounted Cash Flow (DCF)** and **Comparable Company Analysis (CCA)** workflows. Designed for finance professionals, analysts, and students, the tool streamlines company valuation using **real-time market data**, **machine learning models**, and **Excel automation**.

---

## 🎯 Overview

The platform integrates:

- 📈 **Real-time data retrieval** from Alpha Vantage, Financial Modeling Prep (FMP), and Yahoo Finance  
- 🤖 **Peer company identification** via OpenAI GPT  
- 📊 **Interactive visualizations** with Altair  
- 🧾 **Excel-based financial model automation** using xlwings  
- 📁 **Support for custom JSON uploads** with automatic parsing and metric generation  

---

## 🖥️ User Interface (UI)

A sleek, interactive dashboard allows users to easily toggle between data sources, upload custom files, and visualize key metrics.

![Demo](exampleUI.gif)

---

## 🚀 Key Features

### 1. 🔍 Streamlit-Powered Web Interface  
- Sidebar navigation for workflow selection  
- Dynamic inputs for ticker symbols and file uploads  
- Clean, responsive layout with real-time interactivity  

### 2. 📊 Financial Data Retrieval  
- **Alpha Vantage API**:  
  - Balance Sheet  
  - Income Statement  
  - Cash Flow Statement  
  - Company Overview  
  - Real-Time Quotes  
- **FMP API**: Peer company financials  
- **Yahoo Finance**: Historical stock chart data  

### 3. 🧠 Comparable Company Analysis (CCA)  
- Peer companies generated via **OpenAI GPT** based on sector and profile  
- Calculates and displays key metrics:  
  - Market Cap, Enterprise Value  
  - Revenue, EBITDA, EBIT, Net Income  
- Overview of sector, competitors, and relative financial health  

### 4. 📉 Discounted Cash Flow (DCF) Modeling  
- Parses uploaded or fetched financial data  
- Extracts:  
  - Revenue, COGS, OPEX, D&A, CAPEX, Working Capital  
- Automatically writes structured inputs into **pre-formatted Excel templates**  

### 5. 📈 Interactive Stock Charts  
- OHLC charts spanning the last 5 years  
- Toggle between multiple financial and valuation metrics  
- Cleanly integrated into the dashboard  

### 6. 🧾 Excel Automation (via `xlwings`)  
- Populates **DCF** and **CCA** worksheets with one click  
- Fills in formulas, assumptions, peer tables, and output valuation metrics  
- Seamlessly updates macro-enabled Excel models for any public U.S. company  

---

## 📁 Project Structure

```bash
.
├── app.py                                # Main Streamlit app
├── data_fetcher.py                       # Pulls Alpha Vantage financial data
├── comparable_company_analysis.py        # OpenAI + peer analysis
├── stock_chart.py                        # OHLC data and chart generation
├── dcfExcel.py                           # DCF Excel writer
├── dcfModel.py                           # DCF model logic and calculations
├── ccaExcel.py                           # CCA Excel automation
├── style.css                             # Custom Streamlit styling
├── data/                                 # Stored JSONs from API or uploads
│   ├── META_financials.json
│   ├── META_chart.json
│   └── META_comparable_analysis.json
├── models/
│   └── valuation.xlsm                    # Excel model used for automation
├── log data/
│   └── META_calculation_data.txt         # Raw DCF calculation log
```

---

## 📌 Notes  
- Currently supports **U.S. public companies** only  
- Requires valid API keys for [Alpha Vantage](https://www.alphavantage.co), [FMP](https://financialmodelingprep.com), and [OpenAI](https://openai.com)  
- Excel macros must be **enabled** for full functionality  

---

## 📬 Coming Soon  
- Relative Valuation Multiples (P/E, EV/EBITDA, etc.)  
- Sector benchmarking and valuation summaries  
- Enhanced UI with multi-company dashboards  
