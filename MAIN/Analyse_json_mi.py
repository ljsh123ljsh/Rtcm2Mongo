from MAIN import *
import RTCM_ANALYSE.RTCM_json_mi as RTCM
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
        c = (RTCM.MSM4(data, str(int(rtcm_type, base=2))))
        res = c.result()
        del c
        return res
    elif int(rtcm_type, base=2) in [1075, 1085, 1095, 1115, 1125]:
        c = (RTCM.MSM5(data, str(int(rtcm_type, base=2))))
        res = c.result()
        del c
        return res
    elif int(rtcm_type, base=2) == 1005:
        c = RTCM.RTCM1005(data)
        res = c.result()
        del c
        return res
    elif int(rtcm_type, base=2) == 1007:
        c = RTCM.RTCM1007(data)
        res = c.result()
        del c
        return res
    elif int(rtcm_type, base=2) == 1033:
        c = RTCM.RTCM1033(data)
        res = c.result()
        del c
        return res
    else:
        return {'rtcm'+str(int(rtcm_type, 2)): "暂不支持"}


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
