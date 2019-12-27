from CLIENT import *


def genGGA(hhddss):
    B0 = 3107.67923534
    L0 = 12131.54812367
    i = 1
    while i:
        B = round(B0 + random() * locaion_range * choice([1, -1]), 7)
        L = round(L0 + random() * locaion_range * choice([1, -1]), 7)
        GGA = '$GPGGA,' + str(hhddss) + ',' + str(B) + ',N,' + str(L) + ',E,1,24,0.6,43.580,M,-6.251,M,,*47'
        yield GGA, i


async def rabbit(Msg):
    channel.basic_publish(exchange=ex, routing_key='cc', body=Msg)

async def login():
    connect = asyncio.open_connection(host, port)
    reader, writer = await connect
    EncryptionStr = b64encode(str.encode(user + ':' + password))
    header = 'GET /' + mountpoint + ' HTTP/1.1\r\nUser-Agent: NTRIP ZHDGPS\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + bytes.decode(
        EncryptionStr) + '\r\n\r\n'
    writer.write(header.encode())
    await writer.drain()
    line = await reader.readline()
    hhddss = time.strftime('%H%M%S', time.localtime(time.time()))
    hhddss = int(hhddss) - 80000
    if hhddss < 0:
        hhddss = hhddss + 120000
    GGA, No = next(genGGA(hhddss))
    # 获取不同时间段的GGA，并转换为字节流
    GGA = str.encode(GGA)
    # print(line)
    if line == b'ICY 200 OK\r\n':
        i = 1
        while i:
            # 发送GGA，方法同Socket.sendall(GGA)
            print(GGA)
            i += 1
            if writer.is_closing():
                await login()
            try:
                writer.write(GGA)
                await writer.drain()
            except:
                pass
            Msg = await reader.read(1500)
            Msg = b2a_hex(Msg).decode('utf-8')
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
                        print("——" * 50)
                        break
                    # analyse(data)
                    try:
                        analyse(data)
                    except KeyError:
                        load2redis.main()
                    except:
                        continue
            # await rabbit(Msg)
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

    channel = RABBITMQ.RABBITMQ
    ex = RABBITMQ.exchange
    channel.exchange_declare(exchange=ex, exchange_type='topic')
    routing_key = 'data.msm'

    frequency = int(cf.get('client', 'frequency'))

    task = [login() for i in range(simulator_number)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(task))