import os
import json
import pandas as pd

# Configuration
symbol = "GOOGL"
base_folder = "Financial Position"
financials_file_path = os.path.join(base_folder, f"{symbol}_financials.json")
ratios_file_path = os.path.join(base_folder, f"{symbol}_calculated_ratios.json")
output_excel_path = os.path.join(base_folder, f"{symbol}_Financial_Model.xlsx")

# Load Data
with open(financials_file_path, "r") as file:
    financial_data = json.load(file)

with open(ratios_file_path, "r") as file:
    ratios_data = json.load(file)

# Helper Function
def get_value(report, key):
    value = report.get(key)
    if value is None or value in ["None", "N/A", "-", "--"]:
        return 0
    try:
        return float(value.replace(',', '').replace('$', '').strip())
    except:
        return 0

# Extract Financial Data
latest_cash_flow = financial_data['cash_flow']['annualReports'][0]
latest_balance_sheet = financial_data['balance_sheet']['annualReports'][0]
overview = financial_data.get('overview', {})

# FCF Calculation
operating_cash_flow = get_value(latest_cash_flow, 'operatingCashflow')
capex = get_value(latest_cash_flow, 'capitalExpenditures')
fcf = operating_cash_flow - capex

# Debt, Cash, Shares
debt = get_value(latest_balance_sheet, 'shortLongTermDebtTotal') + get_value(latest_balance_sheet, 'longTermDebt')
cash = get_value(latest_balance_sheet, 'cashAndCashEquivalentsAtCarryingValue')
shares_outstanding = get_value(overview, 'SharesOutstanding')

# DCF Assumptions
wacc = 0.10
terminal_growth_rate = 0.03
fcf_growth_rate = 0.05
forecast_years = 5

# Forecasting & Discounting
forecast = []
for year in range(1, forecast_years + 1):
    fcf *= (1 + fcf_growth_rate)
    discount_factor = 1 / ((1 + wacc) ** year)
    discounted_fcf = fcf * discount_factor
    forecast.append((year, fcf, discount_factor, discounted_fcf))

# Terminal Value Calculation
terminal_value = fcf * (1 + terminal_growth_rate) / (wacc - terminal_growth_rate)
discounted_terminal_value = terminal_value / ((1 + wacc) ** forecast_years)

# Enterprise & Equity Value
enterprise_value = sum(f[3] for f in forecast) + discounted_terminal_value
equity_value = enterprise_value - debt + cash
intrinsic_value_per_share = equity_value / shares_outstanding if shares_outstanding else None

# DataFrames for Excel
assumptions_df = pd.DataFrame({
    "Item": ["Starting FCF", "FCF Growth Rate", "WACC", "Terminal Growth Rate", "Debt", "Cash", "Shares Outstanding"],
    "Value": [operating_cash_flow - capex, fcf_growth_rate, wacc, terminal_growth_rate, debt, cash, shares_outstanding]
})

forecast_df = pd.DataFrame(forecast, columns=["Year", "Free Cash Flow", "Discount Factor", "Discounted FCF"])

valuation_df = pd.DataFrame({
    "Item": ["PV of Cash Flows", "PV of Terminal Value", "Enterprise Value", "- Debt", "+ Cash", "Equity Value", "Shares Outstanding", "Intrinsic Value per Share"],
    "Value": [
        sum(f[3] for f in forecast),
        discounted_terminal_value,
        enterprise_value,
        -debt,
        cash,
        equity_value,
        shares_outstanding,
        intrinsic_value_per_share
    ]
})

summary_df = pd.DataFrame({
    "Key Metric": ["Intrinsic Value per Share", "Enterprise Value", "Equity Value"],
    "Value": [intrinsic_value_per_share, enterprise_value, equity_value]
})

# Convert Ratios JSON to DataFrame
ratio_rows = []
for category, metrics in ratios_data.items():
    for metric_name, value in metrics.items():
        ratio_rows.append({
            "Category": category,
            "Metric": metric_name,
            "Value": value
        })

ratios_df = pd.DataFrame(ratio_rows)

# Export Everything to Excel (No Graphing, Just Clean Data)
with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
    assumptions_df.to_excel(writer, sheet_name="Assumptions", index=False)
    forecast_df.to_excel(writer, sheet_name="Forecast", index=False)
    valuation_df.to_excel(writer, sheet_name="Valuation", index=False)
    summary_df.to_excel(writer, sheet_name="Summary Dashboard", index=False)
    ratios_df.to_excel(writer, sheet_name="Financial Ratios", index=False)

    workbook = writer.book

    # Formatting columns in all sheets
    for sheet in ["Assumptions", "Forecast", "Valuation", "Summary Dashboard", "Financial Ratios"]:
        worksheet = writer.sheets[sheet]
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 20)

    # Optional: Highlight headers for each sheet
    header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#DDEBF7'})
    for sheet in ["Assumptions", "Forecast", "Valuation", "Summary Dashboard", "Financial Ratios"]:
        worksheet = writer.sheets[sheet]
        for col_num, value in enumerate(ratios_df.columns.values if sheet == "Financial Ratios" else assumptions_df.columns.values):
            worksheet.write(0, col_num, value, header_format)

print(f"✅ Combined Financial Model saved to: {output_excel_path}")
