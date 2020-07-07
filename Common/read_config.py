import os

from Utils import  config_utils
from Config import settings


file_name = os.path.join(settings.config_path,'config.ini')
config = config_utils.Config_Utils(config_path=file_name)
value = config.config_get('host','ADAPTER')
print(value)


