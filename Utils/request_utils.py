import ast
import re
from requests import exceptions
import jsonpath
from requests.exceptions import ProxyError, RequestException

from Utils.local_config_utils import LocalConfig
from Utils import check_utils
import requests

from Utils.log_utils import logger


class RequestUtils:
   def __init__(self):
       self.host_url = LocalConfig.WEIXIN_HOST
       self.headers = {"ContentType":"application/json;charset=utf-8"}
       self.session = requests.session()
       self.temp_variables = {}

   def __get(self,params_info):
        #该方法实现get请求封装，并将需要传递给后面接口的字段及值以字段的形式存储起来temp_variables
    try:
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
        get_result = check_utils.CheckUtils(response).run_check(check_type=params_info['期望结果类型'],check_data=params_info['期望结果']) #调用断言封装类
    except ProxyError as e:
        get_result = {'code': 4, 'result': '接口%s在请求时发生代理异常' % params_info['接口名称'], '报错信息': 's%' % e.__str__()}
    except ConnectionError as e:
        get_result = {'code': 4, 'result': '接口%s在请求时发生连接异常' % params_info['接口名称'], '报错信息': 's%' % e.__str__()}
    except RequestException as e:
        get_result = {'code': 4, 'result': '接口%s在请求时发生Request异常' % params_info['接口名称'], '报错信息': 's%' % e.__str__()}
    except Exception as e:
        get_result = {'code': 4, 'result': '接口%s在请求时发生异常' % params_info['接口名称'], '报错信息': 's%' % e.__str__()}
    return get_result

   def __post(self,params_info):
     try:
            #该方法实现post请求封装，并将需要传递给后面接口的字段及值以字段的形式存储起来temp_variables
            response = self.session.post(url=self.host_url+params_info['请求地址'],
                                         params = ast.literal_eval(params_info['请求参数(get)']) ,
                                         json = ast.literal_eval( params_info['提交数据(post)'])
                                         )
            response.encoding = response.apparent_encoding
            if params_info['取值方式'] == 'json取值':
                value = jsonpath.jsonpath(response.json(),params_info['取值代码'])[0]
                self.temp_variables[params_info['传值变量']] = value
            elif params_info['取值方式'] == '正则取值':
                value = re.findall(params_info['取值代码'], response.text)[0]
                self.temp_variables[params_info['传值变量']] = value
            post_result = check_utils.CheckUtils(response).run_check(check_type=params_info['期望结果类型'],check_data=params_info['期望结果'])#调用断言封装类
     except ProxyError as e:
            post_result = {'code':4,'result' : '接口%s在请求时发生代理异常' % params_info['接口名称'],'报错信息':'s%' % e.__str__()}
     except ConnectionError as e:
         post_result = {'code': 4, 'result': '接口%s在请求时发生连接异常' % params_info['接口名称'], '报错信息': 's%' % e.__str__()}
     except RequestException as e:
         post_result = {'code': 4, 'result': '接口%s在请求时发生Request异常' % params_info['接口名称'], '报错信息': 's%' % e.__str__()}
     except Exception as e:
         post_result = {'code': 4, 'result': '接口%s在请求时发生异常' % params_info['接口名称'], '报错信息': 's%' % e.__str__()}
     return post_result


   def request(self,params_step):
        #'该方法实现：1.获取excel读取的参数中需要类似${token}这种格式的需要依赖前一个接口的字段，并替换成temp_variables临时储存
        #字段中的值 2.把请求根据请求类型分发给不同的方法并返回请求结果
        request_type = params_step['请求方式']
        variable_list = re.findall('\\${\w+}',params_step['请求参数(get)'])
        if  variable_list:
            for variable in variable_list:
                params_step['请求参数(get)'] = params_step['请求参数(get)']\
                .replace(variable,'"%s"' % self.temp_variables[variable[2:-1]])
        if request_type == 'get':
            result = self.__get(params_step)
        elif request_type == 'post':
            variable_list_post = re.findall('\\${\w+}', params_step['提交数据(post)'])
            if variable_list_post:
               for variable_post in variable_list_post:
                   params_step['提交数据(post)'] = params_step['提交数据(post)']\
                   .replace( variable_post,'"%s"' % self.temp_variables[variable_post[2:-1]])
            result = self.__post(params_step)

        else:

            result = {'code':1,'result':'请求方式不存在！'}

        return  result

   def steps_case(self,cases_info):
       #该方法实现将具有多个步骤的测试用例一一分发给包装好的request()方法，为该类的调用入口
       for case_step in cases_info:
           print('CASE_STEP: ',case_step['测试用例编号'],case_step['测试用例名称'],)
           case_step_result = self.request(case_step)
           if case_step_result['code'] != 0:
               logger.error('存在接口请求异常')
               break
           else:
               logger.info(case_step_result)
       return case_step_result


