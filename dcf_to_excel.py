import json
import openpyxl
import os


# === Config ===
symbol = "GOOGL"
dcf_file_path = r"D:\Projects\In works\Financial Position\GOOGL_dcf_model.json"
excel_file_path = r"D:\Projects\In works\DCF Model\CFI-DCF-Model.xlsx"

os.startfile(excel_file_path)

# === Ensure Files Exist ===
if not os.path.exists(dcf_file_path):
    raise FileNotFoundError(f"DCF file not found: {dcf_file_path}")

if not os.path.exists(excel_file_path):
    raise FileNotFoundError(f"Excel file not found: {excel_file_path}")

# === Load DCF Data ===
with open(dcf_file_path, "r") as file:
    dcf_data = json.load(file)

# === Open Excel Workbook ===
wb = openpyxl.load_workbook(excel_file_path)
sheet = wb.active  # Update if needed to target a specific sheet (like 'DCF Inputs')

# === Map DCF Data to Excel Cells ===
cell_mapping = {
    "Tax Rate": "D5",
    "Discount Rate": "D6",
    "Perpetual Growth Rate": "D7",
    "EV/EBITDA Multiple": "D8",
    "Transaction Date": "D9",
    "Fiscal Year End": "D10",
    "Current Price": "D11",
    "Shares Outstanding": "D12",
    "Debt": "D13",
    "Cash": "D14",
    "Capex": "D15"
}

# === Write Data to Cells ===
sheet[cell_mapping["Tax Rate"]] = dcf_data["Tax Rate"]
sheet[cell_mapping["Discount Rate"]] = dcf_data["Discount Rate (WACC)"]
sheet[cell_mapping["Perpetual Growth Rate"]] = dcf_data["Perpetual Growth Rate"]
sheet[cell_mapping["EV/EBITDA Multiple"]] = dcf_data.get("EV/EBITDA Multiple", "N/A")
sheet[cell_mapping["Transaction Date"]] = dcf_data["Transaction Date"]
sheet[cell_mapping["Fiscal Year End"]] = dcf_data["Fiscal Year End"]
sheet[cell_mapping["Current Price"]] = dcf_data["Current Price"]
sheet[cell_mapping["Shares Outstanding"]] = dcf_data["Shares Outstanding"]
sheet[cell_mapping["Debt"]] = dcf_data["Debt"]
sheet[cell_mapping["Cash"]] = dcf_data["Cash"]
sheet[cell_mapping["Capex"]] = dcf_data["Capex"]

# === Save Workbook ===
wb.save(excel_file_path)

print(f"✅ DCF data successfully written to: {excel_file_path}")
