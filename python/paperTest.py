import websocket, json, pprint
from binance.enums import *
from binance.client import Client
import trendv2 as trend

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
pp = pprint.PrettyPrinter(indent=2)

def on_open(ws):
  print('opened connection')

def on_close(ws):
  print('closed connection')


def on_message(ws, message):
  #pp.pprint(type(message))
  tots = trend.algoWrapper(message)
  #pp.pprint(tots)

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()