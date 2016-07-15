#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wjq'

from peewee import *
import datetime
from playhouse.db_url import connect
from playhouse.pool import PooledMySQLDatabase
import redis
import threading
import threadpool

sever = [
    ('10.100.28.112' , 6379 , 0 , 0),
    ('10.100.28.113' , 6379 , 0 , 1),
    ('10.103.28.103' , 6379 , 0 , 1),
    ('10.103.28.103' , 6379 , 2 , 0),
    ('10.103.28.103' , 6379 , 3 , 0)
]
db = connect('mysql://root:123456@localhost:3306/cms_dev')
# mysql = MySQLDatabase('cms_dev',True,True,None,None,False,host='localhost',port=3306,user='root',password='123456')
# db = PooledMySQLDatabase(mysql, 20 , 2000)
class Stat(Model):
    id = CharField()
    app = CharField()
    value = CharField()
    date = DateField()
    class Meta:
        database = db

def getKeys(host,port,db,pattern):
    r = redis.StrictRedis(host=host , port=port , db=db , socket_connect_timeout=2000 )
    keys = r.keys(pattern)
    print(host + ':'+ str(port) + '('+str(db)+')' + ' -> ' + str(len(keys)))

def rtm(host,port,db,pattern,pf):
    start = datetime.datetime.now().timestamp()
    r = redis.StrictRedis(host=host , port=port , db=db , socket_connect_timeout=2000 )
    keys = r.keys(pattern)
    with r.pipeline() as pipe:
        if pf == 0:
            for k in keys:
                pipe.get(k)
        else:
            for k in keys:
                pipe.pfcount(k)
        values = pipe.execute()
    middle = datetime.datetime.now().timestamp()
    print(host + ':'+ str(port) + '('+str(db)+')' + ' -> Query from redis last: ' + str(middle - start))
    result = zip(keys,values)
    for k,v in result:
        nk = str(k , 'utf-8')
        na = nk.split('_')[1]
        if len(k) > 255 :
            nk = nk[0:250]
        if len(na) > 255 :
            na = na[0:20]
        try:
            Stat.create(id=nk,app=na,value=v,date=datetime.datetime.now())
        except IntegrityError:
            Stat.create(id=(nk + 'oth'),app=na,value=v,date=datetime.datetime.now())
            continue
    finish = datetime.datetime.now().timestamp()
    print(host + ':'+ str(port) + '('+str(db)+')' + ' -> totally inserted : ' + str(len(keys)) + ' during : ' + str(finish-start))

if __name__ == '__main__':
    key = '20151123*'
    pool = threadpool.ThreadPool(8)

    # for h,p,d,pf in sever:
    #     # t = threading.Thread(target=getKeys , args=(h,p,d,key))
    #     t = threading.Thread(target=rtm , args=(h,p,d,key,pf))
    #     t.start()


