#!/usr/bin/env python
# coding:utf-8
__author__ = 'wjq'

import time
import threading
import paramiko

logwatch = ('10.103.11.151','hqNzyvKBYZ6Db6LE')
server = [('10.103.28.101', '5VMzmzpeTQna'),
          ('10.103.28.53', 'vtHhoCcqTp5o'),
          ('10.103.28.61', '0HEv27S0DnVC'),
          ('10.103.28.62', 'a5bMxno6HHns'),
          ('10.103.28.63', '9A2Pv13LvEHT'),
          ('10.103.28.64', 'vieR1DUt7WqT')]

order = 'grep \'YOUKU ANDROID_PHONE\' /opt/logs/push-api/broadcast-info.log.2015-11-09 | awk \'{print $1,$3}\' | more'

def getId(server, pwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(logwatch[0], 22, username='wangjingqi', password='Wjq@getLove', timeout=4)
    # stdin, stdout, stderr =
    # for std in stdout:
    #     print(server + ' : ' + std)
    # client.close()

getId(server[0][0],server[0][1])

# if __name__ == '__main__':
#     for x,y in server:
#         t = threading.Thread(target=getId, args=(x, y))
#         t.start()
