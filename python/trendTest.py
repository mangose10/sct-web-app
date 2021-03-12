import json

trans = ""

with open("trans.json", "r") as infile:
  trans = trans + infile.read()

trano = json.loads(trans)
compound = 1

for i in range(trano['numTransactions']):
  compound *= (1 + trano[str(i)]['change']['percent'])

candf = open("candle.json", "r")
candles = json.loads(candf.readline())

normal = (float(candles['0']['oPrice']) - float(candles[str(len(candles)-1)]['cPrice']))/float(candles['0']['oPrice'])

print("normal:" + str(normal))
print("compound" + str(compound-1))