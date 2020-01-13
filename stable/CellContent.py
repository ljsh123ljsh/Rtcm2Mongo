from stable.ConvertDecimal import ConvertDecimal as cd
class CellContent:
    def __init__(self, cycle, cycle_type):
        '''
        :param cycle: (int)循环次数
        :param cycle_type: (int){'精确伪距观测值':1,'概略伪距整数':11,'概略伪距小数':12,'扩展卫星信息':13, 'GNSS 卫星概略相位距离变化率 ':14, '相位观测值':2,'相位距离锁定时间标志':3,'版周期模糊度标志':4,'GNSS信号CNR'：5}
        '''
        self.cycle = cycle
        self.cycle_type = cycle_type

    def ReturnContent(self, data):
        '''
        :param data: 输入data返回信号数据列表
        :return: 返回信号数据列表
        '''
        self.__data = data
        dic = {1: 15, 2: 22, 3: 4, 4: 1, 5: 6, 6: 15, 11: 8, 12: 10, 13: 4, 14: 14}
        lis = []
        value = dic[self.cycle_type]
        for i in range(self.cycle):
            sta = value * i
            self.__end = value * (i + 1)
            cont = data[sta:self.__end]
            lis.append(cont)
        self.__lis = lis
        return lis

    def ConvertContent(self, gnsscell):
        '''
        :param gnsscell: (str)二进制gnss单元掩码
        :return: 将信号列表与掩码融合后的list
        '''
        gnssmask = [int(c) for c in gnsscell]
        flag = 0
        i = 0
        while i < len(gnssmask):
            if gnssmask[i] == 0:
                i += 1
                continue
            gnssmask[i] *= self.__lis[flag]
            flag += 1
            i += 1
            self.gnssmask = gnssmask
        return gnssmask

    def ConvertDecimal(self, least=0, symbol=False):
        '''
        :param least:  转换时，二进制的最低位
        :param symbol: 转换时，第一位是否为符号位
        :return: 返回进制转换后的与掩码结合的列表
        '''
        return [cd(str(x), least=least, symbol=symbol).convertdecimal() for x in self.gnssmask]

    def RestContent(self):
        '''
        :return: 返回未被使用的剩余的字符
        '''
        rest_data = self.__data[self.__end:]
        return rest_data


