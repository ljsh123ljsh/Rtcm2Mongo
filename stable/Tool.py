from stable.ConvertDecimal import ConvertDecimal as cd
import math
from stable.Map import Map
from binascii import a2b_hex as ab
from zlib import compress
from json import dumps


def supplehead(s):
    '''
    :param s: 输入16进制第一位eg：3，4
    :return: 返回二进制补充的位数eg：00，0
    '''
    s1 = bin(int(s, base=16))[2:]
    s2 = ''
    for i in range(4 - len(s1)):
        s2 += '0'
    return s2


def split_content(c, lis):
    i = 0
    content_lis = []
    while i < len(lis):
        if i + 1 >= len(lis):
            end = len(c)
        else:
            end = lis[i + 1]
        content_lis.append(c[lis[i]: end])
        i += 1
    return content_lis


def extend_satli(int_lis, fl_lis, gnss_x, Nsig):
    '''
    :param int_lis: 整数部分
    :param fl_lis: 小数部分
    :param gnss_x: cell掩码
    :param Nsig: 信号数
    :return: 将整数部分、小数部分整合到ncell信号掩码中
    '''
    flag = 0
    gnss_xli = [c for c in gnss_x]
    i = 0
    while i < len(gnss_x):
        gnss_xli[i] = int(gnss_x[i], base=2) * (
                    int(int_lis[flag], base=2) + cd(fl_lis[flag], least=10).convertdecimal())
        if (i + 1) % Nsig == 0:
            flag += 1
        i += 1
    return gnss_xli

def gnss_system_server(str_b):
    dic = ['GPS', 'GLONASS', 'Galileo', 'BDS']
    li = Map('1', str_b).map_id(add=False)
    s = ""
    for l in li:
        s = s + dic[l] + '  '
    return s

def bin2ascii(str_b):
    if str_b == '':
        return 'None'
    else:
        h = hex(int(str_b, base=2))[2:]
        return str(ab(h), encoding='utf-8')

def XYZ2BLH(X, Y, Z):
    a = 6378137
    b = 6356752.3142
    e2 = (a*a-b*b)/a**2
    L = math.atan(abs(Y/X))
    if Y > 0:
        if X > 0:
            L = 2 * math.pi - L
        else:

            L = math.pi - L
    else:
        if X > 0:
            L = 2 * math.pi - L
        else:
            L = math.pi + L
    B0 = math.atan(Z/math.sqrt(X**2+Y**2))
    while 1:
        N = a/math.sqrt(1-e2*math.sin(B0)*math.sin(B0))
        # H = Z/math.sin(B0)-N*(1-e2)
        H = math.sqrt(X**2+Y**2)/math.cos(B0)-N

        B = math.atan(Z*(N+H)/(math.sqrt(X**2+Y**2)*(N*(1-e2)+H)))
        if abs(B-B0) < 0.000001:
            break
        B0 = B
    B = 180 * B0 / math.pi
    L = 180 * L / math.pi
    k = (B, L, H)
    # print('B={0:.9f}\nL={1:.9f}\nH={2:.9f}'.format(B, L, H))
    return k

def map_d30(content):
    '''
    :param content: 一个16进制以太帧
    :return: 返回生成器yield:d30
    '''
    header = 'd30'
    content = content.replace('\n', '').replace(' ', '')
    while 1:
        index = Map(header, content).map_first()
        if index is None:
            break
        index = index.span()
        length = int(content[index[1]:index[1]+3], base=16)
        data = content[index[0]:index[1]+3+length*2]
        yield data
        content = content[index[1] + 3 + length*2:]

def segment_d30(content):
    gen = map_d30(content)
    lis = []
    while 1:
        try:
            data = next(gen)
            lis.append(data)
        except StopIteration:
            break
    return lis

def dict2json_Compress(dictionary, ifcompress=1):
    '''
    :param dictionary: 输入字典类型
    :param ifcompress: 是否压缩
    :return: 字节流
    '''
    jsons = dumps(dictionary)
    jsons_bytes = bytes(jsons, encoding='utf-8')
    if ifcompress:
        return compress(jsons_bytes)
    else:
        return jsons_bytes

