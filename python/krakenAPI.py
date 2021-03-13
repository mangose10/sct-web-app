import pymongo, dns

mongoc = pymongo.MongoClient("mongodb+srv://crespi:Simple1234@sctdb.v1k99.mongodb.net/test")

latest = mongoc.SCT.Test.find_one({}, sort=[('_id', pymongo.DESCENDING)])
mongoc.SCT.Test.replace_one(latest, {"set":{'it':'worked'}})