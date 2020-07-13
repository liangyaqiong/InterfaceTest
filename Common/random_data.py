import random
import string


class RandomString:
    def __init__(self):
        pass

    def random_data(self,num):

        return  ''.join(random.sample(string.ascii_letters + string.digits, num))

randomstring  = RandomString()

