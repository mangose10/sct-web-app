import time
import sys
from binance.enums import *
from binance.client import Client

key = "8rKrbQ8GpcicyQbGpxF96ihVbsUixobf3SAgprCskLIi5wv0l3RJAUGxA0DvW0U7"
secret = "qGzMO4K4CTnz8jRaaCqDEl263topFa1qwpPzMdrzP1m6YeaeukS1oRaMUL5ga6ae"
client = Client(api_key=key, api_secret=secret, tld="us")

bought = client.create_test_order(
  symbol='BTCUSD',
  side=SIDE_BUY,
  type=ORDER_TYPE_MARKET,
  quantity=0.001,
  newOrderRespType='FULL'
)
print(bought)


sold = client.create_test_order(
  symbol='BTCUSD',
  side=SIDE_SELL,
  type=ORDER_TYPE_MARKET,
  quantity=0.001
)
print(sold)