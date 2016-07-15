#!/usr/bin/env python
#coding:utf-8
__author__='wjq'

import paramiko
import multiprocessing
import time

user = ('wangjingqi','getToefl!100')
logwatch = ('10.103.11.151', 'logwatch' , 'hqNzyvKBYZ6Db6LE')
pushApi = ['10.103.28.101','10.103.28.53','10.103.28.61','10.103.28.62','10.103.28.63','10.103.28.64']
pushEngine = ['10.103.28.41','10.103.28.42','10.103.28.43','10.103.28.44','10.103.28.45','10.103.28.46','10.103.28.47','10.103.28.48']

cmd = ['grep \'YOUKU ANDROID_PHONE\' /opt/logs/push-api/broadcast-info.log.2016-07-14 | awk \'{print $1,$2,$3}\' | more\n' ,]

def getClient(s , cmd , q):
    try:
        client = paramiko.Transport((logwatch[0] , 22))
        client.connect(username=user[0] , password=user[1])
        channel = client.open_session()
        channel.setblocking(1)
        channel.settimeout(None)
        channel.get_pty(width=200)
        channel.invoke_shell()
        time.sleep(1)
        result = ''
        while channel.recv_ready():
            channel.recv(65535)
        else:
            channel.send('\n')
            time.sleep(1)
            channel.send('3\n')
            time.sleep(1)
            while channel.recv_ready():
                channel.recv(65535)
            else:
                channel.send('ssh ' + logwatch[1] + '@' + s + '\n')
                time.sleep(1)
                while channel.recv_ready():
                    channel.recv(65535)
                else:
                    channel.send(logwatch[2] + '\n')
                    time.sleep(1)
                    while channel.recv_ready():
                        channel.recv(65535)
                    else:
                        for c in cmd:
                            channel.send(c)
                            time.sleep(1)
                            while channel.recv_ready():
                                result += str(channel.recv(65535) , 'utf-8')
        rs = result.split('\n')
        for r in rs:
            if r.startswith('2016'):
            # if r.startswith('2016-07-11 21'):
                # print(r)
                q.put(r)
    except BaseException as e:
        print(e)
        pass


def lessonQ(q):
    while True:
        msg = q.get(True)
        print('From Queue: ' + msg)
        c = "grep " + msg[24:len(msg) - 1] +" /opt/logs/mi-push-engine/mi-push-engine.log."\
            + msg[:10] + "-"\
            + msg[11:13]\
            + "\n"
        for en in pushEngine:
            enp = multiprocessing.Process(target=getMiBroadcastId , args=(en , c))
            enp.start()

def getMiBroadcastId(engine , cmd):
    try:
        client = paramiko.Transport((logwatch[0] , 22))
        client.connect(username=user[0] , password=user[1])
        channel = client.open_session()
        channel.setblocking(1)
        channel.settimeout(None)
        channel.get_pty(width=200)
        channel.invoke_shell()
        time.sleep(2)
        result = ''
        while channel.recv_ready():
            channel.recv(65535)
        else:
            channel.send('\n')
            time.sleep(2)
            channel.send('3\n')
            time.sleep(2)
            while channel.recv_ready():
                channel.recv(65535)
            else:
                channel.send('ssh ' + logwatch[1] + '@' + engine + '\n')
                time.sleep(2)
                while channel.recv_ready():
                    channel.recv(65535)
                else:
                    channel.send(logwatch[2] + '\n')
                    time.sleep(2)
                    while channel.recv_ready():
                        channel.recv(65535)
                    else:
                        channel.send(cmd)
                        time.sleep(3)
                        while channel.recv_ready():
                            result += str(channel.recv(65535) , 'utf-8')
        print(result)
    except BaseException as e:
        print(e)
        pass



if __name__ == '__main__':
    q = multiprocessing.Manager().Queue()
    enp = multiprocessing.Process(target=lessonQ , args=(q,))
    enp.start()
    pool = multiprocessing.Pool()
    for pa in pushApi:
        pool.apply(getClient , args=(pa , cmd , q))
    pool.close()
    pool.join()
    # enp.terminate()
