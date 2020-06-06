import requests
import psutil
import os
import re


def find_procs_by_name(name):
    """Return a list of processes matching 'name'."""
    ls = []
    for p in psutil.process_iter(['name']):
        if p.info['name'] == name:
            ls.append(p)
    return ls


isAria2 = 0
isFixed = 0
if find_procs_by_name('aria2c.exe') or find_procs_by_name('aria2cP.exe'):
    if find_procs_by_name('aria2c.exe') is not None:
        pid = find_procs_by_name('aria2c.exe')[0].pid
        result = os.popen('netstat -aon|findstr ' + str(pid)).read()
        port = re.search('127\.0\.0\.1:(.{4,5})', result)
    elif find_procs_by_name('aria2cP.exe') is not None:
        pid = find_procs_by_name('aria2cP.exe')[0].pid
        result = os.popen('netstat -aon|findstr ' + str(pid)).read()
        port = re.search('127\.0\.0\.1:(.{4,5})', result)
    print('检测到 aria2，修改中')
    isAria2 = 1
    setproxy = '{"jsonrpc":2,"id":"webui","method":"system.multicall","params":[[{' \
               '"methodName":"aria2.changeGlobalOption","params":["token:pandownload",{"all-proxy":""}]}]]} '
    post = requests.post(url='http://127.0.0.1:' + str(port[1]) + '/jsonrpc', data=setproxy, timeout=0.1)
    normal_data = '{"id":"webui","jsonrpc":"2.0","result":[["OK"]]}'
    if post.text == normal_data:
        print('修改成功')
        input("\n按回车键退出...")
        isFixed = 1
if isAria2 == 0:
    print('未检测到 aria2，请打开 Pandownload')
    input("\n按回车键退出...")
else:
    if isFixed == 0:
        print('未找到 aria2 端口，请联系开发者/提 Issue')
        print('https://t.me/Ruriri')
        input("\n按回车键退出...")
