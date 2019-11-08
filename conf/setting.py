# Author:jiangcaiyun
# coding:utf-8
import os
BaseDir = os.path.dirname(os.path.dirname(__file__))

Params = {
    "server": "127.0.0.1",
    "port":8000,
    'request_timeout': 30,
    'asset_id': '%s/var/.asset_id' % BaseDir,
    'log_file': '%s/logs/run_log' % BaseDir,
    "urls": {
          "asset_report_with_no_id":"/asset/report/asset_with_no_asset_id/",
          "asset_report":"/asset/report/",  # #正式资产表接口
        },
}

# print(BaseDir)
