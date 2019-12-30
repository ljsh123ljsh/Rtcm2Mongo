from threading import Thread
from redis import StrictRedis
from DB.REDIS import REDIS_pool
from multiprocessing import Process
from MAIN.Analyse_json import Analyse_Rabbitmq_Frame
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
    print((pp[0], pp[1], str(pp[2])[:50]))
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
    multithread()
