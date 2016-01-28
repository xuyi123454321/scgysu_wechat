import time
import redis
import json
import urllib3
from urllib import parse, request
from .models import News, Content
from menu.models import Button
from os import path
import re

# Notice!
# It seems that when a new material is added to the library
# the new one will be put at the first place.

def count_diff():
    '''
    get the number of materials to grap
    '''

    log_file = open("%s/%s"%(path.dirname(__file__), "grap.log"), "a")

    token_db = redis.Redis(host='localhost', port=6379, db=0)
    token = token_db['token'].decode()

    total_url = "https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=%s"%token

    total_old = News.objects.count()

    # get material count
    try_times = 3 # 3 times, 1 every 5 minutes

    while try_times:
        total_res = request.urlopen(total_url)
        total_dict = json.loads(total_res.read().decode('utf-8'))

        if 'news_count' not in total_dict:
            log_file.write("%s:%s\n"%(time.ctime(), total_dict))
            try_times -= 1
            time.sleep(5) # using 5 to test, changing to 5*60 later
        else:
            if try_times < 3:
                log_file.write("%s:Succeed after %d retry"%(time.ctime(), 3-try_times))

            log_file.close()

            return int(total_dict['news_count']) - total_old
            # I hope no materials will be removed

    log_file.close()

    return 0

def grap_cover_pic(media_id):
    '''
    get thumb picture from wechat, which is what is going to show.
    responses will be raw pictures and this function will store it
    in /static/review/cover_pic and name them after their media_id(file type is not necessary)
    ps: I have to say I'm quite annoyed with WeChat's not providing the cover picture url
    '''

    post_dict = {
        'media_id': media_id
    }

    token_db = redis.Redis(host='localhost', port=6379, db=0)
    token = token_db['token'].decode()

    url = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s"%token

    post_data = json.dumps(post_dict)

    req = request.Request(url=url, data=post_data.encode('utf-8'), method='POST')
    res = request.urlopen(req)

    pic_file = open("%s/../static/review/cover_pic/%s"%(path.dirname(__file__), media_id), "wb")
    pic_file.raw.write(res.read())
    pic_file.close()

def grap_material():
    '''
    grap material of news type from wechat
    '''

    post_dict = {
        'type': 'news',
        'offset': 0,
        'count': 0
    }

    #test_file = open("test", "w")

    token_db = redis.Redis(host='localhost', port=6379, db=0)
    token = token_db['token'].decode()

    url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s"%token
    
    mat_left = count_diff() # the number of materials left
    return_var = mat_left
    #test_file.write(str(mat_left))
    offset = 0 # offset starts with 0

    while mat_left>0:
        post_dict['offset'] = offset;
        post_dict['count'] = 20 if mat_left>20 else mat_left

        post_data = json.dumps(post_dict)
        #test_file.write(post_data)
        req = request.Request(url=url, data=post_data.encode('utf-8'), method='POST')
        res = request.urlopen(req)

        material = json.loads(res.read().decode('utf-8'))
        #test_file.write(str(material))
        #test_file.close()

        if 'errorcode' in material:
            log_file = open("%s/%s"%(path.dirname(__file__), "grap.log"), "a")
            log_file.write("%s:%s"%(time.ctime(), str(material)))
            log_file.close()
            return 1
    
        for news in material["item"]:
            new_news = News.objects.create(media_id = news["media_id"],
                update_time = news["update_time"])            
            new_news.save()

            for content in news["content"]["news_item"]:
                new_content = new_news.content_set.get_or_create(category = title_analyser(content["title"]),
                    title = content["title"],
                    thumb_media_id = content["thumb_media_id"],
                    show_cover_pic = bool(content["show_cover_pic"]),
                    author = content["author"],
                    digest = content["digest"],
                    content = content["content"],
                    url = content["url"],
                    content_source_url = content["content_source_url"])[0]
                new_content.save()

                grap_cover_pic(content["thumb_media_id"])
                
        mat_left -= 20
        offset += 20 

    return return_var #return the number of materials grapped

def title_analyser(title):
    '''
    analyse the title to determine the catagory
    '''

    re_str = re.compile(r"^\[.*\]")

    res = re_str.search(title)

    if res is None:
        return Button.objects.get(name="null") # this should be added to the database
        # to mark the article that doesn't exit
    else:
        try:
            return Button.objects.get(name=res.group()[1:][:-1]) # cut '[' and ']'
        except Button.DoesNotExist:
            return Button.objects.get(name="null")

