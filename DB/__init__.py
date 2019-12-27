from configparser import ConfigParser
from os import path
conf_path = path.join(path.abspath(path.dirname(path.dirname(__file__))), 'conf.ini')
cf = ConfigParser()
try:
    cf.read(conf_path, encoding='ANSI')
except:
    cf.read(conf_path)

rabbitmq = {
    'host': cf.get('rabbitmq', 'host'),
    'port': cf.get('rabbitmq', 'port'),
    'user': cf.get('rabbitmq', 'user'),
    'password': cf.get('rabbitmq', 'password'),
    'exchange': cf.get('rabbitmq', 'exchange'),
    'queue': cf.get('rabbitmq', 'queue')
}

mysql = {
    'host': cf.get('mysql', 'host'),
    'port': cf.get('mysql', 'port'),
    'user': cf.get('mysql', 'user'),
    'password': cf.get('mysql', 'password'),
    'db': cf.get('mysql', 'db')
}
redis = {
    'host': cf.get('redis', 'host'),
    'port': cf.get('redis', 'port'),
    'password': cf.get('redis', 'password'),
    'db': cf.get('redis', 'db')
}

mongo = {
    'host': cf.get('mongo', 'host'),
    'port': cf.get('mongo', 'port'),
}
