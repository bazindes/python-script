#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'

import redis

host = '10.100.28.112'
port = 6379
db = 2

r = redis.StrictRedis(host=host , port=port , db=db , socket_connect_timeout=2000 )
keys = r.keys('20160116_3_2*active*BT_361887989_149824@149824*')
#keys = r.keys('20160116_3_2*active*BT_361630389_149800@149800*')
#keys = r.keys('20160118_3_2*active*BT_362116972_150453@150453*')
sum = 0

for key in keys:
    b = r.get(str(key , 'utf-8'))
    sum += int(str(b,'utf-8'))
    print(str(key , 'utf-8') + ' : ' + str( b , 'utf-8'))

print('sum : ' + str(sum))
