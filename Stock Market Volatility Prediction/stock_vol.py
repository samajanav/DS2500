"""
Predicting Stock Volatility
DS2500
Fall 2023

Janav Sama and Raymond Liu (Team 71)

"""

# Importing the necessary libraries 

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import yfinance as yf
from arch import arch_model
import matplotlib.pyplot as plt


def plot_data(data, title, x_label, y_label):
    
    """
    The plot_data function generates a plot for the given data 
    with specified title, x-axis label, and y-axis label.
    
    """
    plt.plot(data)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def main():
    
    """Extracting and Reading Data"""
    
    stock_symbol = input(str("What stock's volatility would you like to find out?\
                        Please enter the stock symbol:"))
    start_date = "2010-01-01"
    end_date = "2023-10-31"
    
    # Fetch stock data using yfinance
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    
    # Load the data from the CSV file
    csv_data = pd.read_csv('Data.csv')
        
    csv_data['Date'] = pd.to_datetime(csv_data['Date'])
    stock_data.index = pd.to_datetime(stock_data.index)
    
    # Merge stock data with CSV data on the 'Date' column
    merged_data = pd.merge(csv_data, stock_data['Close'], how='inner',
                           left_on='Date', right_index=True)
    
    
    """Finding out volatility using Standard Deviation"""
    
    # Extract features and target
    features = merged_data[['Unemployment Rate', 'Interest Rate']]
    target = merged_data['Close']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features,
                                        target, test_size=0.2, random_state=0)
    
    # Create a linear regression model
    model = LinearRegression()
    
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    
    # Calculate predicted volatility
    predicted_volatility = round(np.std(predictions),2)
    
    print("Predicted Volatility (using Standard Deviation):", 
          predicted_volatility)
    
    
    """Finding out volatility using GARCH Model"""
    
    # GARCH model
    garch_model = arch_model(target, vol='Garch', p=1, q=1)
    garch_result = garch_model.fit(disp='off')
    
    # Forecast volatility
    garch_forecast = garch_result.forecast()
    
    # Extract the forecasted volatility
    forecasted_volatility = round(np.sqrt(garch_forecast.variance.iloc[-1, :])
                                  ,2)
    print("Predicted Volatility (using GARCH model):",
          forecasted_volatility.values[0])
    
    
    """PLots and Graphs"""
    
    # Unemployment Rate graph
    unemployment_data = csv_data["Unemployment Rate"]
    plot_data(unemployment_data, "Unemployment Rates in the US from 2010 to 2023",
              "Unemployment Rate (in %)", "Year")
    
    # Interest Rate graph
    interest_data = csv_data["Interest Rate"]
    plot_data(interest_data, "Interest Rates in the US from 2010 to 2023",
              "Interest Rate (in %)", "Year")
    
    
    # Residual Plot for Linear Regression
    plt.figure(figsize=(8, 5))
    residuals = y_test - predictions
    plt.scatter(X_test.index, residuals)
    plt.axhline(y=0, color='r', linestyle='--', label='Zero Residuals')
    plot_data(residuals, 'Residual Plot for Linear Regression', 'Date', 
              'Residuals')
    
    # GARCH Actual vs Forecasted Volatility
    plt.figure(figsize=(12, 6))
    plt.plot(merged_data.index, np.sqrt(garch_result.conditional_volatility), 
             label='Actual Volatility', color='blue')
    plt.plot(garch_forecast.variance.index, forecasted_volatility.values, 
             label='Forecasted Volatility', linestyle='dashed', color='red')
    plot_data(np.sqrt(garch_result.conditional_volatility),
              'Actual vs Forecasted Volatility (GARCH Model)',
              'Date', 'Volatility')
    
    # GARCH Residual Plot
    plot_data(garch_result.resid, 'Residual Plot for GARCH Model', 'Time',
              'Residuals')
    
if __name__ == "__main__":
    main()

