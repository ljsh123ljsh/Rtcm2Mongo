from RTCM_ANALYSE import *
r = StrictRedis(connection_pool=REDIS.REDIS_pool)

class RTCM:

    def MSM4(self, data, rtcmtype):
        tt = 'rtcm' + str(rtcmtype)
        DIC = r.hgetall(tt)
        # 12bits参考站ID； 30bitsGNSS历元； 1bit多点文标志； 7bits保留位； 2bits时钟校准标志； 2bits拓展时钟标志； 1bitGNSS平滑类型标志； 3bitsGNSS平滑区间  共61bits省略
        ID = data[12:24]
        print("参考站ID = {}".format(cd(ID).convertdecimal()))
        gnss_liyuan = data[24:24+30]
        print("GNSS历元 = {}".format(cd(gnss_liyuan).convertdecimal()))
        gnss_sta = data[73:74 + 64]  # 卫星掩码64bits
        sat = Map('1', gnss_sta)
        Nsat = sat.map_amount()  # 卫星数
        # print(Nsat)
        Nsat_id = sat.map_id()
        gnss_sig = data[137:137 + 32]  # 信号掩码32bits
        sig = Map('1', gnss_sig)
        Nsig = sig.map_amount()  # 信号数
        # print(Nsig)
        Nsig_id = sig.map_id()
        # print(Nsig_id)
        # DIC = eval('rtcm'+rtcmtype)
        # print(DIC)
        # print(Nsig_id)
        Nsig_id = [loads(DIC[str.encode(str(x))])['FrequencyBand'] for x in Nsig_id]

        '''
        加入信号类型
        '''
        print("信号类型：{}".format(Nsig_id))

        X = Nsat * Nsig
        gnss_x = data[169:169 + X]  # 单元掩码X bits
        Ncell = Map('1', gnss_x).map_amount()  # 单元掩码数
        # print(Ncell)
        print("卫星数：{}; 信号数：{}; 单元数：{}".format(Nsat, Nsig, Ncell))
        # print((169+Nsat*Nsig+18*Nsat+48*Ncell)/8)

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
        i = 1
        while i <= 5:
            p = CellContent(Ncell, i)
            p.ReturnContent(datan)  # 1精确伪距,2相位距离,3相位距离锁定时间标志,4半周模糊度标志,5信噪比CNR
            p_ll = p.ConvertContent(gnss_x)  # 列表与单元掩码融合后
            if i == 1:  # 精确伪距处理
                p_ll = p.ConvertDecimal(least=24, symbol=True)
            elif i == 2:
                p_ll = p.ConvertDecimal(least=24, symbol=True)
                # print(p_ll)
            elif i == 5:  # 信噪比处理
                p_ll = p.ConvertDecimal()
            # else:
            #     i += 1
            #     continue
            dic[i] = p_ll
            datan = p.RestContent()
            i += 1

        i = 0
        while i < len(gnss):
            dic[1][i] = (gnss[i] + dic[1][i]) * 299792458 / 1000
            i += 1

        df_li = []
        no_k_list = [3, 4]
        for k in range(len(dic.keys())):
            k += 1
             # 2,3,4暂时不处理
            if k in no_k_list:
                continue
            df_sat_sig = DF(index=Nsig_id, columns=Nsat_id)

            for id_c in Nsat_id:
                i = Nsat_id.index(id_c)
                for id_i in Nsig_id:
                    j = Nsig_id.index(id_i)
                    df_sat_sig.loc[id_i, id_c] = str(dic[k][i * Nsig + j])
            df_li.append(df_sat_sig)
            # print(df_sat_sig)
        res = concat(df_li, axis=0, ignore_index=False)
        print(DF(res.T))


    def rtcm1005(self, data):
        ID = data[12:24]
        X = cd(data[34: 34+38], symbol=True).convertdecimal()/1000
        Y = cd(data[74: 74+38], symbol=True).convertdecimal()/1000
        Z = cd(data[114:114+38], symbol=True).convertdecimal()/1000
        BLH = XYZ2BLH(X, Y, Z)
        gnss = data[30:33] + data[73]
        print("参考站ID = {}".format(cd(ID).convertdecimal()))
        print("GNSS系统 = {}".format(gnss_system_server(gnss)))
        print('X = {:.4f}\nY = {:.4f}\nZ = {:.4f}'.format(X, Y, Z))
        print('B={0:.9f}\nL={1:.9f}\nH={2:.9f}'.format(BLH[0], BLH[1], BLH[2]))

    def rtcm1007(self, data):
        ID = data[12:24]
        print("参考站ID = {}".format(cd(ID).convertdecimal()))
        n = cr(data[24:32])
        print("天线标识符 = {}".format(n.Getcontent()))
        rdata = n.Restcontent()
        print("天线设置序列 = {}".format(int(rdata[0:8]+'0')))

    def rtcm1008(self, data):
        ID = data[12:24]
        print("参考站ID = {}".format(cd(ID).convertdecimal()))
        n = cr(data[24:32])
        print("天线标识符 = {}".format(n.Getcontent()))
        rdata = n.Restcontent()
        print("天线设置序列 = {}".format(int(rdata[0:8] + '0')))
        # rtcm1008
        m = int(data[40+8 * n:48+8 * n])
        char2_b = data[48+8 * n:48+8 * n + 8 * m]
        char2 = bin2ascii(char2_b)
        print("天线序列号 = {}".format(char2))

    def rtcm1033(self, data):
        ID = data[12:24]
        print("参考站ID = {}".format(cd(ID).convertdecimal()))
        n = cr(data[24:32])
        print("天线标识符 = {}".format(n.Getcontent()))
        rdata = n.Restcontent()
        print("天线设置序列 = {}".format(int(rdata[0:8]+'0')))
        rdata = rdata[8:]
        li = ['天线序列号', '接收机类型', '接收机固件版本', '接收机序列号']
        for i in range(4):
            cr1 = cr(rdata)
            print(li[i]+"= {}".format(cr1.Getcontent()))
            rdata = cr1.Restcontent()


