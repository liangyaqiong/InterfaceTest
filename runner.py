import HTMLTestReportCN
import unittest
import time

from Config import settings
from Config.settings import case_path


def case_runner():
    suite = unittest.TestSuite()
    case_discover = unittest.defaultTestLoader.discover(case_path,pattern='test*.py',top_level_dir=None)
    for test_file in case_discover:
        for case in test_file:
           suite.addTests(case)
    return suite

report_dir = HTMLTestReportCN.ReportDirectory( settings.reports_path + '/' )
report_dir.create_dir('API_TEST_')
report_path = HTMLTestReportCN.GlobalMsg.get_value('report_path')
fp = open( report_path,'wb' )
runner = HTMLTestReportCN.HTMLTestRunner(stream=fp,
                                         tester="梁雅琼",
                                         title="API_TEST",
                                         description="接口测试演练")
runner.run(case_runner())
