import unittest
from random import random

import requests
from Common.random_data import RandomString
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
        logger.info(reponse.headers)
        self.assertIn('"access_token"',reponse.text)

    def test_get_token_error(self):
        "appid错误，获取token失败"
        reponse = common_api.get_access_token_api(grant_type='client_credential',
                                                  appid='LocalConfig.APPID',
                                                  secret=LocalConfig.SERCET
                                                  )
        self.assertEqual(reponse.json()['errcode'],40013)
    #
    def test_create_tag_success(self):
        "创建标签成功测试"
        json_data = {   "tag" : {     "name" : "ayjhsjhsjqsj326"   } }
        reponse = common_api.create_tag_api(TOKEN = common_api.get_access_token_common(),
                                            tag_json=json_data)
        print(reponse.text)
        self.assertIn('id',reponse.text)

    def test_create_tag_success(self):
        "创建标签成功测试"
        json_data = {   "tag" : {     "name" : RandomString().random_data(num=16)   } }
        reponse = common_api.create_tag_api(TOKEN = common_api.get_access_token_common(),
                                            tag_json=json_data)
        print(reponse.text)
        # self.assertEqual(reponse.json()['errmsg'], 'invalid appid')
        self.assertIn('"id"',reponse.text)

    def test_create_tag_error(self):
        "创建标签失败：标签重复"
        json_data = {   "tag" : {     "name" : '小白兔'   } }
        reponse = common_api.create_tag_api(TOKEN = common_api.get_access_token_common(),
                                            tag_json=json_data)
        print(reponse.text)
        self.assertEqual(reponse.json()['errcode'], 45157)

    def test_update_tag_succcess(self):
        "编辑标签成功"
        json_data = {   "tag" : {     "id" : 106,     "name" :  RandomString().random_data(num=16)  } }
        reponse = common_api.update_tag_api(TOKEN = common_api.get_access_token_common(),
                                            tag_json=json_data)
        logger.info(reponse.text)
        self.assertEqual(reponse.json()['errmsg'], 'ok')

    def test_update_tag_error(self):
        "编辑标签失败：和其他标签重名"
        json_data = {"tag": {"id": 110, "name":'小白兔'}}
        reponse = common_api.update_tag_api(TOKEN=common_api.get_access_token_common(),
                                            tag_json=json_data)
        logger.info('[编辑标签失败：不存在的id]用例  接口响应报文：'+ reponse.text)
        self.assertEqual(reponse.json()['errcode'], 45157)

    def test_delete_tag_success(self):
        "删除标签成功"
        json_data = {   "tag":{        "id" : 106   } }
        reponse = common_api.delete_tag_api(TOKEN=common_api.get_access_token_common(),
                                            tag_json=json_data)
        logger.info('[删除标签成功]用例  接口响应报文：' + reponse.text)
        self.assertEqual(reponse.json()['errmsg'], 'ok')

    def test_delete_tag_error(self):
        "删除标签失败，不能修改0/1/2这三个系统默认保留的标签"
        json_data = {"tag": {"id": 1}}
        reponse = common_api.delete_tag_api(TOKEN=common_api.get_access_token_common(),
                                            tag_json=json_data)
        logger.info('[删除标签失败，不能修改0/1/2这三个系统默认保留的标签]用例  接口响应报文：' + reponse.text)
        self.assertEqual(reponse.json()['errcode'], 45058)

    def setremark_api_error(self):
        "设置备注名失败：不正确的appid"
        json_data = {
                "openid":"wx1e007fa71e41c91c",
                "remark":"pangzi"
}
        reponse = common_api.setremark_api(TOKEN=common_api.get_access_token_common(),
                                            JSON_PARAMS=json_data)
        logger.info('[设置备注名失败：不正确的appid]用例  接口响应报文：' + reponse.text)
        self.assertEqual(reponse.json()['errcode'], 40013)

    def setremark_api_error_openid(self):
        "设置备注名失败：不正确的openid"
        json_data = {
            "openid": "ocYxcuBt0mRugKZ7tGAHPnUaOW7Y",
            "remark": "pangzi"
        }
        reponse = common_api.setremark_api(TOKEN=common_api.get_access_token_common(),
                                           JSON_PARAMS=json_data)
        logger.info('[设置备注名失败：不正确的openid]用例  接口响应报文：' + reponse.text)
        self.assertEqual(reponse.json()['errcode'], 40003)


if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    testsuite.addTest(Test_Cases_Weixin('test_get_token_success'))
    runner = unittest.TextTestRunner()
    runner.run(testsuite)