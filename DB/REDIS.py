from redis import ConnectionPool
from DB import redis
REDIS_pool = ConnectionPool(host=redis['host'], port=int(redis['port']), password=redis['password'], db=redis['db'])