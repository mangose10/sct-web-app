from binance.client import Client
import json, sys

API_KEY = "8rKrbQ8GpcicyQbGpxF96ihVbsUixobf3SAgprCskLIi5wv0l3RJAUGxA0DvW0U7"
API_SECRET = "qGzMO4K4CTnz8jRaaCqDEl263topFa1qwpPzMdrzP1m6YeaeukS1oRaMUL5ga6ae"


client = Client(api_key=API_KEY, api_secret=API_SECRET, tld="us")

#print("here" + str(sys.argv))
k = str(sys.argv[1])

intervalDict = {
  '1m' : {
    'interval' : Client.KLINE_INTERVAL_1MINUTE,
    'startT' : "2 hour ago UTC"
  },
  '5m' : {
    'interval' : Client.KLINE_INTERVAL_5MINUTE,
    'startT' : "10 hours ago UTC"
  },
  '30m' : {
    'interval' : Client.KLINE_INTERVAL_30MINUTE,
    'startT' : "60 hours ago UTC"
  },
  '1h' : {
    'interval' : Client.KLINE_INTERVAL_1HOUR,
    'startT' : "120 hours ago UTC"
  }
}

candles = client.get_historical_klines(symbol='BTCUSD', interval=intervalDict[k]['interval'], start_str=intervalDict[k]['startT'])

#info = client.get_account()
#print(info)
#  [
#      [
#          1499040000000,      # Open time
#          "0.01634790",       # Open
#          "0.80000000",       # High
#          "0.01575800",       # Low
#          "0.01577100",       # Close
#          "148976.11427815",  # Volume
#          1499644799999,      # Close time
#          "2434.19055334",    # Quote asset volume
#          308,                # Number of trades
#          "1756.87402397",    # Taker buy base asset volume
#          "28.46694368",      # Taker buy quote asset volume
#          "17928899.62484339" # Can be ignored
#      ]
#  ]
# {"k":{"t":1615600080000,"T":1615600139999,"o":"56233.59000000","c":"56246.64000000","h":"56249.64000000","l":"56169.81000000"}}

def candleToJSON(data):
  
  arr = []
  i = 0

  mins = 9999999999.0
  maxs = 0.0

  for d in range(len(data)):
    obk = {
      't' : data[d][0],
      'o' : data[d][1],
      'h': data[d][2],
      'l': data[d][3],
      'c': data[d][4],
      'T': data[d][6]
    }
    check = [mins, float(obk['l'])]
    mins = min(check)

    check = [maxs, float(obk['h'])]
    maxs = max(check)
    arr.append(obk)
    #print(d)

  obj = {
    'klinedata':arr,
    'min':mins,
    'max':maxs
  }
  return obj

canObj = candleToJSON(candles)
print(json.dumps(canObj))
#mongoc = pymongo.MongoClient("mongodb://leo:Melmmldm1%21@localhost:27017/?authSource=admin&readPreference=secondary&appname=MongoDB%20Compass&ssl=false")
#mongoc.SCT.candles.insert_one({'h1':canObj})

