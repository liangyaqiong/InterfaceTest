import configparser

class Config_Utils:

    def __init__(self,config_path):
      '实例化configparser，进行配置文件读取'
      self.config = configparser.ConfigParser()
      self.config.read(config_path)

    def config_get(self,section,key):
       '对读取出来的数据通过section,key的形式获取配置文件里面的值'
       config_info = self.config.get(section,key)
       return config_info



