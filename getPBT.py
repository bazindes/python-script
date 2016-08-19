#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wjq'

import http.client

url = '10.100.23.153'
params = 'startTime=20160815&endTime=20160815&limit=20&start=0&clientType=youku%3A%3Aandroid%2Cyouku_hd%3A%3Aandroid&itemTitle=&orderType=normal&_=1471329478201'

def getJson():
    conn = http.client.HTTPSConnection(url)
    conn.request('GET' , '/statOrderItem.do?' + params)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    while not r1.closed:
        print(r1.read(1024))


if __name__ == '__name__':
    getJson()
