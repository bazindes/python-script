#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wjq'

import os
import multiprocessing

def childrun(name):
    print('Im the child %s(%d)' % (name,os.getpid()))

if __name__ == '__main__':
    print('Parent process: %d' % os.getpid())
    p = multiprocessing.Process(target=childrun , args=('test',))
    print('child process starting')
    p.start()
    p.join()
    print('child process ended')
