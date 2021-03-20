import trendv2 as trend
import websocket, json, time

class MyWebSocketClient(object):

    def __init__(self, url):
      websocket.enableTrace(True)
      self.URL = url
      self.connected = False
      self.running = False

    def start(self):
      self.running = True
      self.ws = websocket.WebSocketApp(
        url=self.URL,
        on_open=self.on_open,
        on_message=self.on_message,
        on_close=self.on_close,
        on_error=self.on_error,
      )
      #print("here")
      #print(self.ws)
      self.ws.run_forever()

    def stop(self, other):
      self.running = False
      self.ws.keep_running = False

    def on_open(self, other):
      #print(self)
      #print(other)
      print('Connection opened')
      self.connected = True

    def on_message(self, other, data):
      #print(data)
      trend.algoWrapper(data, 1)

    def on_close(self, other):
      print('Connection closed')
      self.connected = False
      if self.running:
        print("Reconnecting in 15 seconds")
        time.sleep(15)
        self.start()

    def on_error(self, other, err):
      print('Error: {err}')



SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
ws = MyWebSocketClient(SOCKET)
ws.start()

