import  os

# os.path.abspath(__file__)  #获取当前py文件的绝对路径
# os.path.dirname(os.path.abspath(__file__)) #获取当前py文件的目录路径
root_path =  os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #获取当前py文件的目录的上一层目录路径，在这里是项目的根目录的路径

reports_path = os.path.join(root_path,'Reports')
case_path = os.path.join(root_path,'TestCase')
log_path = os.path.join(root_path,'LogOutput')
data_path = os.path.join(root_path,'Data')
config_path = os.path.join(root_path,'Config')

