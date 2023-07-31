import pandas as pd
import yfinance as yf
import os
import sys
import contextlib
from io import StringIO
import shutil

ERROR_LOG_FILE = 'error_log.txt'

def fetch_market_data(tickers):
    '''
    Given a ticker/symbol list of active stocks on the NSE, fetch their price action and volume data since the beginning of time to data/{ticker}.csv
    Default parallelization uses threads = 2*num_cpu_cores. Sometimes fails because of the parallelization.
    :param tickers: The list of tickers/symbols to fetch data for
    :return: A list containing the names of the failed stock tickers
    '''
    failed_downloads=[]
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
    finally:
        return failed_downloads

def main():
    # Fetch the csv containing all the ticker names
    url = 'https://archives.nseindia.com/content/equities/EQUITY_L.csv'
    df = pd.read_csv(url)

    # Filter out rows with invalid tickers
    valid_tickers = df[(df['SYMBOL'].str.isalpha()) & (df[' SERIES'] == "EQ")]

    # Create the data folder, clean it if it already exists
    shutil.rmtree('data', ignore_errors=True)
    os.makedirs('data', exist_ok=True)
    if os.path.exists(ERROR_LOG_FILE):
        os.remove(ERROR_LOG_FILE)

    # Split the valid tickers into smaller chunks for parallel processing
    chunk_size = 8
    ticker_chunks = [valid_tickers[i:i+chunk_size] for i in range(0, len(valid_tickers), chunk_size)]

    # Fetch market data for each stock in chunks
    failed_jobs = []
    for batch in ticker_chunks:
        tickers = [row['SYMBOL'].strip() for _, row in batch.iterrows()]
        failed_jobs += fetch_market_data(tickers)

    # Try solo downloading the failed batches
    fatal_failures = []
    for ticker in failed_jobs:
        fatal_failures += fetch_market_data(ticker)

    # Log fatal failures
    if fatal_failures:
            with open(ERROR_LOG_FILE, 'a') as error_file:
                for ticker in fatal_failures:
                    error_file.write(f"Failed to download market data for {ticker}\n")

if __name__ == '__main__':
    main()
