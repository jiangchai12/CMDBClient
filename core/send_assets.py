__author__ = 'jiangcaiyun'
# coding=utf-8
from core import info_collection
from conf import setting
import json, urllib, urllib2, sys, os

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
        print(asset_data)

    def get_asset_id(self):
        asset_id = self.load_asset_id()
        if asset_id:
            print("asset_id = ", asset_id)
        else:
            data_obj = info_collection.InfoCollection()
            asset_data = data_obj.collection()
            sn = asset_data["sn"]
            print("======not save asset_id=======")
            print "sn is ", sn

    def get_url(self,action_type):
        ip = setting.Params["server"]
        port = setting.Params["port"]
        path = setting.Params["urls"][action_type]
        if type(port) is int:
            url = "http://%s:%s%s" % (ip, port, path)
        else:
            url = "http://%s%s" % (ip, path)
        # print(url)
        return url

    def load_asset_id(self):
        asset_id_file = setting.Params['asset_id']
        if os.path.isfile(asset_id_file):
            asset_id = open(asset_id_file).read()
            if asset_id.isdigit():
                return asset_id
        else:
            asset_id = None


    def __submit_data(self, asset_data, action_type, method):
        if method == "get":
            data = ''
            for k, v in asset_data.items():
                data += "%s=%s" % (k, v)
            data = data[0:]
            # print("__submit_data.data -->", data)
            urls = self.get_url(action_type)
            url_with_data = "%s?%s" % (urls, data)
            try:
                timeout = setting.Params["request_timeout"]
                req = urllib2.Request(url_with_data)
                # print("url_with_data=", url_with_data)
                req_data = urllib2.urlopen(req, timeout=timeout)
                callback = req_data.read()
                print("server_response-->", callback)
                return callback
            except Exception as e:
                sys.exit("\033[31;m1%s\033[0m" % e)
        elif method == "post":
            try:
                data_encode = urllib.urlencode(asset_data)
                timeout = setting.Params["request_timeout"]
                urls = self.get_url(action_type)
                # print("data_encode-->", data_encode)
                req = urllib2.Request(url=urls, data=data_encode)
                req_data = urllib2.urlopen(req, timeout=timeout)
                callback = req_data.read()
                print("callback-->", callback)
                return callback
            except Exception as e:
                sys.exit("\033[31;m1%s\033[0m" % e)

    def __update_asset_id(self, new_asset_id):
        asset_id_file = setting.Params['asset_id']
        dir_name = os.path.dirname(asset_id_file)
        is_exist = os.path.exists(dir_name)
        # print("dir_name=", dir_name)
        if not is_exist:
            os.mkdir(dir_name)
        f = open(asset_id_file, 'wb')
        if new_asset_id:
            f.write(new_asset_id)
        else:
            sys.exit("new_asset_id is None")
        f.close()

    def report_asset(self):
        object = info_collection.InfoCollection()
        asset_data = object.collection()
        asset_id = self.load_asset_id()
        print("asset_id-->", asset_id)
        if asset_id:
            asset_data["asset_id"] = asset_id
            action_type = 'asset_report'
        else:
            asset_data["asset_id"] = None
            action_type = 'asset_report_with_no_id'

        asset_data = {"asset_data": json.dumps(asset_data)}

        print("report_asset.asset_data -->", asset_data)
        respose_data = self.__submit_data(asset_data, action_type, method="post")
        if respose_data:
            respose_data = json.loads(respose_data)
            if 'asset_id' in respose_data:
                asset_id = respose_data['asset_id']
                self.__update_asset_id(asset_id)







    def run_forever(self):
        print("Does not support run_forever!")

if __name__ == "__main__":
    object = ArgvHanddler("ddddd")
    # object.collect_assets()
    # object.get_asset_id()
    # object.help_msg()
    # object.get_url()
    object.report_asset()
    # object.__update_asset_id('')