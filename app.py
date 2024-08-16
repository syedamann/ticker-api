import streamlit as st
import requests
import pandas as pd

# List of ticker symbols
TICKERS = ['AEE', 'REZ', '1AE', '1MC', 'NRZ']

# Function to fetch and parse announcements
def fetch_announcements(ticker):
    url = f"https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error(f"Error parsing JSON for {ticker}")
            return None
    else:
        st.error(f"Failed to fetch data for {ticker}: {response.status_code}")
        return None

# Function to check for "Trading Halt" announcements
def check_trading_halt(announcements):
    return any("trading halt" in announcement['header'].lower() for announcement in announcements)

# Streamlit App Layout
st.title("ASX Announcements Viewer")

# Sidebar for ticker selection
selected_ticker = st.sidebar.selectbox("Select a ticker symbol", TICKERS)

# Fetch announcements for the selected ticker
data = fetch_announcements(selected_ticker)

if data:
    # Display the announcements
    st.subheader(f"Announcements for {selected_ticker}")
    
    df = pd.DataFrame(data['data'])
    if not df.empty:
        st.dataframe(df[['document_release_date', 'header', 'url']])
    else:
        st.write("No announcements available.")

    # Check for "Trading Halt" in announcements
    if check_trading_halt(data['data']):
        st.warning("Trading Halt announcement detected!")
else:
    st.write("No data available for the selected ticker.")


# Function to fetch and parse announcements
def fetch_all_announcements():
    results = {}
    for ticker in TICKERS:
        data = fetch_announcements(ticker)
        if data:
            results[ticker] = data['data']
    return results

# Fetch announcements for all tickers
all_announcements = fetch_all_announcements()

# Display ticker with "Trading Halt"
st.subheader("Tickers with Trading Halt Announcements")
halted_tickers = [ticker for ticker, announcements in all_announcements.items() if check_trading_halt(announcements)]
if halted_tickers:
    st.write(", ".join(halted_tickers))
else:
    st.write("No Trading Halt announcements detected.")
