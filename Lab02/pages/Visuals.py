# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import plotly.express as px

with open("data.json") as f:
    data = json.load(f)

df = pd.DataFrame(data["data_points"])
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")




# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
st.subheader("Stock Prices of Top Tech/AI Stocks as of 10/10/2026")
latest = df[df["year"] == "2026 YTD"].set_index("ticker")["price"]
st.bar_chart(latest)

prices = df.pivot(index="ticker", columns="year", values="price")
first_price = prices.bfill(axis=1).iloc[:, 0]   # first available price (handles Sandisk's missing 2024)
change = round((prices["2026 YTD"] / first_price - 1) * 100,2)
st.subheader("Price Change from Jan 1, 2025 to 2026 YTD (%)")
st.bar_chart(change)
st.subheader("Details:")
st.write("As seen in the bar chart, the leading stock performer from Jan 1, 2025 to 2026 YTD is Sandisk, with a YTD return 1133.07%. This is due to hyperscale data centers needing massive amounts of high-capacity enterprise solid-state drives (SSDs) and flash memory for AI model training and data storage, which is what Micron produces")
st.write("Microsoft lagged despite its YTD return of 45%. This is due to massive capital expenditures(as high as 190 billion), and high reliance on OpenAI, which just announced a revenue that was $20 billion short of expected revenue.")


st.subheader("Compare Cumulative Stock Prices Over Time")

tickers = sorted(df["ticker"].unique())

# Set the default selection once
if "selected_tickers" not in st.session_state:
    st.session_state.selected_tickers = tickers[:3]

# The key links the widget to session state, so the choice persists across reruns
st.multiselect("Choose stocks to compare:", tickers, key="selected_tickers")

filtered = df[df["ticker"].isin(st.session_state.selected_tickers)]

if filtered.empty:
    st.info("Pick at least one stock to see the chart.")
else:
    fig = px.line(
        filtered,
        x="year",
        y="price",
        color="ticker",
        markers=True,
        title="Stock Price by Period",
        labels = {"year": "Period", "price": "Stock Price (USD)", "ticker": "Ticker"}
    )
    fig.update_xaxes(type="category")  # show whole years only
    st.plotly_chart(fig)




# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
