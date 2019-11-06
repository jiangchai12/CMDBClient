# Author:jiangcaiyun

from linux import systeminfo
def windows_data():
    from windows import systeminfo
    # print("plugin_api.windows_data->", systeminfo.collect())
    return systeminfo.collect()

if __name__ == "__main__":
    windows_data()
