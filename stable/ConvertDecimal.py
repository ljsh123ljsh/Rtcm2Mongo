class ConvertDecimal:
    def __init__(self, strbin, least=0, symbol=False):
        # print(strbin)
        '''
        :param strbin: 需要转换的二进制str
        :param least: 二进制小数的最低位数（默认为0）
        :param symbol: 第一位是否为符号位（默认不是符号位）
        '''
        self.strbin = strbin
        self.least = least
        self.symbol = symbol

    def convertdecimal(self):
        '''
        :return: 返回十进制
        '''
        if self.symbol == True:  # 第一位为符号位
            if self.strbin[0] == '1':  # 1代表负数，补码转换
                adaptor = bin(int(self.strbin[1:], base=2) - 1)
                if adaptor[0] == '-':  # 解决传输数据为“10000000000”形式
                    num_bin = adaptor[3:]
                else:
                    num_bin = adaptor[2:]
                num_bin = num_bin.replace('0', '2').replace('1', '0').replace('2', '1')
                num = 0 - int(num_bin, base=2) * 2 ** (0 - self.least)
            else:  # 0代表正数，不做变换
                num_bin = '0' + self.strbin[1:]
                num = int(str(num_bin), base=2) * 2 ** (0 - self.least)
        else:  # 第一位不代表符号
            try:
                num = int(self.strbin, base=2) * 2 ** (0 - self.least)
            except ValueError:
                num = 0
        return num