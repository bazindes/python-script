#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = 'wjq'

import multiprocessing
import redis

sever = [
    ('10.100.28.112' , 6379 , 0 ),
    ('10.100.28.113' , 6379 , 0 ),
    ('10.103.28.103' , 6379 , 0 ),
    ('10.103.28.103' , 6379 , 2 ),
    ('10.103.28.103' , 6379 , 3 )
]

def getKeys(queue):
    for h,p,d in sever:
        r = redis.StrictRedis(host=h , port=p , db=d , socket_connect_timeout=2000 )
        keys = r.keys('*')
        print('%s:%d(%d) -> keys:%d' % (h,p,d,len(keys)))
        queue.put(len(keys))

def calculate(queue):
    num = 0
    while True:
        num += queue.get(True)
        print('%d' % num)

if __name__ == '__main__':
    q = multiprocessing.Queue()
    writer = multiprocessing.Process(target=getKeys , args=(q,))
    reader = multiprocessing.Process(target=calculate , args=(q,))

    writer.start()
    reader.start()

    writer.join()
    reader.join()

