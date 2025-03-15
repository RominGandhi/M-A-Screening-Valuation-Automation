import json
import os
import sys
import argparse
from openai import OpenAI

# === CONFIG ===
base_path = "Financial Position"

# === Helper Function to Safely Extract Numbers ===
def get_value(report, key):
    value = report.get(key)
    if value is None or value in ["None", "N/A", "-", "--"]:
        return 0
    try:
        return float(value.replace(',', '').replace('$', '').strip())
    except (ValueError, AttributeError):
        return 0

# === Calculate Compound Annual Growth Rate (CAGR) ===
def calc_cagr(start, end, periods):
    if start == 0 or periods <= 0:
        return 0
    return (end / start)**(1/periods) - 1

# === Fetch Industry Benchmarks via GPT-4o ===
def fetch_industry_benchmarks(sector):
    client = OpenAI()

    prompt = f"""
For the '{sector}' sector, provide the average:
- Revenue Growth Cap (in %)
- EBIT Margin (in %)
- D&A Margin (in %)
- Capex Margin (in %)
- Change in Operating Working Capital (ΔOWC) Margin (in %)

Please also provide the primary data sources (like Damodaran, Bloomberg, FactSet, or other reputable sources) you used to generate these numbers.

Respond only in this JSON format:
{{
    "Revenue Growth Cap": "x%",
    "EBIT Margin": "x%",
    "D&A Margin": "x%",
    "Capex Margin": "x%",
    "ΔOWC Margin": "x%",
    "Sources": "List the sources used"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a financial analyst specializing in valuation modeling."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content
    return json.loads(content)

# === Forecast Function ===
def forecast(ticker, num_years):
    financials_file = os.path.join(base_path, f"{ticker}_financials.json")
    projections_file = os.path.join(base_path, f"{ticker}_projections.json")

    with open(financials_file, "r") as file:
        financial_data = json.load(file)

    # === Extract Sector from Overview ===
    sector = financial_data.get('overview', {}).get('Sector', 'Unknown')
    print(f"🏢 Detected Sector for {ticker}: {sector}")

    # === Fetch Industry Benchmarks using GPT-4o ===
    print(f"🤖 Asking GPT-4o for industry standards for {sector}...")
    benchmarks = fetch_industry_benchmarks(sector)

    print(f"📊 Industry Benchmarks for {sector}:")
    print(json.dumps(benchmarks, indent=4))

    # Convert percentages to floats
    for key in benchmarks:
        if '%' in benchmarks[key]:
            benchmarks[key] = float(benchmarks[key].replace('%', '')) / 100

    income_statements = financial_data['income_statement']['annualReports']
    cash_flows = financial_data['cash_flow']['annualReports']
    balance_sheets = financial_data['balance_sheet']['annualReports']

    num_hist_years = min(len(income_statements), 5)
    if num_hist_years < 3:
        raise ValueError(f"Need at least 3 years of data to calculate reliable averages for {ticker}.")

    # === Collect Historical Data ===
    revenues, ebit_margins, da_margins, capex_margins, owc_changes = [], [], [], [], []

    for i in range(num_hist_years):
        revenue = get_value(income_statements[i], 'totalRevenue')
        ebit = get_value(income_statements[i], 'operatingIncome')
        da = get_value(cash_flows[i], 'depreciationDepletionAndAmortization')
        capex = abs(get_value(cash_flows[i], 'capitalExpenditures'))

        current_assets = get_value(balance_sheets[i], 'totalCurrentAssets')
        cash = get_value(balance_sheets[i], 'cashAndCashEquivalentsAtCarryingValue')
        current_liabilities = get_value(balance_sheets[i], 'totalCurrentLiabilities')
        debt_current = get_value(balance_sheets[i], 'currentDebt')  # If available

        owc = (current_assets - cash) - (current_liabilities - debt_current)

        if i > 0:
            prev_owc = (get_value(balance_sheets[i-1], 'totalCurrentAssets') -
                        get_value(balance_sheets[i-1], 'cashAndCashEquivalentsAtCarryingValue') -
                        (get_value(balance_sheets[i-1], 'totalCurrentLiabilities') -
                         get_value(balance_sheets[i-1], 'currentDebt')))
            owc_changes.append((owc - prev_owc) / revenue)

        revenues.append(revenue)
        ebit_margins.append(ebit / revenue)
        da_margins.append(da / revenue)
        capex_margins.append(capex / revenue)

    # === Historical Averages ===
    revenue_growth_rate = calc_cagr(revenues[-1], revenues[0], num_hist_years - 1)
    avg_ebit_margin = sum(ebit_margins) / num_hist_years
    avg_da_margin = sum(da_margins) / num_hist_years
    avg_capex_margin = sum(capex_margins) / num_hist_years
    avg_owc_change_margin = sum(owc_changes) / len(owc_changes)

    # === Apply Industry Caps (Guardrails) ===
    revenue_growth_rate = min(revenue_growth_rate, benchmarks['Revenue Growth Cap'])
    avg_ebit_margin = min(avg_ebit_margin, benchmarks['EBIT Margin'])
    avg_da_margin = min(avg_da_margin, benchmarks['D&A Margin'])
    avg_capex_margin = min(avg_capex_margin, benchmarks['Capex Margin'])
    avg_owc_change_margin = min(avg_owc_change_margin, benchmarks['ΔOWC Margin'])

    # === Project Future Years ===
    projected = []
    projected_revenue = revenues[0]

    for year in range(1, num_years + 1):
        projected_revenue *= (1 + revenue_growth_rate)
        projected.append({
            "Year": year,
            "Revenue": projected_revenue,
            "EBIT": projected_revenue * avg_ebit_margin,
            "D&A": projected_revenue * avg_da_margin,
            "Capex": projected_revenue * avg_capex_margin,
            "Change in OWC": projected_revenue * avg_owc_change_margin
        })

    # === Attach Source to Projection File ===
    output = {
        "Projections": projected,
        "Industry Source": benchmarks.get("Sources", "Provided by GPT-4o")
    }

    with open(projections_file, "w") as file:
        json.dump(output, file, indent=4)

    print(f"✅ Saved {num_years}-year projections to {projections_file}")
    print(f"🔗 Source: {benchmarks['Sources']}")

# === Run Script ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Forecast financials for a given ticker.")
    parser.add_argument("ticker", type=str, help="Ticker symbol")
    parser.add_argument("--years", type=int, default=5, help="Number of years to forecast (default: 5)")

    args = parser.parse_args()
    forecast(args.ticker.upper(), args.years)
