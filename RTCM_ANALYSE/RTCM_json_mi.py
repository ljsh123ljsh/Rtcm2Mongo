from RTCM_ANALYSE import *
r = StrictRedis(connection_pool=REDIS.REDIS_pool)




class MSM4():
    def __init__(self, data, rtcmtype):
        dic_result = {}
        tt = 'rtcm' + str(rtcmtype)[:-1]
        DIC = r.hgetall(tt)
        if DIC == None:
            load2redis.main()
            DIC = r.hgetall(tt)
        try:
            # 12bits参考站ID； 30bitsGNSS历元； 1bit多点文标志； 7bits保留位； 2bits时钟校准标志； 2bits拓展时钟标志； 1bitGNSS平滑类型标志； 3bitsGNSS平滑区间  共61bits省略
            ID = data[12:24]
            gnss_liyuan = data[24:24+30]
            # dic_result['type'] = 'rtcm' + str(rtcmtype)
            dic_result['参考站ID'] = cd(ID).convertdecimal()
            dic_result['GNSS历元'] = cd(gnss_liyuan).convertdecimal()
            gnss_sta = data[73:74 + 64]  # 卫星掩码64bits
            sat = Map('1', gnss_sta)
            Nsat = sat.map_amount()  # 卫星数
            Nsat_id = sat.map_id()
            gnss_sig = data[137:137 + 32]  # 信号掩码32bits
            sig = Map('1', gnss_sig)
            Nsig = sig.map_amount()  # 信号数
            Nsig_id = sig.map_id()
            Nsig_id = [loads(DIC[str.encode(str(x))])['FrequencyBand'] for x in Nsig_id]

            X = Nsat * Nsig
            gnss_x = data[169:169 + X]  # 单元掩码X bits
            Ncell = Map('1', gnss_x).map_amount()  # 单元掩码数
            # print(Ncell)
            dic_result['卫星数'] = Nsat
            dic_result['信号数'] = Nsig
            dic_result['信号类型'] = str(Nsig_id)
            dic_result['单元数'] = Ncell
            # print(dic_result)

            # -----------卫星数据data2------------
            data2 = data[169 + X:]
            pse11 = CellContent(Nsat, 11)
            pse11_li = pse11.ReturnContent(data2)
            data22 = pse11.RestContent()
            pse12 = CellContent(Nsat, 12)
            pse12_li = pse12.ReturnContent(data22)
            gnss = extend_satli(pse11_li, pse12_li, gnss_x, Nsig)
            # -----------信号数据datan------------
            datan = pse12.RestContent()
            dic = {}
            key = {1: '精确伪距', 2: '载波相位', 5: '信噪比CNR'}
            i = 1
            while i <= 5:
                p = CellContent(Ncell, i)
                p.ReturnContent(datan)  # 1精确伪距,2相位距离,3相位距离锁定时间标志,4半周模糊度标志,5信噪比CNR
                p_ll = p.ConvertContent(gnss_x)  # 列表与单元掩码融合后
                if i == 1:  # 精确伪距时间处理
                    p_ll = nparray(p.ConvertDecimal(least=24, symbol=True)).tolist()
                    ifAllZero = str(npall(p_ll == 0))
                    com = {'ifAllZero': ifAllZero, 'content': p_ll}
                    # print(com)
                elif i == 2:  # 2相位距离处理
                    p_ll = nparray(p.ConvertDecimal(least=24, symbol=True)).tolist()
                    ifAllZero = str(npall(p_ll == 0))
                    com = {'ifAllZero': ifAllZero, 'content': p_ll}
                elif i == 5:  # 信噪比处理
                    p_ll = nparray(p.ConvertDecimal()).tolist()
                    ifAllZero = str(npall(p_ll == 0))
                    com = {'ifAllZero': ifAllZero, 'content': p_ll}
                else:
                    i += 1
                    continue
                dic[key[i]] = com
                datan = p.RestContent()
                i += 1

            i += 1
            while i < len(gnss):
                dic['精确伪距']['content'][i] = (gnss[i] + dic['精确伪距']['content'][i]) * 299792458 / 1000
                i += 1

            for i in [1, 2, 5]:
                dic_result[key[i]] = dic[key[i]]
            self.dic_result = {
                'rtcm' + str(rtcmtype): dic_result
            }

        except:
            self.dic_result = {'rtcm' + str(rtcmtype) + '-error': '内容异常'}
    def result(self):
        return self.dic_result
    def __del__(self):
        pass

