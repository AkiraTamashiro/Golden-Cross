import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
st.write('Group 1 Project')
st.header("Golden/ Death Cross")

# Define stock categories based on risk tolerance
low_risk_stocks = ['JNJ', 'PG', 'KO', 'WM', 'AEP', 'MCD', 'DUK', 'T', 'PFE', 'MSFT', 'SBUX', 'TXN', 'SNOW']
medium_risk_stocks = ['NKE', 'MMM', 'CURLF', 'LUMN', 'RYAAY', 'ABNB']
high_risk_stocks = ['TSLA', 'SQ', 'SHOP', 'ROKU', 'NVDA']

# Define stock categories dictionary
risk_categories = {
    "Low": low_risk_stocks,
    "Medium": medium_risk_stocks,
    "High": high_risk_stocks
}

# Function to plot golden and death crosses
def plot_crosses(stock_symbol):
    # Download historical data for the selected stock
    data = yf.download(stock_symbol, period="1y")
    
    # Calculate 50-day and 200-day moving averages
    data['50_MA'] = data['Close'].rolling(window=50).mean()
    data['200_MA'] = data['Close'].rolling(window=200).mean()
    
    # Find golden cross and death cross points
    golden_cross = data[(data['50_MA'] > data['200_MA']) & (data['50_MA'].shift(1) <= data['200_MA'].shift(1))]
    death_cross = data[(data['50_MA'] < data['200_MA']) & (data['50_MA'].shift(1) >= data['200_MA'].shift(1))]
    
    # Plot the data
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label=f'{stock_symbol} Close Price', color='black')
    plt.plot(data['50_MA'], label='50-Day Moving Average', color='blue')
    plt.plot(data['200_MA'], label='200-Day Moving Average', color='red')
    plt.scatter(golden_cross.index, golden_cross['50_MA'], color='green', marker='^', label='Golden Cross', s=100)
    plt.scatter(death_cross.index, death_cross['50_MA'], color='red', marker='v', label='Death Cross', s=100)
    
    plt.title(f'{stock_symbol} Golden and Death Crosses')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    
    # Display plot in Streamlit
    st.pyplot(plt)

# Streamlit app layout
st.title("Golden and Death Crosses for Stocks")
st.write("Select a risk tolerance level to view the golden and death crosses of stocks.")

# Select risk tolerance
risk_tolerance = st.selectbox("Choose Risk Tolerance:", ["Low", "Medium", "High"])

# Select a stock within the chosen risk tolerance
selected_stock = st.selectbox("Choose a Stock:", risk_categories[risk_tolerance])

# Display golden and death crosses plot for the selected stock
if st.button("Show Golden and Death Crosses"):
    plot_crosses(selected_stock)
