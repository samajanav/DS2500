import requests 


API_KEY = "JHPY0JKT69A6MHSU"

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=API_KEY'
r = requests.get(url)
data = r.json()

print(data)