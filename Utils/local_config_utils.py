import os

from Config import settings
import configparser

class  LocalConfigUtils:

    def __init__(self):
        self.config_path = os.path.join(settings.config_path,'config.ini')
        self.cfs = configparser.ConfigParser()
        self.cfs.read(self.config_path)

    @property #把方法变为属性方法
    def HOST(self):
        host_url = self.cfs.get('host','ADAPTER')
        return host_url

if __name__ == '__main__':

    con = LocalConfigUtils()
    print(con.HOST)
