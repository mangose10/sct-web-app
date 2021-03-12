import websocket, json, pprint, numpy, dns
import tconfig
import variables
from binance.enums import *
from binance.client import Client
import pymongo

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"

mongoc = pymongo.MongoClient(tconfig.MONGO_URL)
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

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
  message = json.loads(message)

  #print(message)

  if not bool(variables.candles[2]):
    variables.candles[2] = fillCandle(message)
    print(variables.candles[2])
  elif variables.candles[2]['cTime'] < message['k']['t']:
    variables.candles[0] = variables.candles[1]
    variables.candles[1] = variables.candles[2]
    variables.candles[2] = fillCandle(message)
    print(variables.candles[0]['cPrice'])

    if (bool(variables.candles[0]) and ((variables.candles[0]['cPrice']) > (variables.candles[1]['cPrice'])) and ((variables.candles[1]['cPrice'] < (variables.candles[2]['cPrice'])))):
      #min['min'+str(i)] = candles[str(i)]['cPrice']
      print("found min")
      if variables.min2Time <= 0:
        variables.min2 = float(variables.candles[1]['cPrice'])
        variables.min2Time = int(variables.candles[1]['cTime'])
      
      if ((int(variables.candles[1]['cTime'])-variables.min2Time) > 120000):
        variables.min1 = variables.min2
        variables.min1Time = variables.min2Time
        variables.min2 = float(variables.candles[1]['cPrice'])
        variables.min2Time = int(variables.candles[1]['cTime'])

      if ((variables.min1 > 0) and (variables.max1 > 0)):
        variables.uptrend = True if (variables.min2 > variables.min1 and variables.max2 > variables.max1) else False
      if variables.uptrend:
        if not variables.inTrans:
          variables.slope = (variables.min2-variables.min1)/(variables.min2Time-variables.min1Time)
          #if slope > 0.0004 and slope < 0.0006:
          variables.trans['buy'] = {'time':int(variables.candles[2]['cTime']), 'price':float(variables.candles[2]['cPrice'])}
          variables.trans['break'] = variables.curVal * (1+variables.FEE)
          variables.trans['BTCbought'] = variables.curVal/variables.trans['buy']['price']
          variables.inTrans = True
          order = client.order_market_buy(
            symbol='BTCUSD',
            quantity=1)
          print("BOUGHT")


    if (bool(variables.candles[0]) and ((variables.candles[0]['cPrice']) < (variables.candles[1]['cPrice'])) and ((variables.candles[1]['cPrice'] > (variables.candles[2]['cPrice'])))):
      #max['max'+str(i)] = candles[str(i)]['cPrice']
      print("found max")
      variables.max1 = variables.max2
      variables.max1Time = variables.max2Time
      variables.max2 = float(variables.candles[1]['cPrice'])
      variables.max2Time = float(variables.candles[1]['cTime'])
      
      if ((variables.min1 > 0) and (variables.max1 > 0)):
        variables.uptrend = True if (variables.min2 > variables.min1 and variables.max2 > variables.max1) else False
      if ((not variables.uptrend) and (variables.inTrans) and (variables.trans['BTCbought']*float(variables.candles[1]['cPrice']) > variables.trans['break'])):

        sellPrice = float(variables.candles[2]['cPrice'])
        timePassedEnd = variables.candles[2]['cTime'] - variables.trans['buy']['time']

        variables.trans['sell'] = {'time':int(variables.candles[2]['cTime']), 'price':sellPrice}
        variables.trans['change'] = {'percent':(variables.trans['sell']['price']/(variables.trans['buy']['price'])*(1+variables.FEE))-1, 'timeSpan':timePassedEnd, 'slope': variables.slope}
        variables.trans['change']['sellType'] = "break"

        """
        tTrans[str(tTrans['numTransactions'])] = trans
        tTrans['vol'] += tTrans['overallChange']
        tTrans['longestTrade'] = tTrans['longestTrade'] if tTrans['longestTrade'] > trans['change']['timeSpan'] else trans['change']['timeSpan']
        tTrans['numTransactions'] += 1
        """
        variables.curVal = (variables.curVal * (1+variables.trans['change']['percent']))
        mongoc.transactions.insert_one(variables.trans)
        variables.slope = 0
        variables.trans = {}
        variables.inTrans = False
        order = client.order_market_sell(
          symbol='BTCUSD',
          quantity=1)
        print("SOLD")

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()