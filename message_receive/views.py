from django.shortcuts import render
from django.http import HttpResponse
from hashlib import sha1
from xml.dom import minidom
import time

def url_check(request):
    '''
    for wechat server checking our url
    '''

    token = 'scgysu'
    signature = request.GET['signature']
    timestamp = request.GET['timestamp']
    nonce = request.GET['nonce']
    echostr = request.GET['echostr']

    tmp_str = sha1(''.join(sorted((token, timestamp, nonce))).encode()).hexdigest()

    if tmp_str == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponse('')

def simple_response(request):
    '''
    temperary method before more codes are wirtten
    '''
    tree = minidom.parseString(request.body) # WSGIRequest use body for postdata
    to_user = tree.getElementsByTagName('ToUserName')[0]
    from_user = tree.getElementsByTagName('FromUserName')[0]
    msg_type = tree.getElementsByTagName('MsgType')[0]

    # if msg_type.firstChild.toxml() == 'text':
    msg = tree.getElementsByTagName('Content')[0]
    # swap to_user from_user
    to_user.appendChild(from_user.firstChild)
    from_user.appendChild(to_user.firstChild)

    new_msg = tree.createTextNode("我除了卖萌还什么都不会~~~等媒体中心的小伙伴来回复吧。")
    msg.appendChild(new_msg)
    msg.removeChild(msg.firstChild)

    return HttpResponse(tree.toxml())
    # else:
        #return HttpResponse('')

def empty_page(request):
    return HttpResponse("<script>alert('这里暂时还没有什么，去别处看看吧~~~');</script>")

def message_divide(request):
    '''
    send different request to different models to deal with
    '''

    if request.method == 'GET':
        return url_check(request)
    if request.method == 'POST':
        return simple_response(request)
