import time
import redis
import json
import urllib3
from urllib import parse, request
from .models import News, Content
from os import path

def count_diff(token):
    '''
    get the number of materials to grap
    '''

    log_file = open("%s%s"%(path.dirname(__file__), "grap.log"), "a")

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
    
    mat_left = count_diff(token) # the number of materials left
    #test_file.write(str(mat_left))
    offset = News.objects.count() # offset starts with 0

    while mat_left>0:
        post_dict['offset'] = offset;
        post_dict['count'] = 20 if mat_left>20 else mat_left

        post_data = json.dumps(post_dict)
        #test_file.write(post_data)
        req = request.Request(url=url, data=post_data.encode('utf-8'), method='POST')
        res = request.urlopen(req)

        material = json.loads(res.read().decode('utf-8'))

        if 'errorcode' in material:
            log_file = open("%s%s"%(path.dirname(__file__), "grap.log"), "a")
            log_file.write("%s:%s"%(time.ctime(), str(material)))
            log_file.close()
            return 1
    
        for news in material["item"]:
            new_news = News.objects.create(media_id = news["media_id"],
                update_time = news["update_time"])            
            new_news.save()

            for content in news["content"]["news_item"]:
                new_content = Content.objects.create(category = title_analyser(content["title"]),
                    title = content["title"],
                    thumb_media_id = content["thumb_media_id"],
                    show_cover_id = bool(content["show_cover_id"]),
                    author = content["author"],
                    digest = content["digest"],
                    content = content["content"],
                    url = content["url"],
                    content_source_url = content["content_source_url"])
                new_content.save()
                
        mat_left -= 20
        offset += 20 

    return 0

def title_analyser(title):
    '''
    analyse the title to determine the catagory
    '''

    re_str = re.compile(r"^\[.*\]")

    res = re_str.search(title)

    if res is None:
        return Button.objects.get(name="null") # this should be added to the database
    else:
        return Button.objects.get(name=res.group()[1:][:-1]) # cut '[' and ']'

