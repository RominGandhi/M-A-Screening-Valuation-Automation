import json
import openpyxl

# === Configuration ===
symbol = "AAPL"  # Change this if you want to work with a different ticker
input_json_path = f"Financial Position/{symbol}_comparable_analysis.json"
output_excel_path = r"D:\Projects\In works\CCA\CFI-Comparable-Company-Analysis-Template.xlsx"

# === Load JSON Data ===
with open(input_json_path, "r") as f:
    data = json.load(f)

# === Load Existing Workbook ===
wb = openpyxl.load_workbook(output_excel_path)
sheet = wb.active  # Update if you want a specific sheet, like sheet["Sheet1"]

# === Define Starting Row for Target and Peers ===
start_row = 7

# === Helper Function to Write One Row ===
def write_company_metrics(sheet, row, name, metrics):
    sheet[f"B{row}"] = name
    sheet[f"C{row}"] = metrics["Price ($/share)"]
    sheet[f"D{row}"] = metrics["Market Cap ($M)"]
    sheet[f"E{row}"] = metrics["Enterprise Value ($M)"]
    sheet[f"G{row}"] = metrics["Sales ($M)"]
    sheet[f"H{row}"] = metrics["EBITDA ($M)"]
    sheet[f"I{row}"] = metrics["EBIT ($M)"]
    sheet[f"J{row}"] = metrics["Earnings ($M)"]

# === Write Target Company (GOOGL) at Row 7 ===
target = data["target"]
write_company_metrics(sheet, start_row, target["ticker"], target["financial_metrics"])

# === Write Peers Below Target (row 8 onwards) ===
row = start_row + 1
for peer, peer_data in data["peers"].items():
    write_company_metrics(sheet, row, peer, peer_data["financial_metrics"])
    row += 1

# === Save Back to Same Excel File ===
wb.save(output_excel_path)
print(f"✅ Data written successfully to: {output_excel_path}")
