from json import dump, dumps

from Utils.local_config_utils import  LocalConfig
import requests
import unittest
import re
class TestCases(unittest.TestCase):

    def setUp(self) -> None:
        self.url = LocalConfig.PHP_HOST
        self.session = requests.session()

    def tearDown(self) -> None:
        pass


    def test_case_regist(self):
        #请求头
        header_info = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type":"application/x-www-form-urlencoded"
        }
        #请求参数
        get_token_param = {"m":"u",
                           "c":"register"}

        token_response =  self.session.get(url=self.url+'/phpwind/index.php',params = get_token_param,
                                          )
        info = token_response.content.decode('utf-8') #响应报文处理，将content返回的二进制 转换成'utf-8格式'
        token = re.findall('name="csrf_token" value="(.+?)"/></form>',info )[0]  #正则表达式提取需要的字符串
        # print(info)
        print(token)


        #post
        #请求参数
        params = {
            "m": "u",
            "c": "register",
            "a": "dorun"
        }
        #请求消息体
        data = {
            "username": "liangyq10",
            "password": "123456",
            "repassword": "123456",
            "email": "1441404602@163.com",
            "csrf_token": token
        }
        #请求
        reponse = self.session.post(url=self.url+'/phpwind/index.php',params=params,
                                data =data,
                                headers=header_info
                        )
        reponse.content.decode('utf-8')

if __name__ == '__main__':
    testsuite = unittest.TestSuite()
    testsuite.addTest(TestCases('test_case_regist'))
    runner = unittest.TextTestRunner()
    runner.run(testsuite)