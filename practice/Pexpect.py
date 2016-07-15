#!/usr/bin/env python
# coding:utf-8
__author__ = 'wjq'

import pexpect

logwatch = ('10.103.11.151','hqNzyvKBYZ6Db6LE')
server = [('10.103.28.101', '5VMzmzpeTQna'),
          ('10.103.28.53', 'vtHhoCcqTp5o'),
          ('10.103.28.61', '0HEv27S0DnVC'),
          ('10.103.28.62', 'a5bMxno6HHns'),
          ('10.103.28.63', '9A2Pv13LvEHT'),
          ('10.103.28.64', 'vieR1DUt7WqT')]
command = 'grep \'YOUKU ANDROID_PHONE\' /opt/logs/push-api/broadcast-info.log.2015-10-15 | awk \'{print $1,$3}\' | more'

def getId(server , pwd , command):
    ssh = pexpect.spawn('ssh %s@%s' % ('wangjingqi',logwatch[0]))
    ssh.expect('Select server: ')
    ssh.sendline('3')
    ssh.expect('bash-4.1$ ')
