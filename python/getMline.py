import pymongo, dns

mongoc = pymongo.MongoClient("mongodb+srv://crespi:Simple1234@sctdb.v1k99.mongodb.net/test")
latest = mongoc.SCT.transactions.find_one({}, sort=[('_id', pymongo.DESCENDING)])


if (len(latest) < 5):
  del latest['_id']
  print(latest)
else:
  print("{'empty':'true'}")