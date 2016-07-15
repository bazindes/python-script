#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wjq'

import functools

def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args , **kw):
            print('%s %s()' % (text , func.__name__))
            return func(*args , **kw)
        return wrapper
    return decorator

@log('execute')
def now():
    print('2015-12-03')

now()
print(now.__name__)

