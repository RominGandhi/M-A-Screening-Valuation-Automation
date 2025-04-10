
# 💼 Valuation and Financial Modeling Platform

A professional-grade **web-based financial modeling dashboard** powered by **Streamlit**, automating **Discounted Cash Flow (DCF)** and **Comparable Company Analysis (CCA)**. This tool enables **finance professionals**, **analysts**, and **students** to evaluate public companies using **real-time financial data**, **machine learning**, and **Excel-based models** — all in a user-friendly interface.

---

## 🎯 What This Platform Does

- 🔄 **Automates** DCF & CCA models in Excel
- 📡 **Fetches live data** from Alpha Vantage, FMP, and Yahoo Finance
- 🧠 Uses **OpenAI GPT** to generate peer companies
- 🧾 Parses financial statements to extract valuation inputs
- 📈 Displays clean **interactive charts**
- 📤 Accepts **uploaded financial JSON files**

---

## 🖼️ Demo

![Demo](exampleUI.gif)

---

## 🛠️ Features

### ✅ Streamlit-Powered Interface
- Sidebar for ticker entry, file uploads, and API key management
- Live preview of metrics and peer comparisons
- Responsive, browser-based dashboard

### ✅ Data Sources
- **Alpha Vantage**: Financial statements, quotes, and company overview
- **Financial Modeling Prep**: Peer company financials
- **Yahoo Finance**: OHLC stock price data
- **OpenAI**: Sector-based peer generation using GPT

### ✅ Excel Model Integration
- Fills a prebuilt macro-enabled Excel sheet using `xlwings`
- Extracts:
  - Revenue, COGS, OPEX, D&A, CAPEX
  - Changes in Operating Working Capital (ΔOWC)
  - Cost of Debt, Tax Rate, Size Premium
- Populates peer tables and output valuation fields

---

## 🧠 Example Use Case

> You’re analyzing **Apple Inc. (AAPL)** for a valuation project.
1. Launch the app
2. Enter the ticker `AAPL` and hit **Fetch**
3. The app:
   - Pulls AAPL’s financial data
   - Uses GPT to find comparable peers like MSFT, GOOG, etc.
   - Extracts valuation inputs and updates an Excel model
4. Download the fully populated **DCF Excel file** for boardroom-ready reporting

---

## 📁 Folder Structure

```
.
├── app.py                                # Streamlit app entry point
├── data_fetcher.py                       # Alpha Vantage data fetcher
├── dcfModel.py                           # Logic for DCF variable extraction
├── dcfExcel.py                           # Writes DCF data to Excel template
├── comparable_company_analysis.py        # GPT-based peer generator
├── ccaExcel.py                           # Excel automation for peer data
├── stock_chart.py                        # Historical OHLC stock data
├── style.css                             # UI styling
├── models/
│   └── valuation.xlsm                    # Preformatted Excel model
├── data/
│   ├── META_financials.json              # Sample input
│   ├── META_comparable_analysis.json     # GPT peer output
│   └── META_chart.json                   # OHLC chart data
├── log data/
│   └── AAPL_calculation_data.txt         # DCF variable logs
```

---

## 🚀 Getting Started

### 🔧 1. Clone the Repository

```bash
git clone https://github.com/yourusername/valuation-platform.git
cd valuation-platform
```

### 🧪 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔑 3. Set Up API Keys

Create a `.env` file:

```env
ALPHA_VANTAGE_API_KEY=your_alpha_key
FMP_API_KEY=your_fmp_key
OPENAI_API_KEY=your_openai_key
```

### ▶️ 4. Run the App

```bash
streamlit run app.py
```

Then visit `http://localhost:8501`.

---

## ⚙️ Requirements

- Python 3.9+
- Microsoft Excel (for `xlwings` integration)
- Internet connection
- Excel macros **must be enabled**

---

## 📌 Currently Supported

- ✔ U.S. public companies
- ✔ Real-time valuation using financial statements
- ✔ Automated Excel DCF + CCA modeling

---

## 🧰 Technologies Used

| Technology         | Purpose                          |
|--------------------|----------------------------------|
| **Streamlit**      | Web interface                    |
| **Python**         | Core logic and API integration   |
| **Alpha Vantage**  | Financial data                   |
| **FMP**            | Peer company metrics             |
| **OpenAI GPT**     | Peer identification              |
| **xlwings**        | Excel model population           |
| **Altair**         | Chart visualization              |

---

## 🧠 Potential Enhancements

- Valuation multiples (e.g., P/E, EV/EBITDA)
- Sector benchmarking
- PDF report export
- Global company support

---

## 🤝 Contributions

Pull requests are welcome. For major changes, please open an issue first to discuss your proposal.

---

## 📫 Contact

Built by **Romin Gandhi**  
📧 romingandhi.work@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/romingandhi)
