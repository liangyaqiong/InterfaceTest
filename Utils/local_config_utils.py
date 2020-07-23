import os
import random
import string

from Config import settings
import configparser

class  LocalConfigUtils:

    def __init__(self):
        self.config_path = os.path.join(settings.config_path,'config.ini')
        self.cfs = configparser.ConfigParser()
        self.cfs.read(self.config_path,'utf-8')

    @property #把方法变为属性方法
    def ADAPTER_HOST(self):
        host_url = self.cfs.get('host','ADAPTER')
        return host_url
    @property
    def PHP_HOST(self):
        host_url = self.cfs.get('host','PHP_HOST')
        return host_url

    @property
    def WEIXIN_HOST(self):
        host_url = self.cfs.get('host','WEIXIN')
        return host_url

    @property
    def APPID(self):
        value = self.cfs.get('params', 'APPID')
        return value

    @property
    def SERCET(self):
        value = self.cfs.get('params', 'SERCET')
        return value
    @property
    def smtp_server(self):
        value = self.cfs.get('email', 'smtp_server')
        return value
    @property
    def smtp_sender(self):
        value = self.cfs.get('email', 'smtp_sender')
        return value
    @property
    def smtp_key(self):
        value = self.cfs.get('email', 'smtp_key')
        return value
    @property
    def smtp_receiver(self):
        value = self.cfs.get('email', 'smtp_receiver')
        return value
    @property
    def smtp_cc(self):
        value = self.cfs.get('email', 'smtp_cc')
        return value
    @property
    def smtp_subject(self):
        value = self.cfs.get('email', 'smtp_subject')
        return value

LocalConfig = LocalConfigUtils()

if __name__ == '__main__':

    print(LocalConfig.smtp_cc)
