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
    d = 'data.msm,11,070817.17,source3,52100,e86a64fbda61e0cc7a39a90c08004500022abdfd40003b060c5dc0a88275c0a86fad1fa9e82bfd7bf9c77da5de5b501800e5b4790000d300864330011ab130e22c001002826580000000200000007fd390d2139410d2d151c00000000398d0196c8ed2f80d7925f100000000000000000000000000000003cd5f3b4e6c26a87a7577fb11b19ec00787eafabf462a7e5e6e1a9b4fdf155fcf4d838dd3ea1518057b7ddddddddc00aafb698f3bb2c20004000800100020004000800100020000e9ed35d3004843d00128a9d5a22c006090000000000000200000007a123252241eba5a267986f800000000000001de33abf99fc4968796d81d9b0f90dfc09561f777063959a4000800100020000037b979d300484470011ab130e22c004040100100000000080000007a8272ba880007de8c720488000000000000000f3f723ac17174811457fc5c2fa6cdfe7df977770616497c00080010002000005605a5d3007a4650011ab056202c007b60000000000000200000007fbdbf3dbfbbbc3bbe8000000049b141b9a38b1e3e00ca00000000000000000000000000001cb7deb1fb2f08b0d762a9bbec3741873587ee438ff8589e0e5e8351ba16d0bfbecb9f015df7777777005b3d95e17e15c0008001000200040008001000200000692668d300133ed00103f9577462158ad2b2ef9b07a8c6cb57e9c672d300053ef0010000c27e5cd300304090010000000d5452494d424c4520424439393010352e33362c32302f4a554e2f323031380a3538323543303035353240aa90'
    while 1:
        analyse(d)
    # multithread()
