import json
import trendv2 as trend

log = open("trans.json", "w")
log.write("{\n\"trans\":[\n")
log.close()

candf = open("candle.json", "r")
candles = json.loads(candf.readline())

tots = {}

for i in range(1, len(candles)-1):
  tots = trend.algoWrapper(json.dumps(candles[i]), 0)

log = open("trans.json", "a")
log.write(json.dumps(tots, indent=2)+"\n]\n}")
log.close()