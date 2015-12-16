from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import time
import redis
import json
import urllib3
from urllib import parse, request
from .models import News, Content

def get_thumb_pic(media_id):
    '''
    get thumb picture from wechat, which is what is going to show.
    responses will be raw pictures and this function will store it
    in /tmp and name them after review-tmp-'media_id'(file type is not necessary)
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

    pic_file = open("/tmp/review-tmp-%s"%media_id, "wb")
    pic_file.raw.write(res.read())
    pic_file.close()

def review_page(request):
    '''
    the page to show news review
    '''
    template = loader.get_template("review/review.html")
    thumb_pic_list = Content.objects.filter
    context = RequestContext(request, {'thumb_pic_list': thumb_pic_list})

    return HttpResponse(template.render(context))
