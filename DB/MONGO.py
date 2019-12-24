# from DB import *
# from pymongo import MongoClient
# MONGO = MongoClient("mongodb://{}:{}@{}:{}/{}".format(mongo['user'], mongo['password'], mongo['host'], mongo['port'], mongo['db']))
#
# # MONGO_DB = MONGO.mongo['db']
# # MONGO_SET = MONGO_DB.mongo['set']
# ccc = {'user': 'tangluoyan', 'age': 24}
#
# db = MONGO.test
# db.authenticate('ljs', 'ljs', mechanism='SCRAM-SHA-1')
# col = db.new
# print(db)
# print(col)
# _id = col.insert_one(ccc).inserted_id()

from DB import *


# MONGO_DB = MONGO.mongo['db']
# MONGO_SET = MONGO_DB.mongo['set']
ccc = {'user': 'tangluoyan', 'age': 24}
from pymongo import MongoClient
MONGO = MongoClient('127.0.0.1', 27017)
db = MONGO.test1
col = db.new
print(db)
print(col)
col.insert_one(ccc)
for row in col.find():
    print(row)

