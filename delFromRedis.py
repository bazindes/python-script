#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wjq'

import redis

r = redis.StrictRedis(host='',port=6379,db=0)
for key in r.scan_iter():
    r.de