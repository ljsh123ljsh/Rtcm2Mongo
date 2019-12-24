from pymongo import MongoClient
host = '127.0.0.1'
client = MongoClient(host, 27017)
#连接mydb数据库,账号密码认证
db = client.admin    # 先连接系统默认数据库admin
# 下面一条更改是关键，我竟然尝试成功了，不知道为啥，先记录下踩的坑吧
db.authenticate("ljs", "ljs", mechanism='SCRAM-SHA-1') # 让admin数据库去认证密码登录，好吧，既然成功了，
my_db = client.test  # 再连接自己的数据库mydb
collection = my_db.new   # myset集合，同上解释
collection.insert_one({"name":"zhangsan","age":18})   # 插入一条数据，如果没出错那么说明连接成功
for i in collection.find():
    print(i)