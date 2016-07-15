#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wjq'

import multiprocessing
from peewee import *
import datetime
from playhouse.pool import PooledMySQLDatabase
from playhouse.db_url import connect
import redis


sever = [
    ('10.100.28.112' , 6379 , 0 , 0),
    ('10.100.28.113' , 6379 , 0 , 1),
    ('10.103.28.103' , 6379 , 0 , 1),
    ('10.103.28.103' , 6379 , 2 , 0),
    ('10.103.28.103' , 6379 , 3 , 0)
]
db = connect('mysql://root:123456@localhost:3306/cms_dev')
# db = PooledMySQLDatabase('mysql',host='localhost',port=3306,db='cms_dev',user='root',password='123456')
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
    print(host + ':'+ str(port) + '('+str(db)+')' + ' -> Query from redis last: ' + str(middle - start) )
    result = zip(keys,values)
    list = []
    for k,v in result:
        nk = str(k , 'utf-8')
        na = nk.split('_')[1]
        if len(k) > 255 :
            nk = nk[0:250]
        if len(na) > 255 :
            na = na[0:20]
        list.append({'id':nk , 'app':na , 'value':v ,'date':datetime.datetime.now()})
    try:
        Stat.insert_many(list).execute()
    except IntegrityError as e:
        print(e)
        Stat.create(id=(nk + 'oth'),app=na,value=v,date=datetime.datetime.now())
    finish = datetime.datetime.now().timestamp()
    print(host + ':'+ str(port) + '('+str(db)+')' + ' -> totally inserted : ' + str(len(keys)) + ' during : ' + str(finish-start))

if __name__ == '__main__':
    today = datetime.datetime.now()
    print('It is ' + today.strftime('%Y-%m-%d %H:%M:%S') )
    pool = multiprocessing.Pool()
    for i in range(65):
        today = today - datetime.timedelta(days=1)
        key = today.strftime('%Y%m%d')+'*'
        for host,port,db,ispf in sever:
            pool.apply_async(rtm , args=(host,port,db ,key,ispf))
    pool.close()
    pool.join()
    print('It is ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
