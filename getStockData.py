import json
import requests
from credentials import *
import csv
import time

def get_data():
    data = []
    params = {
        "interval": "1day",
        "outputsize": "5000",
        "apikey": "d31cae03b5c7431f886c073e6e0317da"
    }
    base_url = "https://api.twelvedata.com/time_series"
    symbols_per_request = 8  # Number of symbols to process in each iteration
    delay = 60  # Delay in seconds between requests
    with open('./GR1/S&P500Tickers.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        symbols = [row[0] for row in csvreader]
        
        for i in range(0, len(symbols), symbols_per_request):
            symbols_batch = symbols[i:i+symbols_per_request]
            
            for symbol in symbols_batch:
                params["symbol"] = symbol
                
                response = requests.get(base_url, params=params)
                if response.status_code == 200:
                    res = response.json()
                    meta = res.get("meta", {})
                    values = res.get("values", [])
                    new_data = {
                        "meta": meta,
                        "values": values
                    }
                    data.append(new_data)
                    print(new_data)
            
            if i + symbols_per_request < len(symbols):
                # Delay before making the next request
                time.sleep(delay)
    return data