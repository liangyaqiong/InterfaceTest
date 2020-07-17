import re
import ast
# 正则匹配测试
#实际结果：
str1 = '{"access_token":"35_BKh82IAvv_7Obcdwyre-v60qGrcS5rrWo-XN24oxrKZ4Xxh8OIcsa3FahcUsrB_6hY5zEXpx7adPDHNLkFGQuqJY80BHsZc8fIXXkXiMTlvA-hZe5o_KJRlyyVnAXWsywtW5k9vw_1lZ-1IiINAdACAMRE","expires_in":7200}'
#期望结果：
str2 = '{"access_token":"(.+?)","expires_in":(.+?)}'

if re.findall(str2,str1):
    print( True )
else:
    print( False )

print(re.findall(str2,str1))


str_dict = ast.literal_eval(str1) #可以检查是否是这
print(str_dict)
print(str_dict.keys)