import json
import xlwings as xw
import time

def write_to_excel(symbol):
    input_json_path = f"data/{symbol}_comparable_analysis.json"
    financials_json_path = f"data/{symbol}_financials.json"
    base_sheet_name = "CCA"
    new_sheet_name = f"{symbol.upper()}_CCA"
    excel_path = r"D:\Projects\In works\models\Comparable Company Analysis Model.xlsm"

    # === Load JSON Data ===
    with open(input_json_path, "r") as f:
        data = json.load(f)

    with open(financials_json_path, "r") as f:
        financials = json.load(f)

    # === Open Excel Workbook ===
    app = xw.App(visible=False)
    try:
        wb = app.books.open(excel_path)
        time.sleep(1)

        # === Delete sheet if it already exists ===
        if new_sheet_name in [s.name for s in wb.sheets]:
            wb.sheets[new_sheet_name].delete()

        # === Copy base CCA sheet ===
        base_sheet = wb.sheets[base_sheet_name]
        base_sheet.api.Copy(After=wb.sheets[wb.sheets.count - 1].api)
        sheet = wb.sheets[wb.sheets.count - 1]
        sheet.name = new_sheet_name

        # === Clear relevant cells ===
        for cell in ["C4", "C5", "C24", "C25", "C26", "C30", "C32"]:
            sheet.range(cell).clear_contents()

        # === Write Company Name to C4 ===
        company_name = financials.get("overview", {}).get("Name", "")
        sheet.range("C4").value = company_name

        # === Get latest balance sheet report ===
        balance_reports = financials.get("balance_sheet", {}).get("annualReports", [])
        if balance_reports:
            latest_balance = max(balance_reports, key=lambda r: r.get("fiscalDateEnding", ""))
            fiscal_year = latest_balance.get("fiscalDateEnding")
            shares_outstanding = int(latest_balance.get("commonStockSharesOutstanding", 0))
            sheet.range("C5").value = fiscal_year
            sheet.range("C30").value = shares_outstanding

        # === Get latest income report ===
        income_reports = financials.get("income_statement", {}).get("annualReports", [])
        if income_reports:
            latest_income = max(income_reports, key=lambda r: r.get("fiscalDateEnding", ""))
            net_income = int(latest_income.get("netIncome", 0))
            ebit = latest_income.get("ebit", "")
            ebitda = latest_income.get("ebitda", "")
            sheet.range("C26").value = net_income
            sheet.range("C25").value = ebit
            sheet.range("C24").value = ebitda

        # === Extract Previous Close ===
        previous_close = float(financials.get("quote", {}).get("Global Quote", {}).get("08. previous close", 0))
        if previous_close:
            sheet.range("C32").value = previous_close

        # === Helper Function ===
        def write_company_metrics(sheet, row, name, metrics):
            sheet.range(f"B{row}:J{row}").clear_contents()
            sheet.range(f"B{row}").value = name
            sheet.range(f"C{row}").value = metrics.get("Price ($/share)", "")
            sheet.range(f"D{row}").value = metrics.get("Market Cap ($M)", "")
            sheet.range(f"E{row}").value = metrics.get("Enterprise Value ($M)", "")
            sheet.range(f"G{row}").value = metrics.get("Sales ($M)", "")
            sheet.range(f"H{row}").value = metrics.get("EBITDA ($M)", "")
            sheet.range(f"I{row}").value = metrics.get("EBIT ($M)", "")
            sheet.range(f"J{row}").value = metrics.get("Earnings ($M)", "")

        # === Write Peer Companies (up to 5) Starting from Row 11 ===
        row = 11
        for i, (peer, peer_data) in enumerate(data["peers"].items()):
            if i >= 5:
                break
            write_company_metrics(sheet, row, peer, peer_data["financial_metrics"])
            row += 1

        wb.save()
        print(f"✅ Data successfully written to sheet: {new_sheet_name}")

    except Exception as e:
        print(f"❌ Error writing to Excel: {e}")
    finally:
        if 'wb' in locals():
            wb.close()
        app.quit()
