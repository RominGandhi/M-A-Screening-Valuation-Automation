import json
import os
from datetime import datetime

# === CONFIG ===
symbol = "GOOGL"
base_path = "Financial Position"
financials_file = os.path.join(base_path, f"{symbol}_financials.json")
dcf_output_file = os.path.join(base_path, f"{symbol}_dcf_model.json")
openai_api_key = "sk-proj-h453yD0XZwlTBSUfcCV63GceU990l3MpvT7f-gO4ubRgyQsG9NPXH9EjNWqhM1gXbfub8yFNf6T3BlbkFJly3AFpNj
K5u0V4NeqrpzgCLBVAzuDGMseAR2rorORdze3awmvfYBXXMTPFdgL8MRigS6IwLnAA"
# === Load Financial Data ===
with open(financials_file, "r") as file:
    financial_data = json.load(file)

overview = financial_data.get('overview', {})
latest_balance_sheet = financial_data['balance_sheet']['annualReports'][0]
latest_income_statement = financial_data['income_statement']['annualReports'][0]
latest_cash_flow = financial_data['cash_flow']['annualReports'][0]

# === Helper to Extract a Value ===
def get_value(report, key):
    value = report.get(key)
    if value is None or value in ["None", "N/A", "-", "--"]:
        return 0
    try:
        return float(value.replace(',', '').replace('$', '').strip())
    except (ValueError, AttributeError):
        return 0

# === Directly Extract Required Fields ===
fiscal_year_end = latest_balance_sheet.get('fiscalDateEnding', 'Unknown')
cash = get_value(latest_balance_sheet, 'cashAndCashEquivalentsAtCarryingValue')
debt = get_value(latest_balance_sheet, 'shortLongTermDebtTotal')
capex = get_value(latest_cash_flow, 'capitalExpenditures')
current_price = get_value(overview, '200DayMovingAverage')  # Use latest price from overview (if available)
shares_outstanding = get_value(overview, 'SharesOutstanding')
ev_to_ebitda = get_value(overview, 'EVToEBITDA')

# Tax Rate directly from Income Statement
income_before_tax = get_value(latest_income_statement, 'incomeBeforeTax')
income_tax_expense = get_value(latest_income_statement, 'incomeTaxExpense')
tax_rate = income_tax_expense / income_before_tax if income_before_tax else 0

# Perpetual Growth Rate (can be constant or sector-based if you want)
perpetual_growth_rate = 0.025  # You can override this based on your model assumptions.

# Discount Rate (can be pulled directly if stored in overview, or hardcoded if known)
wacc = get_value(overview, 'WeightedAverageCostOfCapital')  # Or hardcode if you prefer.

# Transaction Date (today)
transaction_date = datetime.today().strftime('%Y-%m-%d')

# === Final JSON Output ===
dcf_model = {
    "Transaction Date": transaction_date,
    "Fiscal Year End": fiscal_year_end,
    "Current Price": current_price,
    "Shares Outstanding": shares_outstanding,
    "Debt": debt,
    "Cash": cash,
    "Capex": capex,
    "Tax Rate": tax_rate,
    "Discount Rate (WACC)": wacc,
    "Perpetual Growth Rate": perpetual_growth_rate,
    "EV/EBITDA Multiple": ev_to_ebitda
}

# === Save to File ===
if not os.path.exists(base_path):
    os.makedirs(base_path)

with open(dcf_output_file, "w") as outfile:
    json.dump(dcf_model, outfile, indent=4)

print(f"✅ DCF Model saved to: {dcf_output_file}")
