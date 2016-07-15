#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wjq'

import redis
import multiprocessing
import json

sever = [
    ('10.100.28.112' , 6379 , 0 ),
    ('10.100.28.113' , 6379 , 0 ),
    ('10.103.28.103' , 6379 , 0 )
]


def getInfo( host , port , db):
    redisPool = redis.ConnectionPool(host=host , port=port , db=db ,max_connections=10)
    r = redis.Redis(connection_pool=redisPool)
    result = json.dumps(r.info() , indent=4)
    print(result)



if __name__ == '__main__':
    for host,port,db in sever:
        process = multiprocessing.Process(target=getInfo , args=(host,port,db))
        process.start()
        process.join()
        # getInfo(host,port,db)

