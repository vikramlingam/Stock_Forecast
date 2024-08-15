# Indian Stock Forecast App

**Author:** Vikram Lingam  
**GitHub:** [https://github.com/vikramlingam](https://github.com/vikramlingam)  
**LinkedIn:** [https://www.linkedin.com/in/vikramlingam/](https://www.linkedin.com/in/vikramlingam/)
**Streamlit App** https://stockforecast-vik.streamlit.app/

## Context
The Indian Stock Forecast App is an application developed to predict the future stock price of NIFTY 50 companies, based on the Prophet time series model. An app that allows one to choose any stock out of the NIFTY 50 index, get a brief about the company, and generate a forecast of up to 4 years.

This project uses the following technologies:

-Streamlit to develop the interactive web application.
-Prophet for time series forecasting.
-yfinance, which retrieves historical stock data.

## Features
**Stock Selection**: Selecting companies from NIFTY 50 listed companies, predict the future stock prices. You can modify the code to include more stocks that you wish to forecast.

**Company Summary and Logo**: Overview and logo of selected company.

**Interactive Forecasting**: Develop and visualize 4-year forecasts using the Prophet model.

**User Definable Graphs**: The graphs on the app have a customized color scheme to improve the visibility of the data points – mainly red, green, and yellow.

**User-Friendly Interface**: It is light grey in the background and a sidebar in cream colour, which makes it beautiful.

## How to Use
**Choose a Stock**: From the left bar select a Stock from the NIFTY 50.

**Summary Viewing**: The sidebar will provide a short summary, along with the company logo, related to the selected company.

**Setting Forecast Period**: Use the slider to select the number of years to be forecast to any values ranging from one to four.

**Generate Forecast**: App will visualize raw historical data and forecasted stock prices and its components.

**Important Note**: The app will also have an elaborate note on the limitations of the model and why it should not be the only basis for investment decisions.

## Installation
-To run this app locally do the following:

Clone the repository: git clone https://github.com/vikramlingam/indian-stock-forecast-app.git
