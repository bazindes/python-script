#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wjq'

import paramiko
import time
import threading

cmd = "grep 'YOUKU ANDROID_PHONE' /opt/logs/push-api/broadcast-info.log.2015-11-09 | awk '{print $1,$3}' | more"
server = ['10.103.28.101',
          '10.103.28.53',
          '10.103.28.61',
          '10.103.28.62',
          '10.103.28.63',
          '10.103.28.64']

def getID(server,cmd):
    client = paramiko.Transport(('10.103.11.151',22))
    client.connect(username='wangjingqi',password='Wjq@getLove')
    channel = client.open_session()
    channel.settimeout(5)
    channel.get_pty(width=150)
    channel.invoke_shell()
    time.sleep(3)
    channel.send('3\n')
    time.sleep(2)
    channel.send('ssh logwatch@'+server+'\n')
    time.sleep(2)
    channel.send('hqNzyvKBYZ6Db6LE\n')
    time.sleep(2)
    channel.send(cmd + '\n')
    try:
        c = ''
        while True:
            c += str(channel.recv(65535),'utf-8')
    except BaseException as e:
        pass
    finally:
        print(server +' --------------- Start:\n ' + c[900:] + '\n' + server +' --------------- Over:\n ')
        channel.close()

if __name__ == '__main__':
    for x in server:
        t = threading.Thread(target=getID,args=(x,cmd))
        t.start()
