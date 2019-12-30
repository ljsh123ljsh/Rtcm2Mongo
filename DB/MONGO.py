from pymongo import MongoClient
from DB import *
__host = mongo['host']
__port = int(mongo['port'])
Mongo = MongoClient(__host, __port)