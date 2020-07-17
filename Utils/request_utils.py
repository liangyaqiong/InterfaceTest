import ast
import re

import jsonpath

from Utils.local_config_utils import LocalConfig
import requests


class RequestUtils:
   def __init__(self):
       self.host_url = LocalConfig.WEIXIN_HOST
       self.headers = {"ContentType":"application/json;charset=utf-8"}
       self.session = requests.session()
       self.temp_variables = {}

   def get(self,params_info):

        response = self.session.get(url=self.host_url + params_info['请求地址'],
                         params = ast.literal_eval(params_info['请求参数(get)'])
                         )
        response.encoding = response.apparent_encoding
        if params_info['取值方式'] == 'json取值':
            value = jsonpath.jsonpath(response.json(),params_info['取值代码'])[0]
            self.temp_variables[params_info['传值变量']] = value
        elif params_info['取值方式'] == '正则取值':
            value = re.findall(params_info['取值代码'],response.text)[0]
            self.temp_variables[params_info['传值变量']] = value

        get_result = {
            'code':0,
            'response_reason':response.reason,
            'response_code':response.status_code,
            'response_headers':response.headers,
            'response_body':response.text
        }
        print(response.url)
        return get_result

   def post(self,params_info):

        response = self.session.post(url=self.host_url+params_info['请求地址'],
                                     params = ast.literal_eval(params_info['请求参数(get)']) ,
                                     json = ast.literal_eval( params_info['提交数据(post)'])
                                     )
        print(params_info['提交数据(post)'])
        response.encoding = response.apparent_encoding
        if params_info['取值方式'] == 'json取值':
            value = jsonpath.jsonpath(response.json(), params_info['取值代码'])[0]
            self.temp_variables[params_info['传值变量']] = value
        elif params_info['取值方式'] == '正则取值':
            value = re.findall(params_info['取值代码'], response.text)[0]
            self.temp_variables[params_info['传值变量']] = value

        post_result = {
            'code': 0,
            'response_reason': response.reason,
            'response_code': response.status_code,
            'response_headers': response.headers,
            'response_body': response.text
        }
        print(response.url)
        return post_result


   def request(self,params_step):

        request_type = params_step['请求方式']
        variable_list = re.findall('\\${\w+}',params_step['请求参数(get)'])
        if  variable_list:
            for variable in variable_list:
                params_step['请求参数(get)'] = params_step['请求参数(get)']\
                .replace(variable,'"%s"' % self.temp_variables[variable[2:-1]])
                print(params_step['请求参数(get)'])
        if request_type == 'get':
            result = self.get(params_step)
        elif request_type == 'post':
            variable_list_post = re.findall('\\${\w+}', params_step['提交数据(post)'])
            if variable_list:
               for variable_post in variable_list_post:
                   params_step['提交数据(post)'] = params_step['提交数据(post)']\
                   .replace( variable_post,'"%s"' % self.temp_variables[variable[2:-1]])
            result = self.post(params_step)

        else:

            result = {'code':1,'result':'请求方式不存在！'}

        return  result

   def steps_case(self,cases_info):
       for case_step in cases_info:
           case_step_result = self.request(case_step)
           if case_step_result['code'] != 0:
              break
           print(case_step_result)
       return case_step_result


if __name__ =='__main__':

    case = RequestUtils()

    case_info =     [ {'请求方式': 'get', '请求地址': '/cgi-bin/token','请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}','提交数据（post）': '', '取值方式': 'json取值', '传值变量': 'token', '取值代码': '$.access_token'},
                      {'请求方式': 'post', '请求地址': '/cgi-bin/tags/update', '请求参数(get)': '{"access_token":${token}}','提交数据(post)': '{"tag":{"id":111,"name":"Ykfn8C47qWd12FKt1"}}', '取值方式': '无', '传值变量': '', '取值代码': ''},
                      {'请求方式': 'post', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}','提交数据(post)': '{"tag" : {"name" : "uwuwbdhdbbwbdhwbdh"} }', '取值方式': '无', '传值变量': '', '取值代码': ''}]

    case.steps_case(case_info)
