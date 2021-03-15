import dns, pymongo

mongoc = pymongo.MongoClient("mongodb+srv://crespi:Simple1234@sctdb.v1k99.mongodb.net/test")

lastTrans = mongoc.SCT.transactions.find_one({}, sort=[('_id', pymongo.DESCENDING)])
del lastTrans['_id']
print(lastTrans)