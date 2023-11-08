import json
import requests
from credentials import *
import csv
import time
from datetime import datetime

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
    with open('./S&P500Tickers.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        symbols = [row[0] for row in csvreader]
        
        with open(f'./stockdata.csv', 'w', newline='') as csvfile:
            fieldnames = ["symbol", "timestamp", "open", "high", "low", "close", "volume"]
            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csvwriter.writeheader()  # Write the header only once
            
            for i in range(0, len(symbols), symbols_per_request):
                symbols_batch = symbols[i:i+symbols_per_request]
                
                for symbol in symbols_batch:
                    params["symbol"] = symbol
                    print("Getting symbol " + symbol)
                    response = requests.get(base_url, params=params)
                    res = response.json()
                    status_code = res.get("status")
                    print("Status code " + str(status_code))
                    if status_code != "error":
                        res = response.json()
                        values = res.get("values", [])
                        for entry in values:
                            csvwriter.writerow({
                                "symbol": symbol,
                                "timestamp": datetime.strptime(entry["datetime"], '%Y-%m-%d').strftime('%Y-%m-%d'),
                                "open": float(entry["open"]),
                                "high": float(entry["high"]),
                                "low": float(entry["low"]),
                                "close": float(entry["close"]),
                                "volume": int(entry["volume"])
                            })
                        print("Done")
                    else:
                        print("Waiting")
                        time.sleep(delay)
                        print("Waiting End!")
                        response = requests.get(base_url, params=params)
                        res = response.json()
                        values = res.get("values", [])
                        for entry in values:
                            csvwriter.writerow({
                                "symbol": symbol,
                                "timestamp": datetime.strptime(entry["datetime"], '%Y-%m-%d').strftime('%Y-%m-%d'),
                                "open": float(entry["open"]),
                                "high": float(entry["high"]),
                                "low": float(entry["low"]),
                                "close": float(entry["close"]),
                                "volume": int(entry["volume"])
                            })
                        print("Done")
                
                if i + symbols_per_request < len(symbols):
                    print("Done , waiting")
                    # Delay before making the next request
                    time.sleep(delay)
                    print("Waiting End!")
    print("Done All")
    return data

get_data()
