#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import requests
import json

__author__ = 'wjq'

import sys
import multiprocessing

def read(q , f):
    # file = sys.argv[1]
    with open(f) as lines:
        line = lines.readline()
        while line:
            # print('put ' + str(line))
            q.put(line)
            line = lines.readline()

def push(q):
    print('----- Start -----')
    mid = 'GM_lyyy_' + time.strftime("%Y-%m-%d") + '_11'
    url = 'http://10.103.13.33/push-api/push'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    count = 0

    s = requests.Session()

    while True:
        line = q.get(True)

        r = {}
        r['mid'] = mid
        r['pushType'] = 'GAME'
        r['key'] = 'e126f32341c79978f61c3e7fcc529883'

        q = {}
        q['type'] = 'INDIVIDUAL'
        q['apps'] = [1]
        q['guids'] = [line.split('\n')[0].split('\r')[0]]
        q['payloadType'] = '3'
        r['query'] = q

        p = {}
        pa = {}
        pa['content'] = '雷亚音游《兰空VOEZ》龙渊和优酷土豆全球重磅发行！'
        pa['title'] = '感受第三代音游的魅力！青春的激情！'
        pa['desc'] = '雷亚音游《兰空VOEZ》龙渊和优酷土豆全球重磅发行！感受第三代音游的魅力！青春的激情！'
        pa['type'] = '3'
        pa['url'] = 'http://cms.g.youku.com/mobile/20160527-voez-hd-az-1'
        pa['mid'] = mid
        p['android'] = pa
        r['payload'] = p

        try:
            # s.post(url, data=json.dumps(r), stream=False, timeout=0.2)
            print(line)
            count += 1
        except Exception as e:
            print(e.message)


if __name__ == '__main__':
    queue = multiprocessing.Manager().Queue()
    reader = multiprocessing.Process(target=read , args=(queue , 'ids.txt'))
    pool = multiprocessing.Pool()
    reader.start()
    while True:
        pool.apply_async(push , args=(queue , ))
    pool.close()
    pool.join()