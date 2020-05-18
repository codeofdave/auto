#!/usr/bin/python3
import os,time
s = os.popen('uname -ra;arch')
useradd -m HwHiAiUser -p Huawei@123 -s /bin/bash
#
# cp -a /etc/apt/sources.list /etc/apt/sources.list.bak
# wget -O /etc/apt/sources.list https://mirrors.huaweicloud.com/repository/conf/Ubuntu-Ports-bionic.list
# apt-get update

print(s.readlines())