class MSM5():
    def __init__(self, data, rtcmtype):
        dic_result = {}
        tt = 'rtcm' + str(rtcmtype)[:-1]
        DIC = r.hgetall(tt)
        if DIC == None:
            load2redis.main()
            DIC = r.hgetall(tt)
        try:
            # 12bits参考站ID； 30bitsGNSS历元； 1bit多点文标志； 7bits保留位； 2bits时钟校准标志； 2bits拓展时钟标志； 1bitGNSS平滑类型标志； 3bitsGNSS平滑区间  共61bits省略
            ID = data[12:24]
            gnss_liyuan = data[24:24+30]
            # dic_result['type'] = 'rtcm' + str(rtcmtype)
            dic_result['参考站ID'] = cd(ID).convertdecimal()
            dic_result['GNSS历元'] = cd(gnss_liyuan).convertdecimal()
            gnss_sta = data[73:74 + 64]  # 卫星掩码64bits
            sat = Map('1', gnss_sta)
            Nsat = sat.map_amount()  # 卫星数
            Nsat_id = sat.map_id()
            gnss_sig = data[137:137 + 32]  # 信号掩码32bits
            sig = Map('1', gnss_sig)
            Nsig = sig.map_amount()  # 信号数
            Nsig_id = sig.map_id()
            Nsig_id = [loads(DIC[str.encode(str(x))])['FrequencyBand'] for x in Nsig_id]

            X = Nsat * Nsig
            gnss_x = data[169:169 + X]  # 单元掩码X bits
            Ncell = Map('1', gnss_x).map_amount()  # 单元掩码数
            # print(Ncell)
            dic_result['卫星数'] = Nsat
            dic_result['信号数'] = Nsig
            dic_result['信号类型'] = str(Nsig_id)
            dic_result['单元数'] = Ncell
            # print(dic_result)

            # -----------卫星数据data2------------
            data2 = data[169 + X:]
            pse11 = CellContent(Nsat, 11)
            pse11_li = pse11.ReturnContent(data2)
            data22 = pse11.RestContent()
            pse13 = CellContent(Nsat, 13)
            pse13_li = pse13.ReturnContent(data22)  # 扩展卫星信息
            data22 = pse13.RestContent()
            pse12 = CellContent(Nsat, 12)
            pse12_li = pse12.ReturnContent(data22)
            data22 = pse12.RestContent()
            pse14 = CellContent(Nsat, 14)
            pse14_li = pse14.ReturnContent(data22)
            # print(pse14_li)
            gnss = extend_satli(pse11_li, pse12_li, gnss_x, Nsig)
            gnss_00 = extend_satli(pse14_li, ['00' for i in pse14_li], gnss_x, Nsig)
            # -----------信号数据datan------------
            datan = pse14.RestContent()
            dic = {}
            key = {1: '精确伪距', 2: '载波相位', 5: '信噪比CNR', 6: '精确相位距离变化率'}
            i = 1
            while i <= 6:
                p = CellContent(Ncell, i)
                p.ReturnContent(datan)  # 1精确伪距,2相位距离,3相位距离锁定时间标志,4半周模糊度标志,5信噪比CNR
                p_ll = p.ConvertContent(gnss_x)  # 列表与单元掩码融合后
                if i == 1:  # 精确伪距时间处理
                    p_ll = nparray(p.ConvertDecimal(least=24, symbol=True)).tolist()
                    ifAllZero = str(npall(p_ll == 0))
                    com = {'ifAllZero': ifAllZero, 'content': p_ll}
                    # print(com)
                elif i == 2:  # 2相位距离处理
                    p_ll = nparray(p.ConvertDecimal(least=24, symbol=True)).tolist()
                    ifAllZero = str(npall(p_ll == 0))
                    com = {'ifAllZero': ifAllZero, 'content': p_ll}
                elif i == 5:  # 信噪比处理
                    p_ll = nparray(p.ConvertDecimal()).tolist()
                    ifAllZero = str(npall(p_ll == 0))
                    com = {'ifAllZero': ifAllZero, 'content': p_ll}
                elif i == 6:
                    p_ll = nparray(p.ConvertDecimal(least=14, symbol=True)).tolist()
                    # print(p_ll)
                    ifAllZero = str(npall(p_ll == 0))
                    com = {'ifAllZero': ifAllZero, 'content': p_ll}
                else:
                    i += 1
                    continue
                dic[key[i]] = com
                datan = p.RestContent()
                i += 1
            i = 0
            while i < len(gnss):
                dic['精确伪距']['content'][i] = (gnss[i] + dic['精确伪距']['content'][i]) * 299792458 / 1000
                i += 1
            i = 0
            while i < len(gnss_00):
                dic['精确相位距离变化率']['content'][i] = (gnss_00[i] + dic['精确相位距离变化率']['content'][i]) * 1
                i += 1
            for i in [1, 2, 5, 6]:
                dic_result[key[i]] = dic[key[i]]
            self.dic_result = {
                'rtcm' + str(rtcmtype): dic_result
            }

        except:
            self.dic_result = {'rtcm' + str(rtcmtype) + '-error': '内容异常'}
    def result(self):
        return self.dic_result
    def __del__(self):
        pass

