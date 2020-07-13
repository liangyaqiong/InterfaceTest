import requests
from Utils.local_config_utils import LocalConfig


session = requests.session()



def get_access_token_common():
    "获取TOKEN公共类"
    params = {"grant_type": "client_credential",
              "appid": LocalConfig.APPID,
              "secret": LocalConfig.SERCET
              }
    response =  session.get(url=LocalConfig.WEIXIN_HOST+'/cgi-bin/token',
                params = params )
    TOKEN = response.json()['access_token']
    return TOKEN


def get_access_token_api(grant_type,appid,secret):
    "获取TOKEN接口封装"
    params = {
        "grant_type": grant_type,
        "appid": appid,
        "secret":secret
    }
    response =  session.get(url=LocalConfig.WEIXIN_HOST+'/cgi-bin/token',
                params = params )
    return response


def create_tag_api(TOKEN,tag_json):
    "创建tag接口封装"
    params={"access_token":TOKEN}
    json_data =tag_json

    response =  session.post(url=LocalConfig.WEIXIN_HOST+'/cgi-bin/tags/create',
                params = params,
                json=json_data )
    return response


def update_tag_api(TOKEN,tag_json):
    "编辑tag接口封装"
    params={"access_token":TOKEN}
    json_data =tag_json

    response =  session.post(url=LocalConfig.WEIXIN_HOST+'/cgi-bin/tags/update',
                params = params,
                json=json_data )
    return response

def delete_tag_api(TOKEN,tag_json):
    "删除tag接口封装"
    params={"access_token":TOKEN}
    json_data =tag_json

    response =  session.post(url=LocalConfig.WEIXIN_HOST+'/cgi-bin/tags/delete',
                params = params,
                json=json_data )
    return response

def setremark_api(TOKEN,JSON_PARAMS):
    "设置用户备注名接口封装"
    params={"access_token":TOKEN}
    json_data =JSON_PARAMS

    response =  session.post(url=LocalConfig.WEIXIN_HOST+'/cgi-bin/user/info/updateremark',
                params = params,
                json=json_data )
    return response

