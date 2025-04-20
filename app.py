import streamlit as st 
import os
import json
import pandas as pd
import subprocess
from data_fetcher import fetch_and_save_financials
from chart_display import display_chart 
from ccaExcel import write_to_excel
from dcfModel import dcf_data, run_dcf_model


# === Page Setup ===
st.set_page_config(page_title="Valuation Dashboard", layout="wide")


# === Configurations ===
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# === Load External CSS ===
def load_css(file_path):
    if os.path.exists(file_path):
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# === Generate Missing Files ===
def generate_missing_data(ticker):
    chart_path = os.path.join(DATA_FOLDER, f"{ticker}_chart.json")
    comp_path = os.path.join(DATA_FOLDER, f"{ticker}_comparable_analysis.json")

    if not os.path.exists(chart_path):
        try:
            st.info(f"Generating chart data for {ticker}...")
            subprocess.run(["python", "stock_chart.py", ticker], check=True)
            st.success(f"{ticker}_chart.json generated successfully.")
        except subprocess.CalledProcessError as e:
            st.error(f"Error generating chart data: {e}")

    if not os.path.exists(comp_path):
        try:
            st.info(f"Generating comparable company analysis for {ticker}...")
            subprocess.run(["python", "comparable_company_analysis.py", ticker], check=True)
            st.success(f"{ticker}_comparable_analysis.json generated successfully.")
        except subprocess.CalledProcessError as e:
            st.error(f"Error generating comparable analysis: {e}")


# === Top Buttons ===
_, spacer, button_col = st.columns([4.5, 2, 2.5])
from dcfModel import run_dcf_model  # make sure this import is at the top of your app.py

with button_col:
    selected_action = st.selectbox("Select Analysis", ["Discounted Cash Flow Analysis", "Comparable Company Analysis"])
    
    if st.button("Run Analysis"):
        selected_ticker = st.session_state.get("selected_ticker")

        if not selected_ticker:
            st.warning("Please fetch or upload a company's financials first.")
        else:
            try:
                if selected_action == "Discounted Cash Flow Analysis":
                    dcf_data(selected_ticker)
                    st.success(f"DCF analysis completed. Log saved in log data/{selected_ticker}_calculation_data.txt")
                    run_dcf_model(selected_ticker)
                    try:
                        run_dcf_model(selected_ticker)
                        st.success(f"Excel updated with DCF results for {selected_ticker}")
                    except Exception as e:
                        st.error(f"Failed to run DCF analysis: {e}")
                elif selected_action == "Comparable Company Analysis":
                    write_to_excel(selected_ticker)
                    st.success(f"CCA Excel updated for {selected_ticker}")
            except Exception as e:
                st.error(f"Failed to run analysis: {e}")

        st.markdown("</div>", unsafe_allow_html=True)



# === Title and Instructions ===
st.title("Valuation Dashboard")
st.markdown(
    "<p style='font-size: 16px; color: #cccccc; margin-bottom: 20px;'>"
    "Enter a U.S. public company ticker symbol or upload a financial JSON to fetch company data."
    "</p>",
    unsafe_allow_html=True
)

# === Input Section ===
col1, spacer, col2 = st.columns([1.2, 0.5, 1.2])
selected_ticker = st.session_state.get("selected_ticker")

# Fetch Financials
with col1:
    st.subheader("Fetch by Ticker")
    ticker = st.text_input("Ticker Symbol", "GOOGL").upper()
    if st.button("Fetch Company Financials"):
        try:
            with st.spinner(f"Retrieving data for {ticker}..."):
                path = fetch_and_save_financials(ticker, output_folder=DATA_FOLDER)
            st.success(f"Financial data for {ticker} saved to: {path}")
            st.session_state["selected_ticker"] = ticker
            selected_ticker = ticker
            generate_missing_data(ticker)
        except Exception as e:
            st.error(f"Failed to fetch financial data: {e}")

# Upload JSON
with col2:
    st.subheader("Upload Financials")
    uploaded_file = st.file_uploader("Upload a financials JSON file", type="json", label_visibility="collapsed")

    if uploaded_file is not None:
        try:
            uploaded_data = json.load(uploaded_file)
            required_keys = ["balance_sheet", "income_statement", "cash_flow", "overview", "quote"]

            if all(key in uploaded_data for key in required_keys):
                with st.form("upload_form", clear_on_submit=True):
                    uploaded_ticker = st.text_input("Enter ticker for uploaded file").upper()
                    submitted = st.form_submit_button("Save Uploaded Financials")
                    if submitted and uploaded_ticker:
                        save_path = os.path.join(DATA_FOLDER, f"{uploaded_ticker}_financials.json")
                        with open(save_path, "w", encoding="utf-8") as f:
                            json.dump(uploaded_data, f, indent=4)
                        st.success(f"Uploaded data saved as {uploaded_ticker}_financials.json")
                        st.session_state["selected_ticker"] = uploaded_ticker
                        selected_ticker = uploaded_ticker
                        generate_missing_data(uploaded_ticker)
            else:
                st.error("Uploaded file missing required keys.")
        except Exception as e:
            st.error(f"Error processing uploaded file: {e}")


# === Display Company Snapshot ===
st.markdown("---")
st.markdown("## Company Overview", unsafe_allow_html=True)
st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

