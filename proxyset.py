import requests
import psutil


def find_procs_by_name(name):
    """Return a list of processes matching 'name'."""
    ls = []
    for p in psutil.process_iter(['name']):
        if p.info['name'] == name:
            ls.append(p)
    return ls


pids = psutil.pids()
isAria2 = 0
isFixed = 0
if find_procs_by_name('aria2c.exe'):
    print('检测到 aria2，修改中（需要1-2分钟，请稍候）')
    isAria2 = 1
    for i in range(36800, 37000):
        setproxy = '{"jsonrpc":2,"id":"webui","method":"system.multicall","params":[[{' \
                   '"methodName":"aria2.changeGlobalOption","params":["token:pandownload",{"all-proxy":""}]}]]} '
        try:
            post = requests.post(url='http://127.0.0.1:' + str(i) + '/jsonrpc', data=setproxy, timeout=0.1)
        except requests.exceptions.RequestException:
            continue
        normal_data = '{"id":"webui","jsonrpc":"2.0","result":[["OK"]]}'
        if post.text == normal_data:
            print('修改成功')
            input("\n按回车键退出...")
            isFixed = 1
            break
if isAria2 == 0:
    print('未检测到 aria2，请打开 Pandownload')
    input("\n按回车键退出...")
else:
    if isFixed == 0:
        print('未找到 aria2 端口，请联系开发者/提 Issue')
        print('https://t.me/Ruriri')
        input("\n按回车键退出...")
