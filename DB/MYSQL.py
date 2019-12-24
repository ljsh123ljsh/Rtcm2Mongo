from pymysql import connect
from DB import mysql
MYSQL = connect(host=mysql['host'], port=int(mysql['port']), user=mysql['user'], password=mysql['password'], db=mysql['db'])