if selected_ticker:
    json_path = os.path.join(DATA_FOLDER, f"{selected_ticker}_financials.json")

    if os.path.exists(json_path):
        try:
            with open(json_path) as f:
                financials = json.load(f)

            overview = financials.get("overview", {})
            quote = financials.get("quote", {}).get("Global Quote", {})

            name = overview.get("Name", "N/A")
            exchange = overview.get("Exchange", "N/A")
            sector = overview.get("Sector", "N/A")

            symbol = quote.get("01. symbol", "N/A")
            open_price = quote.get("02. open", "N/A")
            high = quote.get("03. high", "N/A")
            low = quote.get("04. low", "N/A")
            current_price = quote.get("05. price", "N/A")
            volume = quote.get("06. volume", "N/A")
            trading_day = quote.get("07. latest trading day", "N/A")
            prev_close = quote.get("08. previous close", "N/A")
            change = quote.get("09. change", "N/A")
            change_percent = quote.get("10. change percent", "N/A")

            income = financials.get("income_statement", {}).get("annualReports", [{}])[0]
            balance = financials.get("balance_sheet", {}).get("annualReports", [{}])[0]

            revenue = income.get("totalRevenue", "N/A")
            net_income = income.get("netIncome", "N/A")
            shares = balance.get("commonStockSharesOutstanding", "N/A")

            # === Company Header and Chart Side-by-Side ===
            col_header, col_chart = st.columns([1, 1])

            with col_header:
                st.subheader(name)
                st.markdown(f"**Exchange:** {exchange} &nbsp;&nbsp; **Sector:** {sector} &nbsp;&nbsp; **Symbol:** {symbol}")
                st.metric("Trading Date", trading_day)

                col1, col2, col3 = st.columns(3)
                col1.metric("Price", f"${float(current_price):,.2f}" if current_price != "N/A" else "N/A")
                col2.metric("Previous Close", f"${float(prev_close):,.2f}" if prev_close != "N/A" else "N/A")
                col3.metric("Change (%)", f"{change} ({change_percent})" if change != "N/A" else "N/A")

                col4, col5, col6 = st.columns(3)
                col4.metric("Open", f"${float(open_price):,.2f}" if open_price != "N/A" else "N/A")
                col5.metric("High", f"${float(high):,.2f}" if high != "N/A" else "N/A")
                col6.metric("Low", f"${float(low):,.2f}" if low != "N/A" else "N/A")

                col7, col8, col9 = st.columns(3)
                col7.metric("Volume", f"{int(volume):,}" if volume != "N/A" else "N/A")
                col8.metric("Revenue (Latest)", f"${int(revenue):,}" if revenue != "N/A" else "N/A")
                col9.metric("Net Income (Latest)", f"${int(net_income):,}" if net_income != "N/A" else "N/A")

                col10, _, _ = st.columns([1, 0.5, 1])
                col10.metric("Shares Outstanding", f"{int(shares):,}" if shares != "N/A" else "N/A")

            with col_chart:
                display_chart(selected_ticker)


        except Exception as e:
            st.error(f"Error displaying overview: {e}")


# === Comparable Companies Overview ===
st.markdown("---")
st.markdown("## Comparable Company Overview", unsafe_allow_html=True)
st.markdown("<div style='margin-top: 55px;'></div>", unsafe_allow_html=True)

comp_path = os.path.join(DATA_FOLDER, f"{selected_ticker}_comparable_analysis.json")

if os.path.exists(comp_path):
    try:
        with open(comp_path, "r") as f:
            comparable_data = json.load(f)

        peers = comparable_data.get("peers", {})
        if not peers:
            st.warning("No peer data found in comparable analysis file.")
        else:
            for peer_symbol, peer_info in peers.items():
                col1, spacer, col2 = st.columns([1.6, 0.3, 3.8])

                with col1:
                    overview = peer_info.get("overview", {})
                    company_name = overview.get("companyName", peer_symbol)
                    image_url = overview.get("image", "")
                    info_symbol = peer_symbol
                    info_sector = overview.get("sector", "N/A")
                    info_industry = overview.get("industry", "N/A")

                    html_block = f"""
                        <div style="text-align: center; margin-bottom: 10px;">
                            <img src="{image_url}" style="width: 80px; margin-bottom: 10px;" />
                            <h4 style="margin-bottom: 5px;">{company_name}</h4>
                        </div>
                        <div style="display: flex; justify-content: center; gap: 40px;">
                            <div><strong>Symbol:</strong> {info_symbol}</div>
                            <div><strong>Sector:</strong> {info_sector}</div>
                            <div><strong>Industry:</strong> {info_industry}</div>
                        </div>
                    """
                    st.markdown(html_block, unsafe_allow_html=True)

                with col2:
                    metrics = peer_info.get("financial_metrics", {})
                    colA, colB, colC = st.columns(3)

                    colA.metric("Price per Share", f"${metrics.get('Price ($/share)', 0):,.2f}")
                    colB.metric("Market Cap", f"${metrics.get('Market Cap ($M)', 0)/1e9:,.2f}B")
                    colC.metric("EV", f"${metrics.get('Enterprise Value ($M)', 0)/1e9:,.2f}B")

                    colD, colE, colF = st.columns(3)
                    colD.metric("Revenue", f"${metrics.get('Sales ($M)', 0)/1e9:,.2f}B")
                    colE.metric("EBITDA", f"${metrics.get('EBITDA ($M)', 0)/1e9:,.2f}B")
                    colF.metric("Net Income", f"${metrics.get('Earnings ($M)', 0)/1e9:,.2f}B")

                st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
                st.markdown("---")

    except Exception as e:
        st.error(f"Error loading comparable analysis data: {e}")
