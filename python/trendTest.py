import websocket, json, pprint, numpy, dns
import tconfig
from binance.enums import *
from binance.client import Client
import pymongo

min1 = 0
min2 = 0
max1 = 0
max2 = 0
slope = 0
min1Time = 0
min2Time = 0
max1Time = 0
max2Time = 0
FEE = 0.00075
uptrend = False
inTrans = False
trans = {}
#tTrans = {}
#tTrans['overallChange'] = 1000.0
curVal = 1000.0
#tTrans['numTransactions'] = 0
#tTrans['longestTrade'] = 0
#tTrans['vol'] = 1000
min = {}
max = {}
candles = [{},{},{}]

pp = pprint.PrettyPrinter(indent=2)

mongoc = pymongo.MongoClient("mongodb+srv://crespi:Simple1234@sctdb.v1k99.mongodb.net/test")
client = Client(api_key=tconfig.API_KEY, api_secret=tconfig.API_SECRET, tld="us")
client.API_URL = 'https://testnet.binance.vision/api'

def fillCandle(message):
  obj = {
      'oTime' : message['k']['t'],
      'oPrice' : message['k']['o'],
      'high': message['k']['h'],
      'low': message['k']['l'],
      'cPrice': message['k']['c'],
      'volume': message['k']['v'],
      'cTime': message['k']['T'],
    }
  return obj

def algoWrapper(message):
  message = json.loads(message)

  if not bool(candles[2]):
    candles[2] = fillCandle(message)
  elif candles[2]['cTime'] < message['k']['t']:
    buy()
    sell()
  else:
    candles[2] = fillCandle(message)


def buy():
  if (bool(candles[0]) and ((candles[0]['cPrice']) > (candles[1]['cPrice'])) and ((candles[1]['cPrice'] < (candles[2]['cPrice'])))):
    #min['min'+str(i)] = candles[str(i)]['cPrice']
    print("found min")
    if min2Time <= 0:
      min2 = float(candles[1]['cPrice'])
      min2Time = int(candles[1]['cTime'])
    
    if ((int(candles[1]['cTime'])-min2Time) > 120000):
      min1 = min2
      min1Time = min2Time
      min2 = float(candles[1]['cPrice'])
      min2Time = int(candles[1]['cTime'])

    if ((min1 > 0) and (max1 > 0)):
      uptrend = True if (min2 > min1 and max2 > max1) else False
    if uptrend:
      if not inTrans:
        slope = (min2-min1)/(min2Time-min1Time)
        #if slope > 0.0004 and slope < 0.0006:
        trans['buy'] = {'time':int(candles[2]['cTime']), 'price':float(candles[2]['cPrice'])}
        trans['break'] = curVal * (1+FEE)
        trans['BTCbought'] = curVal/trans['buy']['price']
        inTrans = True
        print("BOUGHT")
        """order = client.order_market_buy(
          symbol='BTCBUSD',
          quantity=1)
        trans['buy']['time'] = order['transactTime']"""


def sell():
  if (bool(candles[0]) and ((candles[0]['cPrice']) < (candles[1]['cPrice'])) and ((candles[1]['cPrice'] > (candles[2]['cPrice'])))):
    #max['max'+str(i)] = candles[str(i)]['cPrice']
    print("found max")
    max1 = max2
    max1Time = max2Time
    max2 = float(candles[1]['cPrice'])
    max2Time = float(candles[1]['cTime'])
    
    if ((min1 > 0) and (max1 > 0)):
      uptrend = True if (min2 > min1 and max2 > max1) else False
    if ((not uptrend) and (inTrans) and (trans['BTCbought']*float(candles[1]['cPrice']) > trans['break'])):

      sellPrice = float(candles[2]['cPrice'])
      timePassedEnd = candles[2]['cTime'] - trans['buy']['time']

      trans['sell'] = {'time':int(candles[2]['cTime']), 'price':sellPrice}
      trans['change'] = {'percent':(trans['sell']['price']/(trans['buy']['price'])*(1+FEE))-1, 'timeSpan':timePassedEnd, 'slope': slope}
      trans['change']['sellType'] = "break"

      curVal = (curVal * (1+trans['change']['percent']))
      mongoc.SCT.transactions.insert_one(trans)
      slope = 0
      trans = {}
      inTrans = False
      print("SOLD")
      """order = client.order_market_sell(
        symbol='BTCBUSD',
        quantity=1)
      trans['sell']['time'] = order['transactTime']"""

  candles[0] = candles[1]
  candles[1] = candles[2]
  candles[2] = fillCandle(message)
  print(str(candles[0]['cPrice']) + " - " + str(candles[0]['oTime']))