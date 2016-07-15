#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Administrator'

def fib(max):
    i,j,k = 0,0,1
    for i in range(max):
        yield k
        j,k = k,j+k
    return 'over'

for n in fib(10):
    print(n)