import random
import string
from faker import Faker

'生成含字母和数字的随机数'
# print(''.join(random.sample(string.ascii_letters + string.digits, 16)))

'生成四要素信息'
faker = Faker('zh_CN')
print(faker.name()) #伪造名字
print(faker.address())  #伪造地址
print(faker.ssn()) #伪造身份证
print(faker.phone_number()) #伪造手机号
print(faker.credit_card_number()) #信用卡号

dict = {'age':19}
print(dict['age'])