from urllib import request
import json
import redis
import time
from os import path

url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s"

def create_menu():
    log_file = open("%s/%s"%(path.dirname(__file__), "menu.log"), "a")

    menu_file = open("%s/%s"%(path.dirname(__file__), "menu.json"), "r") #using json for now, chang to db later
    menu_data = json.dumps(menu_file.read(), ensure_ascii=False)
    
    token_db = redis.Redis(host="localhost", port=6379, db=0)
    token = token_db.get("token")

    print(menu_data.encode('utf-8'))
    res = request.urlopen(url%token.decode(), menu_data.encode('utf-8'))
    log_file.write("%s %s\n"%(time.ctime(), res.read().decode()))

    log_file.close()
    menu_file.close()

if __name__=='__main__':
    create_menu()
