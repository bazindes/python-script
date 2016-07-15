#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'wjq'

import os
import multiprocessing
import time,random
def task(name):
    print('Run task %s %d' % (name , os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s lasted %0.2f secs' % (name,(end-start)))

if __name__ == '__main__':
    print('Parent process: %d' % os.getpid())
    pool = multiprocessing.Pool()
    for i in range(5):
        pool.apply_async(task , args=(i,))
    print('waiting for all process done...')
    pool.close()
    pool.join()
    print('all processes done')