import pika
from DB import rabbitmq
pika.ConnectionParameters(host=rabbitmq['host'], port=int(rabbitmq['port']), heartbeat=0)
RABBITMQ = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq['host'], port=int(rabbitmq['port']), credentials=pika.PlainCredentials(password=rabbitmq['password'], username=rabbitmq['user']))).channel()
exchange = rabbitmq['exchange']
queue = rabbitmq['queue']