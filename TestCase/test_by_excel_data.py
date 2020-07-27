import os

from Utils import request_utils
from Utils import test_data
from Config import settings

file_path = os.path.join(settings.data_path,'test_case.xlsx')
test_data = test_data.Test_Data(file_path=file_path,sheet_name='Sheet1').test_data_list()
request = request_utils.RequestUtils()
print(test_data)
for case_info in test_data:
      request.steps_case(case_info.get('case_info'))
    # print(case_info.get('case_info'))

