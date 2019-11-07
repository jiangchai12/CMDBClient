__author__ = 'jiangcaiyun'
# coding=utf-8
from core import info_collection
from conf import setting
import json, urllib, urllib2, sys

class ArgvHanddler(object):
    def __init__(self, Argvs):
        self.argv = Argvs
        self.parse_argv()

    def parse_argv(self):
        if len(self.argv) > 1:
            if hasattr(self, self.argv[1]):
                func = getattr(self, self.argv[1])
                func()
            else:
                self.help_msg()
        else:
            self.help_msg()

    def help_msg(self):
        msg = """
        collet_assets
        run_forever
        get_asset_id
        report_asset
        """
        print(msg)

    def collect_assets(self):
        data_obj = info_collection.InfoCollection()
        asset_data = data_obj.collection()

        return asset_data

    def package_asset_data(self):
        object = info_collection.InfoCollection()
        asset_info = object.collection()
        packa_data = {"asset_data": json.dumps(asset_info)}
        return packa_data

    def get_asset_id(self):
        data_obj = info_collection.InfoCollection()
        asset_data = data_obj.collection()
        asset_id = asset_data["sn"]
        print(asset_id)
        return asset_id
    def get_url(self):
        ip = setting.Params["server"]
        port = setting.Params["port"]
        path = setting.Params["urls"]["asset_report_with_no_id"]
        if type(port) is int:
            url = "http://%s:%s%s" % (ip, port, path)
        else:
            url = "http://%s%s" % (ip, path)
        # print(url)
        return url

    def report_asset(self):
        asset_data = self.package_asset_data()
        # print("report_asset.asset_data -->", asset_data)
        urls = self.get_url()
        self.__submit_data(asset_data, urls, method="post")

    def __submit_data(self, asset_data, urls, method):
        data = ''
        if method == "get":
            for k, v in asset_data.items():
                data += "%s=%s" % (k, v)
            data = data[0:]
            # print("__submit_data.data -->", data)
            url_with_data = "%s?%s" % (urls, data)
            try:
                timeout = setting.Params["request_timeout"]
                req = urllib2.Request(url_with_data)
                print("url_with_data=", url_with_data)
                req_data = urllib2.urlopen(req, timeout=timeout)
                callback = req_data.read()
                print("server_response-->", callback)
                return callback
            except Exception as e:
                sys.exit("\033[31;m1%s\033[0m" % e)
        elif method == "post":
            try:
                data_encode = urllib.urlencode(data)
                timeout = setting.Params["request_timeout"]
                print(data_encode)
                req = urllib2.Request(url=urls, data=data_encode)
                req_data = urllib2.urlopen(req, timeout=timeout)
                callback = req_data.read()
                print(callback)
                return callback
            except Exception as e:
                # sys.exit("\033[31;m1%s\033[0m" % e)
                print(e)





    def run_forever(self):
        print("Does not support run_forever!")

if __name__ == "__main__":
    object = ArgvHanddler("ddddd")
    # object.collect_assets()
    # object.get_asset_id()
    # object.help_msg()
    # object.get_url()
    object.report_asset()