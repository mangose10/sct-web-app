import pymongo, dns, sys, warnings
warnings.filterwarnings('ignore')

mongoc = pymongo.MongoClient("mongodb://leo:Melmmldm1%21@10.0.0.207:27017/?authSource=admin&readPreference=secondary&ssl=false")

start = int(sys.argv[1])
end = start + (1000 * 60 * 60 * 24)

transCol = mongoc.SCT.transactions
arr = []

for t in transCol.find({"buy.time":{'$gte':start, '$lte':end}}):
  del t['_id']
  arr.append(t)

print(str(arr))