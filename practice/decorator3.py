#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wjq'

def logDeco(text=''):
    def log(func):
        def wrapper(*args , **kw):
            print('%s begin %s' % (text , func.__name__))
            re = func(*args , **kw)
            print('%s end %s' % (text , func.__name__))
            return re
        return wrapper
    return log

@logDeco('once')
def now():
    print('2015-12-03')

now()