class RTCM1005():
    def __init__(self, data):
        try:
            ID = data[12:24]
            gnss = data[30:33] + data[73]
            self.dic_result = {
                'rtcm1005': {
                "参考站ID ": cd(ID).convertdecimal(),
                "GNSS系统": gnss_system_server(gnss)}
            }

            # return dic_result
        except:
            self.dic_result = {'rtcm1005' + '-error': '内容异常'}
    def result(self):
        return self.dic_result
    def __del__(self):
        pass
class RTCM1007():
    def __init__(self, data):
        try:
            ID = data[12:24]
            n = cr(data[24:32])
            self.dic_result = {
                'rtcm1007':{
                '参考站ID': cd(ID).convertdecimal(),
                '天线标识符': n.Getcontent()}
            }
            rdata = n.Restcontent()
            self.dic_result['rtcm1007']['天线设置序列'] = int(rdata[0:8]+'0')
            # print(dic_result)
        except:
            self.dic_result = {'rtcm1007' + '-error': '内容异常'}
    def result(self):
        return self.dic_result
    def __del__(self):
        pass

class RTCM1008():
    def __init__(self, data):
        try:
            ID = data[12:24]
            n = cr(data[24:32])
            self.dic_result = {
                'rtcm1008': {
                '参考站ID': cd(ID).convertdecimal(),
                '天线标识符': n.Getcontent()}
            }
            rdata = n.Restcontent()
            self.dic_result['天线设置序列'] = int(rdata[0:8] + '0')
            m = int(data[40+8 * n:48+8 * n])
            char2_b = data[48+8 * n:48+8 * n + 8 * m]
            char2 = bin2ascii(char2_b)
            self.dic_result['rtcm1008']['天线序列号'] = char2
        except:
            self.dic_result = {'rtcm1008' + '-error': '内容异常'}
    def result(self):
        return self.dic_result
    def __del__(self):
        pass

class RTCM1033():
    def __init__(self, data):
        try:
            ID = data[12:24]
            n = cr(data[24:32])
            self.dic_result = {
                'rtcm1033':{
                '参考站ID': cd(ID).convertdecimal(),
                '天线标识符': n.Getcontent()}
            }
            rdata = n.Restcontent()
            rdata = rdata[8:]
            self.dic_result['rtcm1033']['天线设置序列'] = int(rdata[0:8] + '0')
            li = ['天线序列号', '接收机类型', '接收机固件版本', '接收机序列号']
            for i in range(4):
                cr1 = cr(rdata)
                self.dic_result['rtcm1033'][li[i]] = cr1.Getcontent()
                rdata = cr1.Restcontent()
            # print(dic_result)
        except:
            self.dic_result = {'rtcm1033' + '-error': '内容异常'}
    def result(self):
        return self.dic_result
    def __del__(self):
        pass


