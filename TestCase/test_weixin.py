import unittest

import requests

from Utils.local_config_utils import LocalConfig
from Utils.log_utils import logger
from Common import common_api


class Test_Cases_Weixin(unittest.TestCase):

    def setUp(self) -> None:
        pass
    def tearDown(self) -> None:
        pass

    def test_get_token_success(self):
        "获取token成功"
        reponse = common_api.get_access_token_api(grant_type='client_credential',
                                              appid=LocalConfig.APPID,
                                              secret=LocalConfig.SERCET
                                             )
        self.assertEqual(reponse.json()['expires_in'],7200)

    def test_get_token_error(self):
        "appid错误，获取token失败"
        reponse = common_api.get_access_token_api(grant_type='client_credential',
                                                  appid='LocalConfig.APPID',
                                                  secret=LocalConfig.SERCET
                                                  )
        self.assertEqual(reponse.json()['errcode'],'40013')
    #
    def test_get_token(self):
        "appid错误，获取token失败"
        reponse = common_api.get_access_token_api(grant_type='client_credential',
                                                  appid='LocalConfig.APPID',
                                                  secret=LocalConfig.SERCET
                                                  )
        self.assertEqual(reponse.json()['errmsg'], 'invalid appid')


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    testsuite.addTest(Test_Cases_Weixin('test_get_token_error'))
    runner = unittest.TextTestRunner()
    runner.run(testsuite)