import json, pprint, dns, pymongo
from binance.enums import *
from binance.client import Client
from variables import *

pp = pprint.PrettyPrinter(indent=2)

#client = Client(api_key=tconfig.API_KEY, api_secret=tconfig.API_SECRET, tld="us")
#client.API_URL = 'https://testnet.binance.vision/api'

#key = "8rKrbQ8GpcicyQbGpxF96ihVbsUixobf3SAgprCskLIi5wv0l3RJAUGxA0DvW0U7"
#secret = "qGzMO4K4CTnz8jRaaCqDEl263topFa1qwpPzMdrzP1m6YeaeukS1oRaMUL5ga6ae"
#client = Client(api_key=key, api_secret=secret, tld="us")

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

def candleToBBAND(data):
  
  obj = []
  i = 0
  #print(len(data))
  for d in range(len(data)):
    c = float(data[d][4])
    obj.append(c)

  return numpy.array(obj)

def candleToDX(data):
  
  obj = {}
  arrc = []
  arrh = []
  arrl = []
  i = 0
  #print(len(data))
  for d in range(len(data)):
    c = float(data[d][4])
    h = float(data[d][2])
    l = float(data[d][3])
    arrc.append(c)
    arrh.append(h)
    arrl.append(l)
  
  obj = {
    'c': arrc,
    'h': arrh,
    'l': arrl
  }

  return obj

def algoWrapper(message, outType=0):
  global candles
  global mongoc
  message = json.loads(message)
  myOutType = outType
  if myOutType == 1:
    mongoc = pymongo.MongoClient("mongodb+srv://crespi:Simple1234@sctdb.v1k99.mongodb.net/test")

  if not bool(candles[2]):
    candles[2] = fillCandle(message)
  elif candles[2]['cTime'] < message['k']['t']:
    buy()
    sell()
    candles[0] = candles[1]
    candles[1] = candles[2]
    candles[2] = fillCandle(message)
    #if (bool(candles[0])):
      #print(str(candles[0]['cPrice']) + " - " + str(candles[0]['oTime']))    
  else:
    candles[2] = fillCandle(message)

  return {
    'overallValue':curVal,
    'longestTrade':longestTrade,
    'lastTrans':trans,
    'lastTime':candles[2]['cTime'],
    'numTrans':numTrans
  }


def buy():
  global candles
  global min1
  global min2
  global min1Time
  global min2Time
  global max1
  global max2
  global uptrend
  global inTrans
  global trans
  global curVal
  global FEE
  global slope

  if (bool(candles[0]) and ((candles[0]['cPrice']) > (candles[1]['cPrice'])) and ((candles[1]['cPrice'] < (candles[2]['cPrice'])))):
    #print("found min")
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

    if uptrend and not inTrans:
      slope = (min2-min1)/(min2Time-min1Time)

      if (slope > 0.0001):
        
        trans['buy'] = {'time':int(candles[2]['cTime']), 'price':float(candles[2]['cPrice'])}
        trans['break'] = curVal * (1+FEE)
        trans['BTCbought'] = curVal/trans['buy']['price']
        inTrans = True
        print("BOUGHT")
      


def sell():
  global candles
  global min1
  global min2
  global max1Time
  global max2Time
  global max1
  global max2
  global uptrend
  global inTrans
  global trans
  global curVal
  global FEE
  global myOutType
  global slope
  global longestTrade
  global numTrans

  if (bool(candles[0]) and ((candles[0]['cPrice']) < (candles[1]['cPrice'])) and ((candles[1]['cPrice'] > (candles[2]['cPrice'])))):
    #print("found max")
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

      longestTrade = max(longestTrade, timePassedEnd)
      curVal = (curVal * (1+trans['change']['percent']))
      numTrans += 1
      if myOutType == 1:
        mongoc.SCT.transactions.insert_one(trans)
      if myOutType == 0:
        log = open("trans.json", "a")
        log.write(json.dumps(trans, indent=2)+",\n")
        log.close()

      slope = 0
      trans = {}
      inTrans = False
      print("SOLD")