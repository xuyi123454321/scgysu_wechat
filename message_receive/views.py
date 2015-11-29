from django.shortcuts import render
from django.http import HttpResponse
from hashlib import sha1

def url_check(request):
    '''
    for wechat server checking our url
    '''

    token = 'hello'
    signature = request.GET['signature']
    timestamp = request.GET['timestamp']
    nonce = request.GET['nonce']
    echostr = request.GET['echostr']
    
    tmp_str = sha1(''.join(sorted((token, timestamp, nonce))).encode()).hexdigest()

    if tmp_str == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponse('')

def message_divide(request):
    '''
    send different request to different models to deal with
    '''

    if request.method == 'GET':
        return url_check(request)
    #if request.method == 'POST':
    #    return response(request)
