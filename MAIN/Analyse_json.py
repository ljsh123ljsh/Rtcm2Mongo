from MAIN import *
from RTCM_ANALYSE.RTCM_json import RTCM
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
        return {'rtcm'+str(int(rtcm_type)): "暂不支持"}


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
        # key = list(res.keys())[0]
        result_list.append(res)
    return result_list

def Analyse_Rabbitmq_Frame(frame):
    '''
    :param frame: 一个rabbitmq帧
    :return: 返回解析后的json
    '''
    try:
        frame_list = frame.split(',')
        frame_dic = {
            'client_mountpoint': frame_list[3],
            'client_time': frame_list[2],
            'client_rtcm': analyseWholeFrame(frame_list[5])
        }
    except:
        frame_dic = {
            'client_mountpoint': 'novalue',
            'client_time': 'novalue',
            'client_rtcm': analyseWholeFrame(frame)
        }
        return ('novalue', 'novalue', frame_dic)
    return ('a'+frame_list[1], 'a'+frame_list[4], frame_dic)
