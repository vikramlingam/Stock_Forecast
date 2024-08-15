# Before you start with the code, make sure you have these libraries installed. Use pip install streamlit prophet yfinance plotly
import streamlit as st
from datetime import date
import os

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Set the background colors using more specific CSS selectors. in this case I am trying to use cream colour background.
st.markdown(
    """
    <style>
    /* Main content background color */
    .css-1d391kg, .css-1gk3kc2 {
        background-color: #d3d3d3;  /* Light grey */
    }
    /* Sidebar background color */
    .css-1d391kg .css-1gk3kc2 .css-1rqq5ki {
        background-color: #f5f5dc;  /* Cream */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Indian Stock Forecast App')

# Author Information
st.write("**Author:** Vikram Lingam")
st.write("[**GitHub:** https://github.com/vikramlingam](https://github.com/vikramlingam)")
st.write("[**LinkedIn:** https://www.linkedin.com/in/vikramlingam/](https://www.linkedin.com/in/vikramlingam/)")

# Define NIFTY 50 stock tickers, you can add more stocks to this list in the following format
nifty_50_stocks = {
    'Reliance Industries': 'RELIANCE.NS',
    'Tata Consultancy Services': 'TCS.NS',
    'Infosys': 'INFY.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'ICICI Bank': 'ICICIBANK.NS',
    'Hindustan Unilever': 'HINDUNILVR.NS',
    'State Bank of India': 'SBIN.NS',
    'Bharti Airtel': 'BHARTIARTL.NS',
    'Kotak Mahindra Bank': 'KOTAKBANK.NS',
    'Bajaj Finance': 'BAJFINANCE.NS',
    'HDFC': 'HDFC.NS',
    'Larsen & Toubro': 'LT.NS',
    'Axis Bank': 'AXISBANK.NS',
    'ITC': 'ITC.NS',
    'Asian Paints': 'ASIANPAINT.NS',
    'Maruti Suzuki': 'MARUTI.NS',
    'Wipro': 'WIPRO.NS',
    'Mahindra & Mahindra': 'M&M.NS',
    'Nestle India': 'NESTLEIND.NS',
    'Sun Pharmaceutical Industries': 'SUNPHARMA.NS',
    'UltraTech Cement': 'ULTRACEMCO.NS',
    'Tata Steel': 'TATASTEEL.NS',
    'Tech Mahindra': 'TECHM.NS',
    'HCL Technologies': 'HCLTECH.NS',
    'Adani Enterprises': 'ADANIENT.NS',
    'Bajaj Auto': 'BAJAJ-AUTO.NS',
    'Titan Company': 'TITAN.NS',
    'Tata Motors': 'TATAMOTORS.NS',
    'Divis Laboratories': 'DIVISLAB.NS',
    'Power Grid Corporation of India': 'POWERGRID.NS',
    'Cipla': 'CIPLA.NS',
    'Grasim Industries': 'GRASIM.NS',
    'JSW Steel': 'JSWSTEEL.NS',
    'Hero MotoCorp': 'HEROMOTOCO.NS',
    'IndusInd Bank': 'INDUSINDBK.NS',
    'Dr. Reddys Laboratories': 'DRREDDY.NS',
    'Bharat Petroleum Corporation': 'BPCL.NS',
    'Hindalco Industries': 'HINDALCO.NS',
    'Britannia Industries': 'BRITANNIA.NS',
    'Apollo Hospitals': 'APOLLOHOSP.NS',
    'Eicher Motors': 'EICHERMOT.NS',
    'Adani Ports and SEZ': 'ADANIPORTS.NS',
    'Oil and Natural Gas Corporation': 'ONGC.NS',
    'SBI Life Insurance': 'SBILIFE.NS',
    'Tata Consumer Products': 'TATACONSUM.NS',
    'Bajaj Finserv': 'BAJAJFINSV.NS',
    'UPL': 'UPL.NS',
    'Coal India': 'COALINDIA.NS',
    'NTPC': 'NTPC.NS',
    'HDFC Life Insurance': 'HDFCLIFE.NS'
}

# Add a sidebar for NIFTY 50 stock selection
selected_stock = st.sidebar.selectbox(
    'Select a NIFTY 50 stock for prediction', 
    list(nifty_50_stocks.keys())
)

ticker = nifty_50_stocks[selected_stock]

# Load and display the stock summary
def get_stock_summary(ticker):
    stock_info = yf.Ticker(ticker).info
    summary = stock_info.get('longBusinessSummary', 'No summary available.')
    return summary

stock_summary = get_stock_summary(ticker)

st.sidebar.subheader(f'Summary of {selected_stock}')
st.sidebar.write(stock_summary)

# Load logo from the local directory
logo_path = os.path.join("logos", f"{ticker}.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_column_width=True)
else:
    st.sidebar.text("")

n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

# Display company logo or fallback message in the main interface
data_load_state = st.text('Loading data...')
data = load_data(ticker)
data_load_state.text('Data loaded successfully!')

if os.path.exists(logo_path):
    st.image(logo_path, use_column_width=True)
else:
    st.text("")

st.subheader(f'Raw data for {selected_stock}')
st.write(data.tail())

# Plot raw data with specified colors
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open", line=dict(color='red')))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close", line=dict(color='green')))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Predict forecast with Prophet
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Customize the forecast plot colors
def plot_forecast(m, forecast):
    fig = plot_plotly(m, forecast)
    for trace in fig['data']:
        trace['line']['color'] = 'yellow'  # Set forecast line color to yellow
    st.plotly_chart(fig)

st.subheader('Forecast data')
st.write(forecast.tail())
    
st.write(f'Forecast plot for {n_years} years')
plot_forecast(m, forecast)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)

# Add a detailed note on the forecast model and its limitations
st.subheader("Important Note")
st.write("""
**This forecast model is based on Time Series Models. These Models are statistical methods used to analyze and forecast data points collected over time. These models, such as ARIMA, Exponential Smoothing, and Prophet, rely heavily on historical data to predict future values. Additive Models in time series analysis assume that the components (trend, seasonality, and noise) are linearly combined to form the observed data.**

**Limitations in Predicting Stock Market Prices:**

**Complexity of Market Dynamics:**
The stock market is influenced by a vast array of factors, including economic indicators, interest rates, company earnings, geopolitical events, investor sentiment, and more. These factors interact in complex, often non-linear ways, making it challenging for models like Prophet to capture the full scope of influences on stock prices.

**Assumption of Linearity:**
Additive models assume a linear relationship between components, which may oversimplify the actual behavior of stock prices. Stock markets often exhibit non-linear characteristics, with abrupt changes, volatility, and events that are difficult to predict using linear models.

**Over-reliance on Historical Data:**
Time series models, including Prophet, are heavily dependent on historical data. While history can provide some insights, it may not always accurately predict future movements, especially in a market influenced by new information and sudden events that disrupt historical patterns.

**Ignoring External Factors:**
Time series models typically focus on past prices and trends without accounting for external, fundamental factors such as changes in company management, innovations, regulatory changes, and macroeconomic shifts. These factors can have a significant impact on stock prices and are not captured by time series analysis.

**Market Efficiency:**
The Efficient Market Hypothesis (EMH) suggests that stock prices reflect all available information. If markets are efficient, the historical data used in time series models should already incorporate all known information, limiting the ability of these models to predict future prices accurately.

**Why One Should Not Rely Solely on Forecast Models:**

While time series models like Prophet can provide useful insights, relying solely on these models for predicting stock prices is risky. Stock prices are influenced by a combination of technical and fundamental factors. Fundamental analysis—which includes evaluating a company's financial health, competitive position, and industry trends—provides a more comprehensive view of a stock's potential future performance.

Moreover, stock markets are subject to sudden and unpredictable events, such as political changes, economic crises, or company-specific news, which time series models cannot anticipate. Therefore, a balanced approach, combining time series analysis with fundamental analysis, is essential for making informed investment decisions. This approach helps mitigate the risks associated with relying solely on any single forecasting method.
""")
