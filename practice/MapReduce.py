#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'

from functools import reduce

def name(l):
    return list(map(change,l))

def change(name):
    return name[0].upper()+name[1:].lower()

L = ['liSa','ADam','baRt']
result = name(L)
print(result)

def qiuji(x,y):
    return x*y

def prdu(l):
    return reduce(qiuji,l)

L2 = [1,2,3,4,5]
result2 = prdu(L2)
print(result2)


def charToNum(s):
    st = s.split('.')


