from pymongo import MongoClient
from DB import *
__host = mongo['host']
__port = int(mongo['port'])
Mongo = MongoClient(__host, __port)

def transform2mongo(id, port, content):
    collection = Mongo[id][port]
    collection.insert_one(content)