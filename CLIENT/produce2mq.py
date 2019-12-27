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


async def rabbit(message):
    channel.basic_publish(exchange=ex, routing_key=routing_key, body=message)



async def connect_cors():
    connect = asyncio.open_connection(host, port)
    reader, writer = await connect
    EncryptionStr = b64encode(str.encode(user + ':' + password))
    header = 'GET /' + mountpoint + ' HTTP/1.1\r\nUser-Agent: NTRIP ZHDGPS\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + bytes.decode(
        EncryptionStr) + '\r\n\r\n'
    writer.write(header.encode())
    await writer.drain()
    line = await reader.readline()
    # print(line)
    if line == b'ICY 200 OK\r\n':
        # print(line)
        hhddss = time.strftime('%H%M%S', time.localtime(time.time()))
        hhddss = int(hhddss) - 80000
        if hhddss < 0:
            hhddss = hhddss + 120000
        GGA, No = next(genGGA(hhddss))
        # 获取不同时间段的GGA，并转换为字节流
        GGA = str.encode(GGA)
        i = 1
        while i:
            # 发送GGA，方法同Socket.sendall(GGA)
            print(GGA)
            i += 1

            writer.write(GGA)
            await writer.drain()
            Msg = await reader.read(1500)
            Msg = b2a_hex(Msg).decode('utf-8')
            print(Msg)
            # 打印差分数据，根据需要选择是否屏蔽
            await rabbit(Msg)
            await asyncio.sleep(1)
    else :
        print(line)


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

    channel = RABBITMQ.RABBITMQ
    ex = RABBITMQ.exchange
    channel.exchange_declare(exchange=ex, exchange_type='topic', durable=True)
    routing_key = 'data.msm'

    frequency = int(cf.get('client', 'frequency'))

    task = [connect_cors() for i in range(simulator_number)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(task))
