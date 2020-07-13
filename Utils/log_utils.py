import logging
import os
import time

from Config import settings


class Log_Utils:

    def __init__(self):
        self.logname = os.path.join(settings.log_path,'ApiTest_%s.log'%time.strftime('%Y_%m_%d'))
        self.logger = logging.getLogger('APITestLog')
        self.logger.setLevel(level=10)
        #设置文件处理器和控制台处理器
        self.filename_handler = logging.FileHandler(filename=self.logname,mode='a',encoding='utf-8')
        self.consle_stream_handler = logging.StreamHandler()
        #设置日志输出格式
        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        self.filename_handler.setFormatter(formatter)
        self.consle_stream_handler.setFormatter(formatter)

        #添加处理器
        self.logger.addHandler(self.filename_handler)
        self.logger.addHandler(self.consle_stream_handler)
        #关闭处理器，防止日志重复打印
        self.consle_stream_handler.close()
        self.filename_handler.close()

    def log_output(self):
         return self.logger


logger = Log_Utils().log_output()

if __name__ == '__main__':
    logger.info('再来测试一下')

