from threading import Thread
from redis import StrictRedis
from DB.REDIS import REDIS_pool
from multiprocessing import Process
from MAIN.Analyse_json import Analyse_Rabbitmq_Frame
from DB.MONGO import Mongo
from DB.RABBITMQ import exchange

def transform2mongo(id, port, content):
    collection = Mongo[id][port]
    collection.insert_one(content)

def get4redis(REDIS_pool):
    r = StrictRedis(connection_pool=REDIS_pool)
    data = r.rpop(exchange)
    print(data)
    return data

def analyse(data):
    pp = Analyse_Rabbitmq_Frame(str(data))
    transform2mongo(pp[0], pp[1], pp[2])

def multithread():
    while 1:
        # thread_list = []
        for i in range(50):
            thr = Thread(target=analyse, args=(get4redis(REDIS_pool), ))
            # thread_list.append(thr)
            thr.start()
        # for thr in thread_list:
        #     thr.start()

def multiprocess(thr):
    pass

if __name__ == '__main__':
    multithread()
