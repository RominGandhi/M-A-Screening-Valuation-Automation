# 📊 Mergers & Acquisitions (M&A) Valuation & Screening 🚀

## 🏆 Overview
This project focuses on the valuation and screening of potential acquisition targets using **Discounted Cash Flow (DCF) analysis, Comparable Company Analysis (CCA), and financial ratio analysis**. The goal is to identify suitable M&A candidates based on intrinsic and relative valuation metrics.

## ✨ Features
- 🔢 **DCF Model**: Automates the calculation of enterprise value by forecasting future cash flows and discounting them using the Weighted Average Cost of Capital (WACC).
- 📈 **Comparable Company Analysis (CCA)**: Benchmarks target companies against industry peers using key valuation multiples.
- 📊 **Financial Ratios**: Assesses company health and profitability through metrics such as P/E, EV/EBITDA, ROE, ROA, and Debt-to-Equity.
- ⚙️ **Automated Data Retrieval**: Fetches financial data from APIs and processes input files for real-time analysis.
- 🎯 **Sensitivity Analysis**: Provides valuation ranges based on different assumptions for growth rate, WACC, and terminal value.

## 🔍 Methodology
### 1️⃣ Data Collection
- 🏦 Financial statements and market data are sourced from APIs such as **Yahoo Finance, Alpha Vantage, or Bloomberg Terminal**.
- 📂 User-uploaded CSV files can also serve as input for analysis.

### 2️⃣ Discounted Cash Flow (DCF) Model
- 📊 Extracts historical **EBIT**, **Depreciation & Amortization**, **Capital Expenditures**, and **Changes in Working Capital**.
- 🔮 Forecasts Free Cash Flow to the Firm (FCFF) over a 5-year period.
- 🏛 Determines Terminal Value using the **Gordon Growth Model**.
- 💰 Calculates Enterprise Value by discounting FCFF at the **Weighted Average Cost of Capital (WACC)**.

### 3️⃣ Comparable Company Analysis (CCA)
- 📌 Identifies peer companies within the same industry.
- 📉 Computes valuation multiples:
  - 📊 **EV/EBITDA** (Enterprise Value to EBITDA)
  - 💲 **P/E Ratio** (Price to Earnings)
  - 📘 **P/B Ratio** (Price to Book)
  - 🏭 **EV/Sales** (Enterprise Value to Sales)
- ⚖️ Compares the target company’s multiples with industry averages.

### 4️⃣ Financial Ratio Analysis
- 📈 **Profitability Metrics**: ROE (Return on Equity), ROA (Return on Assets), Gross Margin
- 💳 **Leverage Ratios**: Debt-to-Equity, Interest Coverage Ratio
- 💵 **Liquidity Ratios**: Current Ratio, Quick Ratio

### 5️⃣ Screening & Decision Framework
- 📊 Ranks companies based on valuation attractiveness and financial stability.
- ❌ Applies filters to exclude companies with excessive debt, declining profitability, or overvaluation.

## 🛠️ Usage
### 📌 Prerequisites
- 🐍 **Python 3.x**
- 📦 Libraries: `pandas`, `numpy`, `scipy`, `matplotlib`, `yfinance` (or `alpha_vantage` for API data)

### ▶️ Running the Project
1️⃣ Clone the repository:
   ```bash
   git clone https://github.com/your-repo/mna-valuation.git
   cd mna-valuation
   ```
2️⃣ Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3️⃣ Run the valuation script:
   ```bash
   python main.py --target "AAPL" --method "DCF"
   ```

## 📤 Outputs
- 📄 **Valuation Report** (PDF/CSV): Summarizes key findings, including intrinsic valuation and relative analysis.
- 📊 **Graphs & Charts**: Visual representation of financial metrics and valuation ranges.
- 🏆 **Decision Scorecard**: Provides an M&A recommendation based on a weighted scoring system.

## 🚀 Future Enhancements
- 🎲 **Monte Carlo Simulation** for probabilistic DCF modeling.
- 🤖 **Machine Learning Integration** to enhance screening accuracy.
- 🌐 **Web Interface** for interactive valuation and reporting.

## 👥 Contributors
- **Romin Gandhi** (Lead Developer, Finance & Valuation Modeling)

