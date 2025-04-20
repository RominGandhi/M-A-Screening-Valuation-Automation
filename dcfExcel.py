import xlwings as xw

def write_to_excel(
    ticker, financials, revenue_2024, revenues, cogs_list, opex_list, depr_list,
    new_year, tax_rate_corp, peer_summary, cost_of_debt, capex_list, owc_list,
    total_debt, cash, size_premium, ebit_list, ebitda_list, shares_outstanding
):
    try:
        excel_path = r"D:\Projects\In works\models\Discounted Cash Flow Model.xlsm"
        base_sheet_name = "DCF"
        new_sheet_name = f"{ticker.upper()}_DCF"

        app = xw.App(visible=False)
        wb = xw.Book(excel_path)

        # Delete existing sheet with the same name if it exists
        if new_sheet_name in [s.name for s in wb.sheets]:
            wb.sheets[new_sheet_name].delete()

        # Copy base DCF sheet
        base_sheet = wb.sheets[base_sheet_name]
        base_sheet.api.Copy(After=wb.sheets[wb.sheets.count - 1].api)
        ws = wb.sheets[wb.sheets.count - 1]
        ws.name = new_sheet_name

        # === BASIC COMPANY INFO ===
        ws["C4"].clear_contents()
        ws["C4"].value = financials["overview"]["Name"]

        ws["C5"].clear_contents()
        ws["C5"].value = new_year

        ws["C6"].clear_contents()
        ws["C6"].value = round(tax_rate_corp, 4) if tax_rate_corp is not None else ""

        # === REVENUE ===
        for cell, value in zip(["F11", "E11", "D11", "C11"], [revenue_2024] + revenues):
            ws[cell].clear_contents()
            ws[cell].value = round(value, 0) if value is not None else ""

        # === COGS ===
        for cell, value in zip(["F13", "E13", "D13", "C13"], cogs_list):
            ws[cell].clear_contents()
            ws[cell].value = round(value, 0) if value is not None else ""

        # === OPEX ===
        for cell, value in zip(["F16", "E16", "D16", "C16"], opex_list):
            ws[cell].clear_contents()
            ws[cell].value = round(value, 0) if value is not None else ""

        # === D&A ===
        for cell, value in zip(["F24", "E24", "D24", "C24"], depr_list):
            ws[cell].clear_contents()
            ws[cell].value = round(value, 0) if value is not None else ""


        # === EBIT ===
        for cell, value in zip(["F21", "E21", "D21", "C21"], ebit_list):
            ws[cell].clear_contents()
            ws[cell].value = round(value, 0) if value is not None else ""

        # === EBITDA ===
        for cell, value in zip(["F22", "E22", "D22", "C22"], ebitda_list):
            ws[cell].clear_contents()
            ws[cell].value = round(value, 0) if value is not None else ""






        # === PEER DATA (Company Name → Tax Rate) ===
        print("Writing peer comparable data...")
        for i, peer in enumerate(peer_summary[:5]):  # max 5 peers
            row = 31 + i
            for col, key in zip(["B", "C", "D", "E", "H"], 
                                ["Company Name", "Beta (Leveraged)", "Market Value of Debt ($)", "Market Value of Equity ($)", "Tax Rate"]):
                cell = f"{col}{row}"
                ws[cell].clear_contents()
                ws[cell].value = peer[key]

        # === COST OF DEBT ===
        ws["C58"].clear_contents()
        ws["C58"].value = cost_of_debt

        # === CAPEX ===
        for cell, value in zip(["F67", "E67", "D67", "C67"], capex_list):
            ws[cell].clear_contents()
            ws[cell].value = round(value, 0) if value is not None else ""

        # === OWC ===
        for cell, value in zip(["F69", "E69", "D69", "C69"], owc_list):
            ws[cell].clear_contents()
            ws[cell].value = round(value, 0) if value is not None else ""

        # === FINAL METRICS ===
        ws["C80"].clear_contents()
        ws["C80"].value = total_debt

        ws["C81"].clear_contents()
        ws["C81"].value = cash

        ws["C55"].clear_contents()
        ws["C55"].value = size_premium

        ws["C84"].clear_contents()
        ws["C84"].value = round(shares_outstanding, 0) if shares_outstanding is not None else ""


        wb.save()
        wb.close()
        app.quit()

        print(f"Data successfully written to Excel sheet: {new_sheet_name}")

    except Exception as e:
        print(f"Failed to write to Excel: {e}")
