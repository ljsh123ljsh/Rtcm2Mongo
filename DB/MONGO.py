from DB import *
from pymongo import MongoClient
MONGO = MongoClient(host="mongodb://{}:{}@{}:{}/{}".format(mongo['user'], mongo['password'], mongo['host'], mongo['port'], mongo['db']))

# MONGO_DB = MONGO.mongo['db']
# MONGO_SET = MONGO_DB.mongo['set']
ccc = {'user': 'tangluoyan', 'age': 24}

db = MONGO.test
db.authenticate('admin', '123456', mechanism='SCRAM-SHA-1')
col = db.new
print(db)
print(col)
_id = col.insert_one(ccc).inserted_id()

