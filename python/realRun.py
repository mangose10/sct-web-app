import websocket, json, pprint
from binance.enums import *
from binance.client import Client
import trendRealv2 as trend

SOCKET = "wss://stream.binance.us:9443/ws/btcusd@kline_1m"
pp = pprint.PrettyPrinter(indent=2)

def on_open(ws):
  print('opened connection')

def on_close(ws):
  print('closed connection')


def on_message(ws, message):
  #pp.pprint(type(message))
  tots = trend.algoWrapper(message)
  pp.pprint(tots)

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()


#sale example
'''
{
  'symbol': 'BTCUSD', 
  'orderId': 282197865, 
  'orderListId': -1, 
  'clientOrderId': 'nkOswZygCHtXjq92zyfxax', 
  'transactTime': 1616246481474, 
  'price': '0.0000', 
  'origQty': '0.00168200', 
  'executedQty': '0.00168200', 
  'cummulativeQuoteQty': '100.6375', 
  'status': 'FILLED', 
  'timeInForce': 'GTC', 
  'type': 'MARKET', 
  'side': 'SELL', 
  'fills': [{
    'price': '59832.0700', 
    'qty': '0.00168200', 
    'commission': '0.00027758', 
    'commissionAsset': 'BNB', 
    'tradeId': 9154804
  }]
}
'''

'''
{
  'symbol': 'BTCUSD', 
  'orderId': 282208973, 
  'orderListId': -1, 
  'clientOrderId': 'Bwdky1bCUtfbQbKU5w6AXA', 
  'transactTime': 1616247268076, 
  'price': '0.0000', 
  'origQty': '0.00168600', 
  'executedQty': '0.00168600', 
  'cummulativeQuoteQty': '100.6332', 
  'status': 'FILLED', 
  'timeInForce': 'GTC', 
  'type': 'MARKET', 
  'side': 'BUY', 
  'fills': [{
    'price': '59687.5700', 
    'qty': '0.00168600', 
    'commission': '0.00027909', 
    'commissionAsset': 'BNB', 
    'tradeId': 9155439
  }]
}
'''