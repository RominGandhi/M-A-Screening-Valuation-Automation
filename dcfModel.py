import json
import pandas as pd
import requests
from dcfExcel import write_to_excel
from contextlib import redirect_stdout
import os
from contextlib import redirect_stdout
import os

def dcf_data(ticker: str):
    # Prepare folder and file
    output_dir = "calculation data"
    os.makedirs(output_dir, exist_ok=True)
    log_file_path = os.path.join(output_dir, f"{ticker}_calculation_data.txt")

    # Redirect all print output to the file
    with open(log_file_path, "w", encoding="utf-8") as f:
        with redirect_stdout(f):
            run_dcf_model(ticker)  # your main logic is moved to a helper function


def run_dcf_model(ticker: str):
    
    json_file_path = f"data/{ticker}_financials.json"
    comp_file_path = f"data/{ticker}_comparable_analysis.json"

    with open(json_file_path, "r") as f:
        financials = json.load(f)

    with open(comp_file_path, "r") as f:
        comp_data = json.load(f)

    
    # === EXTRACT INCOME STATEMENTS ===
    income_reports = financials["income_statement"]["annualReports"]
    # Fix: sort by date (descending) to make sure most recent is first
    income_reports.sort(key=lambda x: x["fiscalDateEnding"], reverse=True)
    latest_report = income_reports[0]
    new_year = latest_report["fiscalDateEnding"].split("-")[0]


    # === CORPORATE TAX RATE ===
    try:
        income_before_tax = float(latest_report["incomeBeforeTax"])
        tax_expense = float(latest_report["incomeTaxExpense"])
        if income_before_tax <= 0:
            tax_rate_corp = 0
        else:
            tax_rate_corp = tax_expense / income_before_tax
    except (KeyError, ValueError) as e:
        tax_rate_corp = None

    # === DISPLAY BASIC INFO ===
    print(f"📅 Last Fiscal Year: {new_year}\n")

    # === DISPLAY CORPORATE TAX RATE ===
    print("🏛️ Corporate Tax Rate Calculation:")
    print(f"Income Before Tax: ${income_before_tax:,.0f}")
    print(f"Income Tax Expense: ${tax_expense:,.0f}")
    print(f"Tax Rate = {tax_expense:,.0f} ÷ {income_before_tax:,.0f} = {tax_rate_corp:.2%}\n")

    def get_size_premium_from_json(financials):
        """
        Automatically fetches the market cap from financials JSON and returns the estimated size premium.
        """
        try:
            market_cap_str = financials["overview"]["MarketCapitalization"]
            market_cap = float(market_cap_str)
        except (KeyError, ValueError):
            print("Market Capitalization not available or invalid.")
            return 0.0

        # Market cap brackets in USD (Duff & Phelps)
        brackets = [
            (float('inf'), 264_000_000_000),
            (264_000_000_000, 51_900_000_000),
            (51_900_000_000, 20_600_000_000),
            (20_600_000_000, 11_700_000_000),
            (11_700_000_000, 7_700_000_000),
            (7_700_000_000, 4_500_000_000),
            (4_500_000_000, 2_550_000_000),
            (2_550_000_000, 1_100_000_000),
            (1_100_000_000, 500_000_000),
            (500_000_000, 0)
        ]

        size_premiums = [
            0.00,
            0.20,
            0.45,
            0.70,
            0.95,
            1.20,
            1.65,
            2.25,
            3.25,
            5.00
        ]

        for i, (upper, lower) in enumerate(brackets):
            if lower <= market_cap < upper:
                premium = size_premiums[i]
                print(f"🏷️ Market Cap: ${market_cap:,.0f} → Size Premium: {premium:.2f}%")
                return premium

        print("⚠️ Market cap did not match any bracket. Defaulting to 0.00%.")
        return 0.0

    size_premium = get_size_premium_from_json(financials)


    # === NET SALES (Latest Year: 2024A) ===
    try:
        revenue_2024 = float(latest_report["totalRevenue"])
        print(f"🟢 2024A Net Sales (Total Revenue): ${revenue_2024:,.0f}\n")
    except (KeyError, ValueError):
        print("🟢 2024A Net Sales: Data not available.\n")

    # === NET SALES (3 years back, 2 years back, 1 year back) ===
    print("💵 Net Sales (Total Revenue):")

    revenues = []
    years = []

    for i in range(1, 4):  # From 1 year back to 3 years back
        try:
            report = income_reports[i]
            year = report["fiscalDateEnding"].split("-")[0]
            revenue = float(report["totalRevenue"])
            revenues.append(revenue)
            years.append(year)
            print(f"{year}A: ${revenue:,.0f}")
        except (IndexError, KeyError, ValueError):
            print(f"{i} year(s) back: Data not available.")
            revenues.append(None)
            years.append("N/A")

    # === GROWTH CALCULATION: Year-3 → Year-2 ===
    if None not in revenues[-2:]:
        growth = (revenues[1] - revenues[2]) / revenues[2]
        print(f"\n📈 Revenue Growth from {years[2]} to {years[1]}: {growth:.2%}")
    else:
        print("\n📈 Revenue Growth from Year-3 to Year-2: Not enough data.")

    # === COGS (Cost of Goods Sold): 2024A to 3 years back ===
    print("\n🧾 COGS (Cost of Goods Sold):")

    cogs_list = []

    for i in range(0, 4):  # Include 2024A (i=0) to 3 years back
        try:
            report = income_reports[i]
            year = report["fiscalDateEnding"].split("-")[0]
            cogs = float(report["costOfRevenue"])
            cogs_list.append(cogs)
            print(f"{year}A: ${cogs:,.0f}")
        except (IndexError, KeyError, ValueError):
            print(f"{i} year(s) back: COGS data not available.")
            cogs_list.append(None)

    # === OPEX (Operating Expenses): 2024A to 3 years back ===
    print("\n🧾 Operating Expenses (OPEX):")

    opex_list = []

    for i in range(0, 4):  # Include 2024A to 3 years back
        try:
            report = income_reports[i]
            year = report["fiscalDateEnding"].split("-")[0]
            opex = float(report["operatingExpenses"])
            opex_list.append(opex)
            print(f"{year}A: ${opex:,.0f}")
        except (IndexError, KeyError, ValueError):
            print(f"{i} year(s) back: OPEX data not available.")
            opex_list.append(None)

    # === DEPRECIATION & AMORTIZATION: 2024A to 3 years back ===
    print("\n🧾 Depreciation & Amortization:")

    depr_list = []

    for i in range(0, 4):  # From 2024A to 3 years back
        try:
            report = income_reports[i]
            year = report["fiscalDateEnding"].split("-")[0]
            d_and_a = float(report["depreciationAndAmortization"])
            depr_list.append(d_and_a)
            print(f"{year}A: ${d_and_a:,.0f}")
        except (IndexError, KeyError, ValueError):
            print(f"{i} year(s) back: D&A data not available." )
            depr_list.append(None)


    import pandas as pd

    # === PARSE PEER METRICS ===
    peer_summary = []

    for peer_ticker, peer in comp_data["peers"].items():
        name = peer.get("overview", {}).get("companyName", "N/A")
        beta = peer.get("overview", {}).get("beta", "N/A")
        
        # Financial Metrics
        market_cap_m = peer.get("financial_metrics", {}).get("Market Cap ($M)", 0)
        enterprise_value_m = peer.get("financial_metrics", {}).get("Enterprise Value ($M)", 0)
        
        # Income Statement data for Tax Rate
        income_statement = peer.get("financials", {}).get("income_statement", {})
        income_before_tax = income_statement.get("incomeBeforeTax", 0)
        income_tax_expense = income_statement.get("incomeTaxExpense", 0)

        # Calculate tax rate if both values are available
        if income_before_tax != 0:
            tax_rate = round(income_tax_expense / income_before_tax, 4)  # rounded to 4 decimals
        else:
            tax_rate = "N/A"  # In case of zero or missing data

        # Market value calculations
        market_equity = market_cap_m * 1_000_000
        market_debt = (enterprise_value_m - market_cap_m) * 1_000_000  # EV - Equity = Debt (simplified)

        peer_summary.append({
            "Ticker": peer_ticker,
            "Company Name": name,
            "Beta (Leveraged)": beta,
            "Market Value of Equity ($)": round(market_equity, 2),
            "Market Value of Debt ($)": round(market_debt, 2),
            "Tax Rate": tax_rate  # Add Tax Rate
        })

    # === CONVERT TO DATAFRAME & DISPLAY ===
    df = pd.DataFrame(peer_summary)
    print(df)

    # === CALCULATE EBIT FOR THE PAST FOUR FISCAL YEARS ===
    print()
    # === EXTRACT EBIT AND EBITDA FOR PAST 4 FISCAL YEARS ===
    print("\n📊 EBIT and EBITDA for the Past 4 Fiscal Years:\n")

    # Loop through the most recent 4 years of reports
    for i in range(4):
        try:
            report = income_reports[i]
            fiscal_year = report["fiscalDateEnding"].split("-")[0]
            ebit = float(report["ebit"])
            ebitda = float(report["ebitda"])
            print(f"Fiscal Year {fiscal_year}:")
            print(f"  EBIT:   ${ebit:,.0f}")
            print(f"  EBITDA: ${ebitda:,.0f}\n")
        except (IndexError, KeyError, ValueError) as e:
            print(f"Fiscal Year {fiscal_year}: Data not available.\n")

    # === COST OF DEBT (Rd) CALCULATION ===
    def safe_float(value):
        try:
            return float(value) if value is not None and value != "None" else 0.0
        except ValueError:
            return 0.0

    interest_expense = safe_float(financials['income_statement']['annualReports'][0].get('interestExpense'))
    long_term_debt = float(financials['balance_sheet']['annualReports'][0]['longTermDebt'])  # Long-term Debt

    # Calculate the Cost of Debt (Rd)
    cost_of_debt = interest_expense / long_term_debt

    # Calculate the After-Tax Cost of Debt
    after_tax_cost_of_debt = cost_of_debt * (1 - tax_rate_corp)

    # Output the results
    print(f"\n🔴 Cost of Debt (Rd): {cost_of_debt:.2%}")
    print(f"🔴 After-Tax Cost of Debt: {after_tax_cost_of_debt:.2%}")


    # === CAPITAL EXPENDITURES (CAPEX): 2024A to 3 years back ===
    print("\n🏗️ Capital Expenditures (Capex):")

    capex_list = []
    for i in range(0, 4):  # From 2024A to 3 years back
        try:
            report = financials["cash_flow"]["annualReports"][i]
            year = report["fiscalDateEnding"].split("-")[0]
            capex = float(report["capitalExpenditures"])
            capex_list.append(capex)
            print(f"{year}A: ${capex:,.0f}")
        except (IndexError, KeyError, ValueError):
            print(f"{i} year(s) back: Capex data not available.")
            capex_list.append(None)


    print("\n🔁 Operating Working Capital (OWC) and Change (ΔOWC):")

    owc_list = []
    years = []

    # Helper function to safely convert values
    def safe_float(value):
        try:
            return float(value) if value is not None and value != "None" else 0.0
        except ValueError:
            return 0.0

    # Extract OWC for each year
    for i in range(4):  # From most recent (2024A) to 3 years back
        try:
            report = financials["balance_sheet"]["annualReports"][i]
            year = report["fiscalDateEnding"].split("-")[0]
            years.append(year)

            # Safe extraction with fallback to 0
            receivables = safe_float(report.get("currentNetReceivables"))
            inventory = safe_float(report.get("inventory"))
            other_current_assets = safe_float(report.get("otherCurrentAssets"))
            accounts_payable = safe_float(report.get("currentAccountsPayable"))
            other_current_liabilities = safe_float(report.get("otherCurrentLiabilities"))

            # OWC = (AR + Inventory + Other Current Assets) - (AP + Other Current Liabilities)
            owc = (receivables + inventory + other_current_assets) - (accounts_payable + other_current_liabilities)
            owc_list.append(owc)

            print(f"{year}A - OWC: ${owc:,.0f}")

        except (KeyError, IndexError) as e:
            years.append("N/A")
            owc_list.append(None)
            print(f"{i} year(s) back: OWC data not available.")

    # Compute change in OWC (ΔOWC)
    print("\n📉 Year-over-Year Change in Operating Working Capital (ΔOWC):")

    for i in range(1, len(owc_list)):
        if owc_list[i] is not None and owc_list[i - 1] is not None:
            delta = owc_list[i] - owc_list[i - 1]
            print(f"{years[i]}A - ΔOWC: ${delta:,.0f}")
        else:
            print(f"{years[i]}A - ΔOWC: Not enough data")


    print("\n💰 Total Debt and Cash & Cash Equivalents:")

    def safe_float(value):
        try:
            return float(value) if value is not None and value != "None" else 0.0
        except ValueError:
            return 0.0

    # Extract most recent year's balance sheet (2024A)
    report = financials["balance_sheet"]["annualReports"][0]

    # Extract values safely
    short_term_debt = safe_float(report.get("shortTermDebt"))
    long_term_debt = safe_float(report.get("longTermDebt"))
    cash = safe_float(report.get("cashAndCashEquivalentsAtCarryingValue"))

    # Calculate total debt
    total_debt = short_term_debt + long_term_debt

    # Print values
    print(f"Total Debt (2024A): ${total_debt:,.0f}")
    print(f"  ↳ Short-Term Debt: ${short_term_debt:,.0f}")
    print(f"  ↳ Long-Term Debt:  ${long_term_debt:,.0f}")
    print(f"Cash & Cash Equivalents (2024A): ${cash:,.0f}")

    print("\n📊 Shares Outstanding:")

    # Extract safely
    shares_outstanding = safe_float(report.get("commonStockSharesOutstanding"))

    print(f"Shares Outstanding (2024A): {shares_outstanding:,.0f} shares")

    # === COLLECT EBIT and EBITDA LISTS ===
    ebit_list = []
    ebitda_list = []

    for i in range(4):
        try:
            report = income_reports[i]
            ebit = float(report["ebit"])
            ebitda = float(report["ebitda"])
            ebit_list.append(ebit)
            ebitda_list.append(ebitda)
        except (IndexError, KeyError, ValueError):
            ebit_list.append(None)
            ebitda_list.append(None)

    # === Write to Excel ===
    write_to_excel(
    ticker,
    financials=financials,
    revenue_2024=revenue_2024,
    revenues=revenues,
    cogs_list=cogs_list,
    opex_list=opex_list,
    depr_list=depr_list,
    new_year=new_year,
    tax_rate_corp=tax_rate_corp,
    peer_summary=peer_summary,
    cost_of_debt=cost_of_debt,
    capex_list=capex_list,
    owc_list=owc_list,
    total_debt=total_debt,
    cash=cash,
    size_premium=size_premium,
    ebit_list=ebit_list,
    ebitda_list=ebitda_list,
    shares_outstanding=shares_outstanding
)



def dcf_data(ticker: str):
    # Prepare folder and file
    output_dir = "calculation data"
    os.makedirs(output_dir, exist_ok=True)
    log_file_path = os.path.join(output_dir, f"{ticker}_calculation_data.txt")

    # Redirect all print output to the file
    with open(log_file_path, "w", encoding="utf-8") as f:
        with redirect_stdout(f):
            run_dcf_model(ticker)  # your main logic is moved to a helper function



