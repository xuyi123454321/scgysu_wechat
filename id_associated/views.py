from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader, Template, Context
import time
from .models import student

from os import path
from urllib import request
import json

def init_page(request):
    '''
    get code from wechat which is access to user infomation.
    URL in wechat menu is https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
    where
        REDIRECT_URI = http://wechat.ourscgy.ustc.edu.cn/id_associated/init
        SCOPE = snsapi_userinfo
        state is optional.
    REDIRECT_URI will be loaded as redirect_uri/?code=CODE&state=STATE.
    '''
    openid = getOpenidFromCode(request.GET['code']);
    try:
        stu = student.objects.get(openid = openid)
    except student.DoesNotExist:
        return HttpResponse(association_page(openid))

    return HttpResponse(associated_page("openid", openid))

def res_page(request):
    '''
    get user student id via get method
    return id associated page
    '''
    try:
        stu = student.objects.get(stu_id = request.GET['stu_id'])
    except student.DoesNotExist:
        student.objects.create(stu_id = request.GET['stu_id'], openid = request.GET['openid'])
        return render_to_response('id_associated/bind-succeeded.html')

    return HttpResponse(associated_page("openid", request.GET['openid']))

def sep_page(request):
    '''
    web page to separate wechat account and student account
    identify a student by either of openid and stu_id
    '''
    use_openid, use_stu_id = True, True
    try:
        openid = request.GET['openid']
    except KeyError:
        use_openid = False
    try:
        stu_id = request.GET['stu_id']
    except KeyError:
        use_stu_id = False

    try:
        if use_openid:
            stu = student.objects.get(openid = openid)
        elif use_stu_id:
            stu = student.objects.get(stu_id = stu_id)
        else:
            raise student.DoesNotExist
    except student.DoesNotExist:
        return HttpResponse("<script>alert('OOPS~~Something went wrong')</script>") # account to sep doesn't exist

    stu.delete()
    return render_to_response('id_associated/unbind-succeeded.html')

def getOpenidFromCode(code):
    return code
    #info = getBasicInfoFromCode(code)
    #return  info['openid']

def getBasicInfoFromCode(code):
    '''
    get access token to user information from
    https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code
    '''
    info_file_path = path.dirname(__file__) + '../app_data.json'
    info_file = open(info_file_path, 'r')
    app_data = json.load(info_file)
    appid = app_data['appID']
    secrect = app_data['appsecrect']
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(appid, secrect, code)
    info_json = request.urlopen(url)
    info_json = json.loads(total_res.read().decode('utf-8'))

    return info_json

def getUserInfo(token):
    '''
    get user information from
    https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
    '''
    pass # useless for now

def association_page(openid):
    template = loader.get_template("id_associated/binding.html")
    context = Context({'openid': openid})
    return template.render(context)

def associated_page(name, value):
    '''
    generate get values sent to seperate page.
    name could be eigther "stu_id" or "openid".
    '''
    template = loader.get_template("id_associated/binded.html")
    context = Context({'name': name, 'value': value})
    return template.render(context)
