#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wjq'

def count():
    def g(i):
        def f():
            return i*i
        return f

    fs = []
    for i in range(1,4):
        fs.append(g(i))
    return fs

f1,f2,f3 = count()
print(f1())
print(f2())
print(f3())
