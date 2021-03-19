import pymongo, dns

mongoc = pymongo.MongoClient("mongodb://leo:Melmmldm1%21@174.48.53.242:27017/?authSource=admin&readPreference=secondary&ssl=false")
latest = mongoc.SCT.transactions.find_one({}, sort=[('_id', pymongo.DESCENDING)])



del latest['_id']
print(latest)