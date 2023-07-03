import pandas as pd

# Read the data from html link
wiki_data=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies') # Open the link and download S&P company details in a table

# All data is stored in first cell
data = wiki_data[0] 
print(data.head())

# Sort the dataframe on ticker in alphabetical ascending order
sorted_data = data.sort_values(by=['Symbol'], ascending=True) 

# Convert the dataframe to csv file
# Index is False as we don't want to write index in csv file
sorted_data.to_csv('S&P500Tickers.csv', mode='w', index=False) 