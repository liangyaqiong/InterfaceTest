import ast
import re
from Utils import request_utils


class CheckUtils:

    def __init__(self,response_data=None):

        self.response_data =response_data
        self.check_rules = {
               '无':self.none_check,
               'json键是否存在':self.keys_check,
               'json键值对':self.key_value_check,
               '正则匹配': self.regexp_check
        }

        self.pass_result = {
            'code': 0,
            'response_reason': self.response_data.reason,
            'response_code': self.response_data.status_code,
            'response_headers': self.response_data.headers,
            'response_body': self.response_data.text,
            'check_result': True,
            'message': ''  # 扩招作为日志输出等
        }

        self.fail_result = {
            'code': 2,
            'response_reason': self.response_data.reason,
            'response_code': self.response_data.status_code,
            'response_headers': self.response_data.headers,
            'response_body': self.response_data.text,
            'check_result': False,
            'message': ''  # 扩招作为日志输出等
        }

    def none_check(self,check_data=None):
         return  self.pass_result

    def keys_check(self,check_data=None):
        keys_list = check_data.split(',')
        check_result_list = []
        fail_keys_list = []
        for key in  keys_list:
            if key in self.response_data.json().keys():
                check_result_list.append(self.pass_result)
            else:
                check_result_list.append(self.fail_result)
                fail_keys_list.append(key)
        if  self.fail_result in  check_result_list:
            return self.fail_result
        else:
            return self.pass_result

    def key_value_check(self,check_data=None):
        check_result_list = []
        fail_keys_values_list = []
        for key_value in ast.literal_eval(check_data).items():
            if key_value in self.response_data.json().items():
                  check_result_list.append(self.pass_result)
            else:
                 check_result_list.append(self.fail_result)
                 fail_keys_values_list.append(key_value)
        if self.fail_result in check_result_list:
            return  self.fail_result
        else:
            return  self.pass_result

    def regexp_check(self,check_data=None):
        pattern = re.compile(check_data)#将正则匹配字符串编译为正则表达式对象
        if re.findall(pattern=pattern,string= self.response_data.text):
            return self.pass_result
        else:
            return self.fail_result

    def run_check(self,check_type=None,check_data=None):
        request_code = self.response_data.status_code
        if request_code == 200:
             if check_type in self.check_rules:
                     check_result = self.check_rules[check_type](check_data) # self.check_keyvalue(check_data)
                     return check_result
             else:
                     self.fail_result['message'] ="不支持'%s'判断方法" % check_type
                     return self.fail_result
        else:
            self.fail_result['message'] = "请求失败，状态码不能为:%s" % request_code
            return self.fail_result

if __name__ == '__main__':
    # CheckUtils({"access_token":"hello","expires_":7200}).check_key("access_token,expires_in")
    # print( CheckUtils({"access_token": "hello", "expires_i": 7200}).check_keyvalue( '{"expires_in":7200}' ) )
    # s = {"access_token":"hello","expires_":7200}
    # print( list(s.keys()) )
    # str1 = '{"access_token": "hello", "expires_i": 7200}'
    # pattern = re.compile('"access_toke": "(.+?)"')
    # print( re.findall( pattern,str1 ) )
    # if []:  # 空列表  空字符串 0  False
    #     print( 'hello' )
    CheckUtils(request_utils.RequestUtils().steps_case(cases_info=None))