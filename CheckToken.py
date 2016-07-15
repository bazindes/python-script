#!/usr/bin/env python
#coding:utf-8
__author__ = 'Administrator'

import asyncio
import asyncio_redis
import threading

server = ["10.103.28.81", "10.103.28.82", "10.103.28.85", "10.103.28.86", "10.103.28.54"]
port = [6379, 6380, 6381, 6382]
id = ''

def getId(server,port,id):
    #create Redis connection
    connection = yield from asyncio_redis.Connection.create(host = server,port = port)
    #get by id
    result = yield from connection.scan(id)
    if result :
        print(server+':'+p)
    #close connection
    connection.close()

def getEvent(server,port,id):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getId(server,port,id))

if __name__ == '__main__':
    for s in server:
        for p in port:
            t = threading.Thread(target=getEvent,args=(s,p,id))
            t.start()





