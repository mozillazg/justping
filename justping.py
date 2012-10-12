#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""通过 ping 命令找出连接时间最短的 ip 或域名
"""

import subprocess

def ping(host):
    """host like:
    192.168.1.1 or www.baidu.com
    """
    import re

    cmd = 'ping ' + host
    sub = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out = sub.communicate()[0]
    text = out.replace('\r\n', '\n')
    ip = '0.0.0.0'
    lost = time = 0
    try:
        ip = re.search(r'^\d+\.\d+\.\d+\.\d+\b', text, re.M).group()
        time = int(re.search(r'\d+(?=ms$)', text).group())
        lost = int(re.search(r'\d+(?=%)', text).group())
    except:
        pass
    return host, ip, time, lost

def get_hosts(filename):
    """get hosts from file
    """
    hosts = list()
    with open(filename) as f:
        for line in  f:
            line = line.strip()
            if line:
                hosts.append(line)
    return hosts

if __name__ == '__main__':
    filename = 'hosts.txt'
    hosts = get_hosts(filename)
    result_time = dict()
    print '#' * 50
    print 'host(ip)'.rjust(30), 'time    lost'.rjust(14)
    for x in hosts:
        host, ip, time, lost = ping(x)
        result_time.update({host:time})
        print ('%s(%s): ' % (host, ip)).rjust(32), ('% 3sms   % 2s%%') % (time, lost)
    times = sorted(result_time.itervalues())
    times = [i for i in times[:] if i]
    print '#' * 50
    if times:
        for k, v in result_time.iteritems():
            if v == times[0]:
                print '%s has the min ping time: %s ms' % (k, v)
    raw_input('>')
