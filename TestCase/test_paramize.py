import os
import unittest
import warnings

import paramunittest
from Config import settings
from Utils import test_data,request_utils


file_path = os.path.join(settings.data_path,'test_case.xlsx')
test_data = test_data.Test_Data(file_path=file_path,sheet_name='Sheet1').test_data_list()

@paramunittest.parametrized(
    *test_data
)


class ParamsTest(paramunittest.ParametrizedTestCase):

    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
    def setParameters(self,case_id,case_info):
        self.case_name = case_id
        self.case_info = case_info

    def test_case(self):
      '''测试备注'''
      self._testMethodName = self.case_info[0].get('测试用例编号')  #self.case_info 返回的是一个列表
      self._testMethodDoc =self.case_info[0].get('测试用例名称')
      #调用接口进行测试
      print(self.case_info[0].get('测试用例名称'),self.case_info[0].get('测试用例编号'))
      test_result =   request_utils.RequestUtils().steps_case(self.case_info)
      #断言
      self.assertTrue(test_result['check_result'],test_result['message'])

if __name__ == '__main__':
    unittest.main( verbosity=0)

