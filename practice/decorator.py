#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wjq'

import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s()' % func.__name__)
        return func(*args , **kw)
    return wrapper

@log
def now():
    print('2015-12-03')

now()
print(now.__name__)
