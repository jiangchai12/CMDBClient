# Author:jiangcaiyun

from linux import systeminfo
def windows_data():
    from windows import systeminfo
    print(systeminfo.collect())
    return systeminfo.collect()

