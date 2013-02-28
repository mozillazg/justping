#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""通过 ping 命令找出响应时间最短的 ip 或域名
支持 windows，unix，linux
"""

import re
import os
import subprocess
import sys


def ping(host):
    """返回 ping 结果

    host 参数应为字符串类型的 ip 或域名
        '192.168.1.1' or 'www.baidu.com'

    返回 host, ip, time, lost
        host：域名或 ip，字符串类型
        ip：ip 地址，字符串类型，默认值为'0.0.0.0'
        time：平均响应时间（ms），int 类型，默认值为0
        lost：平均丢包率（%），int 类型，默认值为0

    返回值示例：
        ('baidu.com', '123.125.114.144', 70, 0)
    """
    os_name = os.name
    # 根据系统平台设置 ping 命令
    if os_name == 'nt':  # windows
        cmd = 'ping ' + host
    else:  # unix/linux
        cmd = 'ping -c 4 ' + host

    # 执行 ping 命令
    sub = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, shell=True)
    out = sub.communicate()[0]
    if not out:
        return host, '0.0.0.0', 0, 100

    # 替换换行符，因为在正则表达式中
    # 'a$' 匹配 'a\r\n' 中的 'a\r'
    text = out.replace('\r\n', '\n').replace('\r', '\n')

    # 使用正则匹配 ip 地址: [192.168.1.1] (192.168.1.1)
    ip = re.findall(r'(?<=\(|\[)\d+\.\d+\.\d+\.\d+(?=\)|\])', text)

    # 获取时间信息
    if os_name == 'nt':
        time = re.findall(r'\d+(?=ms$)', text)
    else:
        time = re.findall(r'(?<=\d/)[\d\.]+(?=/)', text)

    # 丢包率
    lost = re.findall(r'\d+(?=%)', text)

    ip = ip[0] if ip else '0.0.0.0'

    # 小数点四舍五入
    time = int(round(float(time[0]))) if time else 0
    lost = int(round(float(lost[0]))) if lost else 0

    return host, ip, time, lost


def get_hosts(filename):
    """从文件中读取 ip/域名
    返回 ip/域名 列表，默认值为空
    """
    hosts = []
    with open(filename) as f:
        for line in f:
            line = line.strip().strip('.,/')
            if line:
                hosts.append(line)
    return hosts

if __name__ == '__main__':
    # 处理命令行参数
    argvs = sys.argv
    leng = len(argvs)
    hosts = []
    filename = 'hosts.txt'
    add = False
    ips = []

    #  如果包含命令参数
    if leng >= 2:
        name = argvs[1]

        # 第一个参数是个文件
        if os.path.isfile(name):
            filename = name

            if leng > 2:
                # 第二个参数是 +
                if argvs[2] == '+':
                    add = True
                    ips = argvs[3:]
                else:
                    ips = argvs[2:]
        else:
            if name == '+':
                add = True
                ips = argvs[2:]
            else:
                ips = argvs[1:]
        # 处理 ip/域名参数
        if ips:
            for s in ips:
                name = s.strip('.,/')
                name = re.sub(r'https?://', '', name)
                hosts.append(name)

    # 既没有 ip/域名参数，也没有文件参数同时默认文件也不存在
    if not hosts and not os.path.isfile(filename):
        sys.exit('No ip/host or the file("%s") not existed!' % (filename))

    if not hosts:  # 如果没有参数，使用默认文件
        # 移除重复项
        hosts = list(set(get_hosts(filename)))
    else:
        hosts = list(set(hosts))
        # 如果包含 + 参数，合并 ip/域名信息
        if add:
            hosts = list(set(get_hosts(filename) + hosts))

    if not hosts:  # 如果最终都没获取到 ip/域名 信息
        sys.exit('Not find ip/host')

    result_time = {}

    print '#' * 55
    # 固定字符串长度
    print 'host(ip)'.rjust(33), 'time'.rjust(8), 'lost'.rjust(8)

    for x in hosts:
        host, ip, time, lost = ping(x)
        result_time.update({host: time})
        if time == 0:
            lost = 100
        print ('%s(%s): ' % (host, ip)).rjust(35),\
              ('% 3sms' % (time)).rjust(6),\
              ('% 2s%%' % (lost)).rjust(8)

    times = sorted(result_time.itervalues())
    # 去除 time 为0的
    times = [i for i in times[:] if i]

    print '#' * 55
    if times:
        for k, v in result_time.iteritems():
            if v == times[0]:
                print '%s has min ping time: %s ms' % (k, v)
