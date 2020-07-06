import requests
import pytest
from Common import  Environment

def setup_function():
    print('\n每个用例执行前开始=========================')
def teardown_function():
    print('\n每个用例执行前结束=========================')

@pytest.mark.goingtotest
def  test_one():
    en = Environment.Environment()
    url_ptc =en.enviro_get('PTC')
    param = 'requestId=53ad59aa-d3a6-4c60-a6fb-44e709631980'
    response =  requests.get(url=url_ptc+'withdraw/bankcard/query',params=param)
    response.encoding='UTF-8'
    print('\n接口请求响应为：\n',response.json())
    re = response.json()
    try:
       assert re["status"] == '20' and re["resultCode"] == '65'

    except Exception as e:
         print('\n==================用例执行失败！')
         raise e
    else:
         print('\n==================用例执行成功！')

@pytest.mark.goingtotest
def test_two():
    a=1
    b=2
    assert  a<b
if __name__ == "__main__":
    pytest.main('-q','test_FirstInterface.py')
