import pandas as pd
import yfinance as yf
import os
import sys
import contextlib
from io import StringIO
import shutil

def fetch_market_data(tickers):
    '''
    Given a ticker/symbol list of active stocks on the NSE, fetch their price action and volume data since the beginning of time to data/{ticker}.csv
    Default parallelization uses threads = 2*num_cpu_cores
    :param tickers: The list of tickers/symbols to fetch data for
    '''
    failed_downloads = []
    try:
        # Annoying detail, yf does not throw an error on failure. Just outputs to stdout. 
        # Fix: Mute its output and raise an error ourselves
        output_buffer = StringIO()
        with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(output_buffer):
            data = yf.download(tickers, period='max', group_by='ticker', prepost=True, actions=True, keepna=False)
            retry_list = [ticker + ".NS" for ticker in tickers if data[ticker].empty]
            retry_data = yf.download(retry_list, period='max', group_by='ticker', prepost=True, actions=True, keepna=False)

        # Store retrieved data to files / log errors
        for ticker in tickers:
            file_name = f'data/{ticker}.csv'
            stock_data = data[ticker] if not data[ticker].empty else retry_data[ticker + ".NS"]
            stock_data = stock_data.dropna(subset=stock_data.columns.difference(['Date']), how='all')
            if stock_data.empty:
                failed_downloads.append(ticker)
            else:
                stock_data.to_csv(file_name)
                print(f'Downloaded market data for {ticker} and saved to {file_name}')
    except Exception as e:
        failed_downloads += tickers
        
    # Log errors to an error log
    if failed_downloads:
        with open('error_log.txt', 'a') as error_file:
            for ticker in failed_downloads:
                error_file.write(f"Failed to download market data for {ticker}\n")

def main():
    # Fetch the csv containing all the ticker names
    url = 'https://archives.nseindia.com/content/equities/EQUITY_L.csv'
    df = pd.read_csv(url)

    # Filter out rows with invalid tickers
    valid_tickers = df[(df['SYMBOL'].str.isalpha()) & (df[' SERIES'] == "EQ")]

    # Create the data folder, clean it if it already exists
    shutil.rmtree('data', ignore_errors=True)
    os.makedirs('data', exist_ok=True)

    # Split the valid tickers into smaller chunks for parallel processing
    chunk_size = 200
    ticker_chunks = [valid_tickers[i:i+chunk_size] for i in range(0, len(valid_tickers), chunk_size)]

    # Fetch market data for each stock
    for batch in ticker_chunks:
        tickers = [row['SYMBOL'].strip() for _, row in batch.iterrows()]
        fetch_market_data(tickers)

if __name__ == '__main__':
    main()
