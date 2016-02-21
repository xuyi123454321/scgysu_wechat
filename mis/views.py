from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from urllib import parse
import re
import codecs
from .lesson_robber import get_opener

header = {
    "Host": "mis.teach.ustc.edu.cn",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}

url = "http://mis.teach.ustc.edu.cn"

def get_random_image(opener):
    '''
    this function will grap the check code image
    and save it to /tmp/ramdom_image
    '''
    postdata = parse.urlencode({'userbz':'s'}).encode()
    entry_res = opener.open(url+"/userinit.do", postdata)

    entry_page = entry_res.read().decode('gb2312')

    regex = re.compile("randomImage.do\?date='\d*'")

    image_url = regex.search(entry_page)

    if image_url is None:
        # print("Something went wrong!\n")
        return None
    else:
        image_res = opener.open("%s/%s"%(url,image_url.group()))
        image_data = image_res.read()
        return image_data

def init_page(request):
    opener = get_opener(header)
    image_data = get_random_image(opener)
    
    # get the cookies and send it to the user
    cookiejar = opener.handlers[-2].cookiejar
    cookie = []
    for i in cookiejar:
        cookie.append(i)

    cookie = cookie[0]

    context = RequestContext(request, {'picture': "data:image/jpeg;base64,%s"%codecs.encode(image_data, 'base64').decode('utf-8')})
    template = loader.get_template("mis/index.html")
    response = HttpResponse(template.render(context))
    response.set_cookie('scgysumis', cookie.value)

    return response