if __name__ =='__main__':

    case = RequestUtils()

    # case_info = [{'测试用例编号': 'case02', '测试用例名称': '测试能否正确新增用户标签', '用例执行': '否', '测试用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}', '提交数据(post)': '', '取值方式': '正则取值', '传值变量': 'token', '取值代码': '"access_token":"(.+?)"', '期望结果类型': '正则匹配', '期望结果': '{"access_token":"(.+?)","expires_in":(.+?)}'}]
    case_info = [{'测试用例编号': 'case01', '测试用例名称': '测试能否正确执行获取access_token接口', '用例执行': '否', '测试用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}', '提交数据(post)': '', '取值方式': '正则取值', '传值变量': 'token', '取值代码': '"access_token":"(.+?)"', '期望结果类型': '正则匹配', '期望结果': '{"access_token":"(.+?)","expires_in":(.+?)}'},
                 {'测试用例编号': 'case01', '测试用例名称': '测试查询所有标签', '用例执行': '是', '测试用例步骤': 'step_02', '接口名称': '获取所有标签接口', '请求方式': 'get', '请求地址': '/cgi-bin/tags/get', '请求参数(get)': '{"access_token":${token}}', '提交数据(post)': '', '取值方式': '', '传值变量': '', '取值代码': '', '期望结果类型': 'json键是否存在', '期望结果': 'tags'},
                 {'测试用例编号': 'case02', '测试用例名称': '获取token', '用例执行': '否', '测试用例步骤': 'step_01','接口名称': '获取access_token接口', '请求方式': 'get', '请求地址': '/cgi-bin/token','请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}','提交数据(post)': '', '取值方式': '正则取值', '传值变量': 'token', '取值代码': '"access_token":"(.+?)"', '期望结果类型': '正则匹配','期望结果': '{"access_token":"(.+?)","expires_in":(.+?)}'},
                 {'测试用例编号': 'case02', '测试用例名称': '测试是否能创建标签', '用例执行': '是', '测试用例步骤': 'step_02', '接口名称': '新建标签', '请求方式': 'post', '请求地址': '/cgi-bin/tags/create', '请求参数(get)': '{"access_token":${token}}', '提交数据(post)': '{"tag": {"name":"happy36"}}', '取值方式': 'json取值', '传值变量': 'tagid', '取值代码': "$.tag.id", '期望结果类型': '正则匹配', '期望结果': '{"tag":{"id":(.+?),"name":"happy36"}}'},
                 {'测试用例编号': 'case03', '测试用例名称': '获取token', '用例执行': '否', '测试用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}', '提交数据(post)': '', '取值方式': '正则取值', '传值变量': 'token', '取值代码': '"access_token":"(.+?)"', '期望结果类型': '正则匹配', '期望结果': '{"access_token":"(.+?)","expires_in":(.+?)}'},
                 {'测试用例编号': 'case03', '测试用例名称': '测试是否能更新标签', '用例执行': '是', '测试用例步骤': 'step_02', '接口名称': '更新标签', '请求方式': 'post', '请求地址': '/cgi-bin/tags/update', '请求参数(get)': '{"access_token":${token}}', '提交数据(post)': '{"tag":{"id":${tagid},"name":"sad35"}} ', '取值方式': '', '传值变量': '', '取值代码': '', '期望结果类型': 'json键值对', '期望结果': '{"errcode":0,"errmsg":"ok"}' },
                 {'测试用例编号': 'case04', '测试用例名称': '获取token', '用例执行': '否', '测试用例步骤': 'step_01', '接口名称': '获取access_token接口', '请求方式': 'get', '请求地址': '/cgi-bin/token', '请求参数(get)': '{"grant_type":"client_credential","appid":"wx55614004f367f8ca","secret":"65515b46dd758dfdb09420bb7db2c67f"}', '提交数据(post)': '', '取值方式': '正则取值', '传值变量': 'token', '取值代码': '"access_token":"(.+?)"', '期望结果类型': '正则匹配', '期望结果': '{"access_token":"(.+?)","expires_in":(.+?)}'},
                 {'测试用例编号': 'case04', '测试用例名称': '测试是否能删除标签', '用例执行': '是', '测试用例步骤': 'step_02', '接口名称': '更新标签', '请求方式': 'post', '请求地址': '/cgi-bin/tags/delete', '请求参数(get)': '{"access_token":${token}}', '提交数据(post)': '{"tag":{"id":${tagid}}} ', '取值方式': '', '传值变量': '', '取值代码': '', '期望结果类型': 'json键值对', '期望结果': '{"errcode":0,"errmsg":"ok"}'},
                 ]

    case.steps_case(case_info)
