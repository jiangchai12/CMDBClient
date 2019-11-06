__author__ = 'jiangcaiyun'
# coding=utf-8
from core import info_collection
from conf import setting

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
        print("send_assets.ArgvHanddler.collect_assets-->", asset_data)
        return asset_data

    def package_asset_data(self):
        asset_info = info_collection.InfoCollection()
        packa_data = {"asset_data", asset_info}
        return packa_data

    def get_asset_id(self):
        data_obj = info_collection.InfoCollection()
        asset_data = data_obj.collection()
        asset_id = asset_data["sn"]
        print(asset_id)
        return asset_id
    def get_url(self):

        pass

    def report_asset(self):
        asset_data = self.package_asset_data()
        url = self.get_url()

    def run_forever(self):
        print("Does not support run_forever!")

if __name__ == "__main__":
    object = ArgvHanddler("ddddd")
    # object.collect_assets()
    # object.get_asset_id()
    object.help_msg()