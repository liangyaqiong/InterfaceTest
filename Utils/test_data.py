import os

from Config import settings
from Utils  import excel_data_utils

class Test_Data:

    def __init__(self,file_path,sheet_name):
       "初始化excel数据，把excel数据用封装好的工具类加工成字典的形式"
       self.excel= excel_data_utils.Excel_Utils(file_path=file_path,sheet_name=sheet_name)
       self.dict_data = self.excel.get_dict_data()

    def dict_add_case_number(self):
        "将excele数据进行加工"
        test_data_dict = {}
        for row_data in self.dict_data:
            test_data_dict.setdefault(row_data['测试用例编号'],[]).append(row_data)
        return  test_data_dict

    def test_data_list(self):
        "对excel数据进行加工，转换成列表，每个元素为“用例名：用例执行内容” 的形式"
        data_list = []
        for a, b in self.dict_add_case_number().items():
             dict_test_data = {}
             dict_test_data['case_id'] = a
             dict_test_data['case_info'] = b
             data_list.append(dict_test_data)
        return  data_list


if __name__ == '__main__':

     pass