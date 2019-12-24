from MAIN import *
# from RTCM_ANALYSE.RTCM_json import RTCM
from RTCM_ANALYSE.RTCM_pandas import RTCM
'''
解析d30
'''


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
    print("——"*30)
    print("RTCM格式：{}".format(int(rtcm_type, base=2)))
    print("比特数：{};\t字节数:{}".format(length * 8, length))
    if int(rtcm_type, base=2) in [1074, 1084, 1094, 1114, 1124]:  # 1074-GPS, 1084-GLONASS, 1094-GALILEO, 1114-QZZSS, 1124-BDS
        a = RTCM().MSM4(data, str(int(rtcm_type, base=2)))
        try:
            print(a)
        except:
            pass
    elif int(rtcm_type, base=2) == 1005:
        a = RTCM().rtcm1005(data)
        try:
            print(a)
        except:
            pass
    elif int(rtcm_type, base=2) == 1007:
        a = RTCM().rtcm1007(data)
        try:
            print(a)
        except:
            pass
    elif int(rtcm_type, base=2) == 1033:
        a = RTCM().rtcm1033(data)
        try:
            print(a)
        except:
            pass
    else:
        print("暂不支持")


def analyseWholeFrame(content):
    content_lis = segment_d30(content)
    thread_list = []
    for data in content_lis:
        thr = Thread(target=analyse, args=(data, ))
        thread_list.append(thr)
    for l in thread_list:
        l.start()

