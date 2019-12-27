from DB import MONGO
#
st = {"name":"zhangsan","age":18}
st1 = {"name":"zhahgfdhdfngsan","age":15}
mongo = MONGO.Mongo
collection = mongo['test']['new']
# db = mongo.test
# collection = db.new
collection.insert_many([st, st1])

for i in collection.find():
    print(i)