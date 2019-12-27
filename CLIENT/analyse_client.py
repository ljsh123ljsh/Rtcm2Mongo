from CLIENT import *

'''
模拟 + 解析
'''

async def connect_cors():
    k = 1
    while k:
        connect = asyncio.open_connection(host, port)
        reader, writer = await connect
        EncryptionStr = b64encode(str.encode(user + ':' + password))
        header = 'GET /' + mountpoint + ' HTTP/1.1\r\nUser-Agent: NTRIP ZHDGPS\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + bytes.decode(EncryptionStr) + '\r\n\r\n'
        print(header)
        writer.write(header.encode())
        await writer.drain()
        line = await reader.readline()
        print(line)
        k += 1
        if line == b'ICY 200 OK\r\n':
            while 1:
                # 获取不同时间段的GGA，并转换为字节流
                a = time.strftime('%H%M%S', time.localtime(time.time()))
                a = int(a)-80000
                if a < 0:
                    a = a+120000
                # 随机位置
                B = round(3114.67923534 + random()*locaion_range*choice([1, -1]), 7)
                L = round(12135.54812367 + random()*locaion_range*choice([1, -1]), 7)
                GGA = '$GPGGA,' + str(a) + ','+str(B)+',N,'+str(L)+',E,1,24,0.6,43.580,M,-6.251,M,,*47'
                print(GGA)
                GGA = str.encode(GGA)
                # 发送GGA，方法同Socket.sendall(GGA)
                writer.write(GGA)
                await writer.drain()
                # 接收差分数据
                Msg = await reader.read(1400)
                Msg = b2a_hex(Msg).decode('utf-8')
                # 打印差分数据，根据需要选择是否屏蔽
                # 解算差分
                print(Msg)
                if ifThread == 1:
                    print("多线程")
                    # analyseWholeFrame(Msg)
                    try:
                        analyseWholeFrame(Msg)
                    except KeyError:
                        load2redis.main()
                    finally:
                        analyseWholeFrame(Msg)
                else:
                    print("单线程")
                    gen = map_d30(Msg)
                    while 1:
                        try:
                            data = next(gen)
                        except StopIteration:
                            print("——" * 30)
                            print('COMPLETE')
                            print("——"*50)
                            break
                        # analyse(data)
                        try:
                             analyse(data)
                        except KeyError:
                             load2redis.main()
                        except:
                            continue
                    # 解算完成

                await asyncio.sleep(1)


if __name__ == '__main__':
    conf_path = join(abspath(dirname(dirname(__file__))), 'conf.ini')
    print(conf_path)
    cf = ConfigParser()
    try:
        cf.read(conf_path, encoding='ANSI')
    except:
        cf.read(conf_path)
    host = cf.get('ntripcaster', 'IP')
    print(host)
    port = int(cf.get('ntripcaster', 'port'))
    user = cf.get('ntripcaster', 'user')
    password = cf.get('ntripcaster', 'password')
    mountpoint = cf.get('ntripcaster', 'mountpoint')
    locaion_range = float(cf.get('client', 'range'))
    simulator_number = int(cf.get('client', 'clientnumber'))
    ifThread = int(cf.get('ntripcaster', 'ifthread'))
    task = [connect_cors() for i in range(simulator_number)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(task))