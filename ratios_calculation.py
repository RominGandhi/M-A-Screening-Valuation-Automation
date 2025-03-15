import json
import os

# Path to your financials JSON file (modify symbol to test different companies)
symbol = "GOOGL"
file_path = os.path.join("Financial Position", f"{symbol}_financials.json")

# Load JSON Data
with open(file_path, "r") as file:
    financial_data = json.load(file)

# Helper function to safely extract a value
def get_value(report, key):
    """
    Safely extract numeric value from financial report data.
    Handles missing fields, non-numeric entries, and formatting issues.
    """
    value = report.get(key)
    if value is None or value in ["None", "N/A", "-", "--"]:
        print(f"⚠️ Warning: Missing '{key}' - assuming 0")
        return 0
    try:
        return float(value.replace(',', '').replace('$', '').strip())
    except (ValueError, AttributeError):
        print(f"⚠️ Warning: Invalid '{key}' value - assuming 0")
        return 0

# Extract latest year data (most recent annual report)
latest_balance_sheet = financial_data['balance_sheet']['annualReports'][0]
latest_income_statement = financial_data['income_statement']['annualReports'][0]
latest_cash_flow = financial_data['cash_flow']['annualReports'][0]

# Extract balance sheet data
total_assets = get_value(latest_balance_sheet, 'totalAssets')
total_liabilities = get_value(latest_balance_sheet, 'totalLiabilities')
total_equity = get_value(latest_balance_sheet, 'totalShareholderEquity')
current_assets = get_value(latest_balance_sheet, 'totalCurrentAssets')
current_liabilities = get_value(latest_balance_sheet, 'totalCurrentLiabilities')
cash = get_value(latest_balance_sheet, 'cashAndCashEquivalentsAtCarryingValue')
inventory = get_value(latest_balance_sheet, 'inventory')  # May not exist in tech companies

# Extract income statement data
revenue = get_value(latest_income_statement, 'totalRevenue')
net_income = get_value(latest_income_statement, 'netIncome')
ebit = get_value(latest_income_statement, 'operatingIncome')
interest_expense = get_value(latest_income_statement, 'interestExpense')

# Extract cash flow data
operating_cash_flow = get_value(latest_cash_flow, 'operatingCashflow')
capital_expenditures = get_value(latest_cash_flow, 'capitalExpenditures')

# Ratios Calculation
ratios = {
    "Liquidity Ratios": {
        "Current Ratio": current_assets / current_liabilities if current_liabilities else None,
        "Quick Ratio": (current_assets - inventory) / current_liabilities if current_liabilities else None
    },
    "Leverage Ratios": {
        "Debt/Equity Ratio": total_liabilities / total_equity if total_equity else None,
        "Liability/Assets Ratio": total_liabilities / total_assets if total_assets else None,
        "Interest Coverage Ratio": ebit / interest_expense if interest_expense else None
    },
    "Profitability Ratios": {
        "Net Margin": net_income / revenue if revenue else None,
        "ROE (Return on Equity)": net_income / total_equity if total_equity else None,
        "ROA (Return on Assets)": net_income / total_assets if total_assets else None
    },
    "Efficiency Ratios": {
        "Asset Turnover": revenue / total_assets if total_assets else None
    },
    "Cash Flow Ratios": {
        "Free Cash Flow": operating_cash_flow - capital_expenditures
    }
}

# OPTIONAL: Get Market Cap directly from Overview if your JSON includes it
if 'overview' in financial_data and 'MarketCapitalization' in financial_data['overview']:
    market_cap = get_value(financial_data['overview'], 'MarketCapitalization')
else:
    market_cap = 0  # You could also fetch from yfinance if needed

# Optional: Valuation multiples (require market cap & share price, or can be skipped for private companies)
ebitda = get_value(latest_income_statement, 'ebitda')

enterprise_value = market_cap + total_liabilities - cash

ratios["Valuation Multiples"] = {
    "EV/EBITDA": enterprise_value / ebitda if ebitda else None,
    "P/E Ratio": market_cap / net_income if net_income else None
}

# Display all ratios
print(f"\n📊 Financial Ratios for {symbol} (Latest Year)\n")
for category, metrics in ratios.items():
    print(f"{category}:")
    for ratio_name, value in metrics.items():
        if value is not None:
            print(f"  {ratio_name}: {value:.2f}")
        else:
            print(f"  {ratio_name}: Data not available")
    print()

# Optional: Save ratios to a file for further analysis
output_file = os.path.join("Financial Position", f"{symbol}_calculated_ratios.json")
with open(output_file, "w") as outfile:
    json.dump(ratios, outfile, indent=4)

print(f"✅ Ratios saved to: {output_file}")
