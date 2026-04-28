# Stock Predictor Telegram Bot

## What it does
A Telegram bot that provides real-time stock prices and predicts future prices using machine learning.

## Features
- `/price SYMBOL` - Get current stock price
- `/predict SYMBOL` - Get 7-day price prediction with chart
- Real-time data from Yahoo Finance
- Machine learning predictions with visual charts

## How to Run
1. Install requirements: `pip install python-telegram-bot yfinance matplotlib scikit-learn pandas`
2. Run: `python prediction_bot.py`
3. Open Telegram and search for @MaxStockPredictorBot

## Technologies Used
- Python
- python-telegram-bot (Telegram API)
- yfinance (Stock data)
- scikit-learn (Machine learning)
- matplotlib (Charts)

## Example Usage
- `/price AAPL` - Shows Apple's current price
- `/predict TSLA` - Shows Tesla prediction with chart