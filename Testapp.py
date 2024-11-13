#Web App
import yfinance as yf
import plotly.graph_objects as go
import streamlit as st

# Set up Streamlit page configuration
st.set_page_config(page_title="Golden and Death Crosses", layout="wide")

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

# Function to plot golden and death crosses using Plotly
def plot_crosses(stock_symbol):
    # Download historical data for the selected stock (last 5 years)
    data = yf.download(stock_symbol, period="3y")
    
    # Calculate 50-day and 200-day moving averages
    data['50_MA'] = data['Close'].rolling(window=50).mean()
    data['200_MA'] = data['Close'].rolling(window=200).mean()
    
    # Find golden cross and death cross points
    golden_cross = data[(data['50_MA'] > data['200_MA']) & (data['50_MA'].shift(1) <= data['200_MA'].shift(1))]
    death_cross = data[(data['50_MA'] < data['200_MA']) & (data['50_MA'].shift(1) >= data['200_MA'].shift(1))]
    
    # Create a Plotly figure
    fig = go.Figure()

    # Add close price trace
    fig.add_trace(go.Scatter(
        x=data.index, y=data['Close'], mode='lines', name='Close Price', line=dict(color='black')
    ))

    # Add 50-day moving average trace
    fig.add_trace(go.Scatter(
        x=data.index, y=data['50_MA'], mode='lines', name='50-Day MA', line=dict(color='blue')
    ))

    # Add 200-day moving average trace
    fig.add_trace(go.Scatter(
        x=data.index, y=data['200_MA'], mode='lines', name='200-Day MA', line=dict(color='red')
    ))

    # Mark golden crosses with green dots
    fig.add_trace(go.Scatter(
        x=golden_cross.index, y=golden_cross['50_MA'], mode='markers', name='Golden Cross',
        marker=dict(color='green', size=8)
    ))

    # Mark death crosses with red dots
    fig.add_trace(go.Scatter(
        x=death_cross.index, y=death_cross['50_MA'], mode='markers', name='Death Cross',
        marker=dict(color='red', size=8)
    ))

    # Customize layout to enable panning, zooming, and using range slider
    fig.update_layout(
        title=f'{stock_symbol} Golden and Death Crosses',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider=dict(visible=True),  # Adds a range slider for panning
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    # Display Plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Streamlit app layout
st.title("Golden and Death Crosses for Stocks")
st.write("Select a risk tolerance level to view the golden and death crosses of stocks with mouse-enabled interactivity.")

# Select risk tolerance
risk_tolerance = st.selectbox("Choose Risk Tolerance:", ["Low", "Medium", "High"])

# Select a stock within the chosen risk tolerance
selected_stock = st.selectbox("Choose a Stock:", risk_categories[risk_tolerance])

# Display golden and death crosses plot for the selected stock
if st.button("Show Golden and Death Crosses"):
    plot_crosses(selected_stock)
