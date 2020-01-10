from threading import Thread
from redis import StrictRedis
from DB.REDIS import REDIS_pool
from MAIN.Analyse_json_mi import Analyse_Rabbitmq_Frame
from DB.MONGO import Mongo
from DB.RABBITMQ import exchange
class Nonedata(Exception):
    pass

def transform2mongo(id, port, content):
    collection = Mongo[id][port]
    collection.insert_one(content)

def get4redis(REDIS_pool):
    r = StrictRedis(connection_pool=REDIS_pool)
    data = r.rpop(exchange)
    if data == None:
        raise Nonedata()
    return data

def analyse(data):
    pp = Analyse_Rabbitmq_Frame(str(data))
    print((pp[0], pp[1], str(pp[2])))
    transform2mongo(pp[0], pp[1], pp[2])

def multithread():
    while 1:
        # for i in range(50):
        try:
            thr = Thread(target=analyse, args=(get4redis(REDIS_pool), ))
            thr.start()
        except Nonedata:
            pass

if __name__ == '__main__':
    d = 'data.msm,11,070817.17,source3,52100,d3004d4320011abae5423f800000004180000000202001007dd19190f3321a6ce0d7c1fb8176dd3da20497c93111abfa89cbedf3dfba03be2cb9fc13a4207230a27e42792affffffff00bafcf1bb4cf5602cbfd3002443c00128b38a023f801000000000000000204000006817e677ecd7fe8116fa00cffe6da8fc024fd3003f4460011abae5423f800400008000000000080101007e9a93a6983f09be0e7c19f231ed2fda97f48cbfd7067f6f01fc520ffd7dbffbd0ffffff818e99e19e60da72ddd3002a4640011aba0a803f80020000000000000020820000777ae311a60f0c1b9e599cf83c1fe3095fff8c31c8f2ea0cd300133ed00103f957745f928ad2b2f3b007a8c6ce3f7da1b3d300053ef0010000c27e5cd300304090010000000d5452494d424c4520424439393010352e33362c32302f4a554e2f323031380a3538323543303035353240aa90'
    while 1:
        analyse(d)
    # multithread()
