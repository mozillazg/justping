# justping
通过解析 ping 命令执行结果，查找 ping 值最小的 ip/域名

## 用法
**justping.py** [*filename*] [**+**] [*ip/host*...]

### 参数
*filename* ------ 内容为一行一个 ip/域名的文件，参考 hosts.txt    
**+** ---------------- 同时比较文件内及后面输入的 ip/域名    
*ip/host* -------- ip/域名

### 示例

* 

        >python justping.py
        ######################################################
                                 host(ip)   time    lost
              baidu.com(123.125.114.144):  170ms    0%
                   qq.com(119.147.15.13):   66ms    0%
        ######################################################
        qq.com has the min ping time: 66 ms
        >

* 

        >python justping.py baidu.com 8.8.8.8
        ######################################################
                                 host(ip)   time    lost
              baidu.com(123.125.114.144):  170ms    0%
                        8.8.8.8(8.8.8.8):  124ms    0%
        ######################################################
        8.8.8.8 has the min ping time: 124 ms
        >

* 

        >python justping.py hosts.txt
        ######################################################
                                host(ip)   time    lost
               baidu.com(220.181.111.86):   81ms    0%
                   qq.com(119.147.15.13):   63ms    0%
        ######################################################
        qq.com has the min ping time: 63 ms
        >

* 

        >python justping.py hosts.txt + 8.8.8.8
        ######################################################
                                host(ip)   time    lost
               baidu.com(220.181.111.86):   81ms    0%
                   qq.com(119.147.15.13):   63ms    0%
                        8.8.8.8(8.8.8.8):  124ms    0%
        ######################################################
        qq.com has the min ping time: 63 ms
        >

