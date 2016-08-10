#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'

import redis
import datetime

def getDate():
    start = datetime.datetime(2016,7,27)
    end = datetime.datetime(2016,8,8)
    return [i.strftime('%Y-%m-%d') for i in (start + datetime.timedelta(n) for n in range((end - start).days + 1))]

def add(x,y):
    return x+y
def repl(x):
    return x.replace('-','')
def utf_8(x):
    return [str(y,'utf-8') for y in x]

keys = getDate()

hosts = [('10.100.28.112' , 2),('10.100.28.113' , 0),('10.103.28.103' , 4),('10.103.28.103' , 3),('10.100.28.112' , 0)]

def getMi():
    miSend = redis.StrictRedis(host=hosts[4][0],port=6379, db=hosts[4][1], socket_connect_timeout=2000)
    miSendUV = redis.StrictRedis(host=hosts[1][0],port=6379, db=hosts[1][1], socket_connect_timeout=2000)
    nk = [k+'_1_3_1_*_send*' for k in list(map(repl, keys))]
    misKeys = [miSend.keys(k) for k in nk]
    mis = [miSend.get(s) for k in misKeys for s in k]
    misuvKeys = [miSendUV.keys(k) for k in nk]
    misuv = [miSendUV.pfcount(s) for k in misuvKeys for s in k]
    re = [str(x,'utf-8')+':'+str(y,'utf-8') for x,y in list(zip([s for k in misKeys for s in k] , mis))]
    reuv = [str(x,'utf-8')+':'+str(y) for x,y in list(zip([s for k in misuvKeys for s in k] , misuv))]
    return list(zip(re,reuv))

def getAndroidSend():
    msgid = redis.StrictRedis(host=hosts[0][0], port=6379, db=hosts[0][1], socket_connect_timeout=2000)
    bkeys = []
    for b in getBroadcastNum():
        if (len(b) == 0):
            bkeys.append(['_1_3_-_send_null'])
        else:
            bkeys.append(['_1_3_-_send_' + str(k, 'utf-8') for k in b])
    akeys = []
    nk = list(map(repl,keys))
    for i in range(len(bkeys)):
        nb = []
        for j in bkeys[i]:
            nb.append(nk[i] + j)
        akeys.append(nb)
    asend = []
    for a in akeys:
        asend.append([msgid.get(k) for k in a])
    num = []
    for m in asend:
        a = 0
        for n in m:
            if n != None:
                a = str(n, 'utf-8')
        num.append(a)
    return akeys

def getIpadUV():
    device = redis.StrictRedis(host=hosts[3][0], port=6379, db=hosts[3][1], socket_connect_timeout=2000)
    return [str(device.get(ad), 'utf-8') for ad in [k + '_3_2_' for k in list(map(repl, keys))]]

def getIphoneUV():
    device = redis.StrictRedis(host=hosts[3][0], port=6379, db=hosts[3][1], socket_connect_timeout=2000)
    return [str(device.get(ad), 'utf-8') for ad in [k + '_1_1_' for k in list(map(repl, keys))]]

def getMqttUV():
    device = redis.StrictRedis(host=hosts[3][0] , port=6379 , db=hosts[3][1] , socket_connect_timeout=2000)
    return [str(device.get(ad),'utf-8') for ad in [k+'_1_3_' for k in list(map(repl,keys))]]

def getMiNum():
    msgid = redis.StrictRedis(host=hosts[0][0] , port=6379 , db=hosts[0][1] , socket_connect_timeout=2000 )
    bkeys = []
    for b in getBroadcastNum():
        if(len(b) == 0):
            bkeys.append(['_1_3_1_send_null'])
        else:
            bkeys.append(['_1_3_1_send_'+str(k,'utf-8') for k in b])
    mkeys = []
    nk = list(map(repl,keys))
    for i in range(len(bkeys)):
        nb = []
        for j in bkeys[i]:
            nb.append(nk[i] + j)
        mkeys.append(nb)
    mi = []
    for mk in mkeys:
        mi.append([msgid.get(k) for k in mk])
    num = []
    for m in mi:
        a = 0
        for n in m:
            if n != None:
                a = str(n,'utf-8')
        num.append(a)
    return num



def getBroadcastNum():
    broadcast = redis.StrictRedis(host=hosts[2][0] , port=6379 , db=hosts[2][1] , socket_connect_timeout=2000 )
    bkeys = [i+'_YOUKU_IPHONE' for i in keys]
    return [list(broadcast.hgetall(k).keys()) for k in bkeys]



if __name__ == '__main__':
    lens = [len(i) for i in getBroadcastNum()]
    miNum = [int(i) for i in getMiNum()]
    mqttNum =[int(i) for i in getMqttUV()]
    ipadNum = [int(i) for i in getIpadUV()]
    iphoneNum = [int(i) for i in getIphoneUV()]
    andr = list(zip(miNum,mqttNum))
    lastMi = ''
    sums = []
    for x in range(len(andr)):
        sum = 0
        if andr[x][0] == 0:
            sum = int(andr[x-1][0]) + int(andr[x][1])
        else:
            sum = int(andr[x][0]) + int(andr[x][1])
        sums.append(sum)
    miSend = [an[0]*an[1]for an in list(zip( miNum, lens))]
    mqttSend = [an[0]*an[1]for an in list(zip( mqttNum, lens))]
    iphSend = [an[0]*an[1]for an in list(zip( iphoneNum , lens))]
    ipdSend = [an[0]*an[1]for an in list(zip(ipadNum, lens))]
    misu = getMi()

    # print(miNum)
    # print(miSend)
    # print(mqttNum)
    # print(mqttSend)
    # print(iphoneNum)
    # print(iphSend)
    # print(ipadNum)
    # print(ipdSend)
    for mi in misu:
        print(mi)