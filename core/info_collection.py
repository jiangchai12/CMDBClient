__author__ = 'jiangcaiyun'
from  plugins import plugin_api
class InfoCollection(object):
    def __init__(self):
        pass

    def collection(self):
        win_data = plugin_api.windows_data()
        # print("info_collection.InfoCollection.collection->", win_data)
        return win_data

if __name__ == "__main__":
    obj = InfoCollection()
    obj.collection()