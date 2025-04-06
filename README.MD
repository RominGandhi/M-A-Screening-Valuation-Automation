# U.S. Public Company Valuation Model — DCF, CCA & WACC Automation

This repository presents a professional-grade valuation model designed for **any publicly traded U.S. company**, integrating both **Discounted Cash Flow (DCF)** and **Comparable Company Analysis (CCA)** methodologies. The model includes a macro-enabled Excel template dynamically populated using Python, with valuation commentary and peer benchmarking fully automated.

> 💡 Example included: Alphabet Inc. (GOOGL)

---

## 📈 Key Features

- 🔄 **Automated Excel population** using Python (`xlwings`)
- 📊 **Comparable Company Analysis (CCA)** with:
  - EV/Sales
  - EV/EBITDA
  - EV/EBIT
  - P/E multiples
- 📉 **Discounted Cash Flow (DCF)** model with:
  - Forecasted financials
  - WACC and terminal value assumptions
  - Present value of free cash flow
- 💬 **Dynamic valuation commentary** (e.g., "Alphabet Inc. appears undervalued by ~67% based on its peer-derived implied valuation.")
- 📈 **Professional visuals**: bar charts, valuation breakdowns, and share price comparison
- ⚙️ **JSON-based data loading** to keep input clean, auditable, and API-ready

---

## 🧾 How It Works

### 🔹 Input Files
- `symbol_comparable_analysis.json`: includes company and peer financials and multiples
- `symbol_financials.json`: includes income statement, balance sheet, and stock quote data

### 🔹 Python Script
- Parses both JSON files
- Writes target company and peer metrics to a pre-formatted Excel template
- Fills in assumptions (e.g., shares outstanding, net income, current price)
- Generates automated commentary and calculations for implied price/share

### 🔹 Excel Template (`.xlsm`)
- Pre-built valuation model with formulas and visuals
- CCA section dynamically updates with input
- DCF includes unlevered free cash flow forecast and terminal value
- Implied price/share and over/undervaluation commentary appear automatically

---

## 🧪 Example Output (GOOGL)

- Median P/E of peers: **30.72x**
- Implied equity value: **$3.07T**
- Shares outstanding: **12.2B**
- Implied price/share: **$251.89**
- Current price: **$150.72**

> **Result:**  
> `Alphabet Inc. Class A appears undervalued by approximately 67% based on its peer-derived implied valuation.`

---

## 🧰 Tools Used

| Tool        | Purpose                            |
|-------------|------------------------------------|
| **Python**  | Automation via `xlwings` and `json`|
| **Excel**   | Template model & formatting        |
| **CFI + IC**| Source of original template format |

---

## 🏗 Template Attribution

> 📌 The original Excel structure was based on templates from  
> - [Corporate Finance Institute (CFI)](https://corporatefinanceinstitute.com)  
> - Educational resources from **Investment Club (IC)** communities  
>  
> 🛠 However, this version was **heavily customized** to include:
> - Automated Python integration
> - Enhanced formatting
> - Additional input cells and logic
> - Custom commentary generation
> - Graph-ready data layouts

---

## 🗂 Project Structure

