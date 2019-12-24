from MAIN import *
from RTCM_ANALYSE.RTCM_json import RTCM
from stable.Tool import dict2json_Compress
'''
解析d30
'''

class MyThread(Thread):
    def __init__(self, target=None, args=()):
        self.target = target
        Thread.__init__(self)
        self.args = args
    def run(self):
        self.result = self.target(self.args[0])
    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def analyse(data):
    '''
    :param data: d30开始的报文
    :return: 解析
    '''
    data = data[3:]
    length = int(data[0:3], base=16)
    data = data[3:]
    supp = supplehead(data[0])
    data = supp + bin(int(data, base=16))[2:]
    rtcm_type = data[0:12]  # 差分电文类型12bis
    if int(rtcm_type, base=2) in [1074, 1084, 1094, 1114, 1124]:
        return RTCM().MSM4(data, str(int(rtcm_type, base=2)))
    elif int(rtcm_type, base=2) == 1005:
        return RTCM().rtcm1005(data)
    elif int(rtcm_type, base=2) == 1007:
        return RTCM().rtcm1007(data)
    elif int(rtcm_type, base=2) == 1033:
        return RTCM().rtcm1033(data)
    else:
        return {'type': 'rtcm'+str(int(rtcm_type)), 'error': "暂不支持"}


def analyseWholeFrame(content):
    content_lis = segment_d30(content)
    thread_list = []
    result_list = []
    for data in content_lis:
        thr = MyThread(target=analyse, args=(data,))
        thread_list.append(thr)
    for l in thread_list:
        l.run()
    for l in thread_list:
        res = l.get_result()
        result_list.append(res)
    return result_list

def Analyse_Rabbitmq_Frame(frame):
    '''
    :param frame: 一个rabbitmq帧
    :return: 返回解析后的json
    '''
    frame_list = frame.split(',')
    frame_dic = {
        'testid': frame_list[1],
        'client_port': frame_list[4],
        'client_time': frame_list[2],
        'client_mountpoint': frame_list[3],
        'client_rtcm': analyseWholeFrame(frame_list[5])
    }
    return frame_dic

if __name__ == '__main__':
    cc = 'data.msm,11,070817.17,source3,52096,d3004d4320011abae5423f800000004180000000202001007dd19190f3321a6ce0d7c1fb8176dd3da20497c93111abfa89cbedf3dfba03be2cb9fc13a4207230a27e42792affffffff00bafcf1bb4cf5602cbfd3002443c00128b38a023f801000000000000000204000006817e677ecd7fe8116fa00cffe6da8fc024fd3003f4460011abae5423f800400008000000000080101007e9a93a6983f09be0e7c19f231ed2fda97f48cbfd7067f6f01fc520ffd7dbffbd0ffffff818e99e19e60da72ddd3002a4640011aba0a803f80020000000000000020820000777ae311a60f0c1b9e599cf83c1fe3095fff8c31c8f2ea0cd300133ed00103f957745f928ad2b2f3b007a8c6ce3f7da1b3d300053ef0010000c27e5cd300304090010000000d5452494d424c4520424439393010352e33362c32302f4a554e2f323031380a3538323543303035353240aa90'
    pp = Analyse_Rabbitmq_Frame(cc)
    print(pp)
    com_pp = dict2json_Compress(pp)
    print(com_pp)

    from pymongo import MongoClient

    MONGO = MongoClient('127.0.0.1', 27017)
    db = MONGO.test1
    col = db.new
    print(db)
    print(col)
    col.insert_one(pp)
    for row in col.find():
        print(row)


