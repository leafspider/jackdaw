# Importing the yfinance package
import yfinance as yf
import json
# import pandas as pd


class YahooFinanceSearch:

    def __init__(s):
        pass

    def fetch_info(s, ticker_name):
        return yf.Ticker(ticker_name).info

    def fetch_history(s, ticker, start_date, end_date):
        return yf.download(ticker, start_date.isoformat(), end_date.isoformat())

    def fetch_csv(s, ticker, start_date, end_date):
        history = s.fetch_history(ticker, start_date, end_date)
        history["Date"] = history.index
        history = history[["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]]
        history.reset_index(drop=True, inplace=True)
        return history

    def fetch_dataframe(s, ticker, start_date, end_date):
        return s.fetch_csv(ticker, start_date, end_date)
        #return pd.DataFrame(csv)

    def fetch_close(s, ticker, start_date, end_date):
        history = s.fetch_csv(ticker, start_date, end_date)
        return history["Close"]

    def fetch_json(s, ticker, start_date, end_date):
        df = s.fetch_close(ticker, start_date, end_date)
        return df.to_json();


if __name__ == "__main__":

    fs = YahooFinanceSearch()

    ticker = "GOOG"
    start_date = "2024-04-01"
    end_date = "2024-05-01"

    #data = fs.fetch_info(ticker)
    #print(data)

    #data = fs.fetch_history(ticker, start_date, end_date)
    #print(data)

    #data = fs.fetch_csv(ticker, start_date, end_date)
    #print(data)

    from datetime import date

    start_date = date(2024, 4, 1)
    end_date = date(2024, 5, 1)
    data = fs.fetch_json(ticker, start_date, end_date)
    print(data)
