#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'wjq'

import itertools
import redis


msgidRedis = redis.StrictRedis(host='10.103.28.103',port=6379,db=4,socket_connect_timeout=20000)
countRedis = redis.StrictRedis(host='10.100.28.112',port=6379,db=2,socket_connect_timeout=20000)
deviceRedis = redis.StrictRedis(host='10.103.28.103',port=6379,db=3,socket_connect_timeout=20000)
keys =[key for key in msgidRedis.keys('2016*_YOUKU_IPHONE')]
hkeys =[msgidRedis.hkeys(hkey) for hkey in keys]
andrkey = '_1_3_-_'
miuikey = '_1_3_1_'
iphonekey = '_1_1_-_'
ipadkey = '_3_2_-_'

def makeMid(hkeys , keys):
    list = []
    for i in range(len(keys)):
        for h in hkeys[i]:
            list.append(str(keys[i] , 'utf-8')[:10] + '=' + str(h , 'utf-8'))
    return list

mids = makeMid(hkeys , keys)

def getNum(key , type):
    list = []
    for mid in mids:
        pmid = mid.split('=')
        activeKey = pmid[0].replace('-','') + key + type +'_' + pmid[1]
        n = countRedis.get(activeKey)
        if n == None :
            list.append('0')
        else:
            list.append(str(n, 'utf-8'))
    return list

def getDevice(p):
    list = []
    for mid in mids:
        list.append(str(deviceRedis.get(mid[:10].replace('-','')+p) , 'utf-8'))
        # list.append(mid[:8].replace('-','')+p)
    return list

def getMsg():
    list = []
    for mid in mids:
        p = mid.split('=')
        list.append(str(msgidRedis.hget(p[0]+'_YOUKU_IPHONE', mid[11:]),'utf-8'))
    return list

def percent(ns,ds):
    list = []
    for i in range(len(ns)):
        if ns[i] == '0' or ds[i] == '0':
            list.append(0)
        else:
            list.append(round(int(ns[i]) / int(ds[i]) , 4))
    return list


if __name__ == '__main__':
    andrRecv = getNum(andrkey , 'recv')
    andrActive = getNum(andrkey , 'active')
    andrRate = percent(andrActive,andrRecv)
    miRecv = getNum(miuikey , 'recv')
    miActive = getNum(miuikey , 'active')
    miRate = percent(miActive,miRecv)
    iphoneSend = getDevice('_1_1_')
    iphoneActive = getNum(iphonekey , 'active')
    iphoneRate = percent(iphoneActive,iphoneSend)
    ipadSend = getDevice('_3_2_')
    ipadActive = getNum(ipadkey , 'active')
    ipadRate = percent(ipadActive,ipadSend)
    msgs = getMsg()

    msg = []
    alist = []
    mlist = []
    ielist = []
    idlist = []
    numlist = []
    for i in range(len(msgs)):
        msg.append(msgs[i].split('@')[0])
        alist.append(ipadRate[i])
        mlist.append(miRate[i])
        ielist.append(iphoneRate[i])
        idlist.append(ipadRate[i])
        numlist.append(int(andrActive[i]) + int(miActive[i]) + int(iphoneActive[i]) + int(ipadActive[i]))
    print(msg)
    print(len(msg))
    print(alist)
    print(len(alist))
    print(mlist)
    print(len(mlist))
    print(ielist)
    print(len(ielist))
    print(idlist)
    print(len(idlist))
    print(numlist)
    print(len(numlist))
