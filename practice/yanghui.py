#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'

def triangles():
    base = [1]
    yield base
    base = [1,1]
    yield base
    while True:
        base = [1] + [ base[i]+base[i+1] for i in range(len(base) - 1)] +[1]
        yield base

n = 0
for i in triangles():
    print(i)
    n = n + 1
    if n == 10 :
        break
