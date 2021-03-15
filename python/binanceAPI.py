from binance.client import Client
from binance.enums import *
import time, json, pymongo, pprint
import tconfig

import numpy
import talib
from talib import MA_Type

#upper, middle, lower = talib.BBANDS( matype=MA_Type.T3)

#key = "8rKrbQ8GpcicyQbGpxF96ihVbsUixobf3SAgprCskLIi5wv0l3RJAUGxA0DvW0U7"
#secret = "qGzMO4K4CTnz8jRaaCqDEl263topFa1qwpPzMdrzP1m6YeaeukS1oRaMUL5ga6ae"
#client = Client(api_key=key, api_secret=secret, tld="us")

client = Client(api_key=tconfig.API_KEY, api_secret=tconfig.API_SECRET, tld="us")
client.API_URL = 'https://testnet.binance.vision/api'


#candles = client.get_historical_klines(symbol='BTCUSD', interval=Client.KLINE_INTERVAL_1HOUR, start_str="60 hour ago UTC")
'''
testOrder = client.create_test_order(
    symbol='BTCUSD',
    side=SIDE_BUY,
    type=ORDER_TYPE_MARKET,
    quantity=1)
'''
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(client.get_account())

testOrder = client.order_market_buy(
    symbol='BTCBUSD',
    quantity=0.001)
print(testOrder)

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

def candleToJSON(data):
  
  obj = []
  i = 0
  #print(len(data))
  for d in range(len(data)):
    obk = {
      'oTime' : data[d][0],
      'oPrice' : data[d][1],
      'high': data[d][2],
      'low': data[d][3],
      'cPrice': data[d][4],
      'volume': data[d][5],
      'cTime': data[d][6],
      'quoteVolume': data[d][7],
      'numTrades': data[d][8],
      'takerBaseVolume': data[d][9],
      'takerQuoteVolume': data[d][10]
    }
    obj.append(obk)
    #print(d)

  return obj
'''
canObj = candleToJSON(candles)
print(canObj)
mongoc = pymongo.MongoClient("mongodb+srv://crespi:Simple1234@sctdb.v1k99.mongodb.net/test")
mongoc.SCT.candles.insert_one({'h1':canObj})
'''
#with open("candle.json", "w") as outfile:  
#    json.dump(candleToJSON(candles), outfile)
