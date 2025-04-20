import os
import pandas as pd
import streamlit as st
import altair as alt

DATA_FOLDER = "data"

def display_chart(ticker):
    ohlc_path = os.path.join(DATA_FOLDER, f"{ticker}_chart.json")

    if os.path.exists(ohlc_path):
        try:
            ohlc_df = pd.read_json(ohlc_path)
            ohlc_df.columns = [col[0] if isinstance(col, tuple) else col for col in ohlc_df.columns]
            ohlc_df.rename(columns={"('Date', '')": "Date"}, inplace=True)
            ohlc_df["Date"] = pd.to_datetime(ohlc_df["Date"])

            metrics_to_plot = st.multiselect(
                "Metrics", ["Open", "High", "Low", "Close"],
                default=["Close", "High", "Low", "Open"],
                label_visibility="collapsed"
            )

            if metrics_to_plot:
                melted_df = ohlc_df.melt(
                    id_vars="Date", 
                    value_vars=metrics_to_plot, 
                    var_name="Metric", 
                    value_name="Price"
                )

                chart = alt.Chart(melted_df).mark_line().encode(
                    x=alt.X("Date:T", title="Date"),
                    y=alt.Y("Price:Q", title="Price"),
                    color=alt.Color("Metric:N", scale=alt.Scale(scheme="dark2")),
                    tooltip=["Date:T", "Metric:N", "Price:Q"]
                ).properties(
                    width="container",
                    height=500,
                    background="black"
                ).interactive()

                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Please select at least one metric to plot.")

        except Exception as e:
            st.error(f"Error reading OHLC chart data: {e}")
    else:
        st.info(f"No chart data found for {ticker}. Please generate {ticker}_chart.json.")
