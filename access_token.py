#!/usr/bin/env python
'''
this script runs apart from the django to
access token from https://api.weixin.qq.com/cgi-bin/token using method GET.
token is stored in redis.
to get the token call redis.Redis(host='localhost', port=6379, db=0) to get the database.
Note that data in redis is of type bytes, so remember to call token.decode()
'''

from urllib import request
import time
import redis
import json
from os import path

class TokenAccessError(Exception):
    '''
    Exception raised when only responce from weixin goes wrong
    '''
    def __str__(self):
        return "Cannot access token"

def access_token(appid, appsecret):
    res = request.urlopen("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(appid, appsecret))
    res_dict = json.loads(res.read().decode())

    if not 'access_token' in res_dict.keys():
        raise TokenAccessError
        return (0, 0)
    else:
        return (res_dict['access_token'], res_dict['expires_in'])

def main():
    log_file = open("%s/%s"%(path.dirname(__file__), "access_token.log"), "a")
    app_data = json.load(open("%s/%s"%(path.dirname(__file__), "app_data.json"), "r"))

    token_cache = redis.Redis(host="localhost", port=6379, db=0)

    while True:
        try:
            token, expires_in = access_token(app_data['appID'],
                                        app_data['appsecret'])
            log_file.write("%s:%s\n"%(time.ctime(), token))
            token_cache['token'] = token # data in redis is stored in bytes
            #time.sleep(expires_in) I decide to use django-crontab instead
        except Exception as e:
            log_file.write("%s:%s\n"%(time.ctime(), e))
            time.sleep(60)
        else:
            break

    log_file.close()

if __name__=='__main__':
    main()
