#!/usr/bin/env python
'''
access token from https://api.weixin.qq.com/cgi-bin/token using method GET.
token is stored in redis.
to get token call redis.Redis(host='localhost', port=6379, db=0) to get the database.
'''

from urllib import request
import time
import redis
import json

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
    log_file = open("access_token.log", "a")
    app_data = json.load(open("app_data.json", "r"))

    token_cache = redis.Redis(host="localhost", port=6379, db=0)

    while True:
        try:
            token, expires_in = access_token(app_data['appID'],
                                        app_data['appsecret'])
            token_cache['token'] = token
            time.sleep(expires_in)
        except Exception as e:
            log_file.write("%s:%s"%(time.ctime(), e))
            time.sleep(60)
        
if __name__=='__main__':
    main()
