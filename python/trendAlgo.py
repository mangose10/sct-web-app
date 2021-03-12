import json

candf = open("candle.json", "r")
candles = json.loads(candf.readline())

min1 = 0
min2 = 0
max1 = 0
max2 = 0
slope = 0
min1Time = 0
min2Time = 0
max1Time = 0
max2Time = 0
uptrend = False
inTrans = False
trans = {}
tTrans = {}
tTrans['overallChange'] = 1000.0
tTrans['numTransactions'] = 0
tTrans['longestTrade'] = 0
tTrans['vol'] = 1000
min = {}
max = {}

"""
"0" : 0.00075,
  "50000" : 0.000675,
  "100000" : 0.0006,
  "500000" : 0.000525,
  "1000000" : 0.000375,
  "5000000" : 0.0003,
  "10000000" : 0
"""

def getFee(vol):
  return 0.00075
  if vol < 50000:
    return 0.00075
  elif vol < 100000:
    return 0.0006
  elif vol < 500000:
    return 0.000525
  elif vol < 1000000:
    return 0.000375
  elif vol < 5000000:
    return 0.0003
  else:
    return 0
  
for i in range(1, len(candles)-1):
  """
  #trendline = ((min2-min1)/timeDiff)*timePassed+min2
  if inTrans and (trans['buy']['time'] < candles[str(i)]['oTime']):

    timePassedEnd=int(candles[str(i)]['cTime'])-trans['buy']['time']
    y = (float(candles[str(i)]['cPrice'])-trans['buy']['price'])/timePassedEnd

    if y < slope and timePassedEnd > 60000:
      CountedSellPrice = slope*(timePassedEnd-30000)+trans['buy']['price']
      maxSellPrice = float(candles[str(i)]['high'])
      sellPrice = maxSellPrice if maxSellPrice < CountedSellPrice else CountedSellPrice

      trans['sell'] = {'time':int(candles[str(i)]['cTime'])-30000, 'price':sellPrice}
      trans['change'] = {'percent':(trans['sell']['price']/trans['buy']['price'])-1-getFee(tTrans['vol']), 'timeSpan':timePassedEnd-30000, 'slope': slope}
      trans['change']['sellType'] = "slope"

      tTrans[str(tTrans['numTransactions'])] = trans
      tTrans['overallChange'] = (tTrans['overallChange'] * (1+trans['change']['percent']))
      tTrans['vol'] += tTrans['overallChange']
      slope = 0
      tTrans['numTransactions'] += 1
      trans = {}
      inTrans = False
  """
  if (((candles[str(i-1)]['cPrice']) > (candles[str(i)]['cPrice'])) and ((candles[str(i)]['cPrice'] < (candles[str(i+1)]['cPrice'])))):
    min['min'+str(i)] = candles[str(i)]['cPrice']
    
    if min2Time <= 0:
      min2 = float(candles[str(i)]['cPrice'])
      min2Time = int(candles[str(i)]['cTime'])
    
    if ((int(candles[str(i)]['cTime'])-min2Time) > 120000):
      min1 = min2
      min1Time = min2Time
      min2 = float(candles[str(i)]['cPrice'])
      min2Time = int(candles[str(i)]['cTime'])

    if ((min1 > 0) and (max1 > 0)):
      uptrend = True if (min2 > min1 and max2 > max1) else False
    if uptrend:
      if not inTrans:
        slope = (min2-min1)/(min2Time-min1Time)
        #if slope > 0.0004 and slope < 0.0006:
        trans['buy'] = {'time':int(candles[str(i+1)]['cTime']), 'price':float(candles[str(i+1)]['cPrice'])}
        trans['break'] = tTrans['overallChange'] * (1+getFee(tTrans['vol']))
        trans['BTCbought'] = tTrans['overallChange']/trans['buy']['price']
        inTrans = True


  if (((candles[str(i-1)]['cPrice']) < (candles[str(i)]['cPrice'])) and ((candles[str(i)]['cPrice'] > (candles[str(i+1)]['cPrice'])))):
    max['max'+str(i)] = candles[str(i)]['cPrice']
    max1 = max2
    max1Time = max2Time
    max2 = float(candles[str(i)]['cPrice'])
    max2Time = float(candles[str(i)]['cTime'])
    
    if ((min1 > 0) and (max1 > 0)):
      uptrend = True if (min2 > min1 and max2 > max1) else False
    if ((not uptrend) and (inTrans) and (trans['BTCbought']*float(candles[str(i+1)]['cPrice']) > trans['break'])):

      sellPrice = float(candles[str(i+1)]['cPrice'])
      timePassedEnd = candles[str(i+1)]['cTime'] - trans['buy']['time']

      trans['sell'] = {'time':int(candles[str(i+1)]['cTime']), 'price':sellPrice}
      trans['change'] = {'percent':(trans['sell']['price']/(trans['buy']['price'])*(1+getFee(tTrans['vol'])))-1, 'timeSpan':timePassedEnd, 'slope': slope}
      trans['change']['sellType'] = "break"

      tTrans[str(tTrans['numTransactions'])] = trans
      tTrans['overallChange'] = (tTrans['overallChange'] * (1+trans['change']['percent']))
      tTrans['vol'] += tTrans['overallChange']
      tTrans['longestTrade'] = tTrans['longestTrade'] if tTrans['longestTrade'] > trans['change']['timeSpan'] else trans['change']['timeSpan']
      slope = 0
      tTrans['numTransactions'] += 1
      trans = {}
      inTrans = False

  

with open("mins.json", "w") as outfile:  
    json.dump(min, outfile)

with open("maxs.json", "w") as outfile:  
    json.dump(max, outfile)

with open("trans.json", "w") as outfile:  
    json.dump(tTrans, outfile, indent=2)