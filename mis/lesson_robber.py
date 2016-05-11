#!/usr/env python3

from urllib import request, parse
from http import cookiejar
from django.template import RequestContext, loader
from django.http import HttpResponse
import re
import pyquery
import os

header = {
    "Host": "mis.teach.ustc.edu.cn",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}

url = "http://mis.teach.ustc.edu.cn"

def get_opener(head):
    # deal with the Cookies
    cj = cookiejar.CookieJar()
    pro = request.HTTPCookieProcessor(cj)
    opener = request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

def data_input(request):
    raw_data = request.body.decode()
    raw_data = raw_data.split('&')

    raw_data_dict = {}
    for item in raw_data:
        item = item.split('=')
        raw_data_dict[item[0]] = item[1]

    return raw_data_dict

def login(opener, data):

    postdata = {
        'userCode': data["username"],
        'passWord': data["password"],
        'check' : data["check"],
    }

    postdata['userbz'] = 's'
    postdata['hldjym'] = ''
    postdata = parse.urlencode(postdata).encode()

    login_res = opener.open(url+"/login.do", postdata)

    return login_res
    #login_page = login_res.read().decode("gb2312")

    #res_file = open("login.html", "w")
    #res_file.write(login_page)
    #res_file.close()

def query_lesson(opener, data):
    lesson_type = int(data["lesson_type"])

    lesson_number = data["lesson_number"]

    get_data = {
        'xnxq': 20152,
        'seldwdm': 'null',
        'selkkdw': '',
        'seyxn': 2015,
        'seyxq': 2,
        'queryType': lesson_type,
        'rkjs': '',
        'kkdw': '',
        'kcmc': '',
        }
    
    get_data = parse.urlencode(get_data, encoding = 'gb2312')

    query = opener.open(url+"/init_st_xk_dx.do?"+get_data)

    query_page = query.read()
    query_page = pyquery.PyQuery(query_page)

    table = query_page.find('table#dxkctable1')
    tr_list = table.find('tr')[1:]
    parameter = {} # some data to grap from query result

    for tr in tr_list:
        if lesson_number == tr.findall('td')[1].text.strip():
            para_text = tr.findall('td')[-1].find('input').values()[-1]
            para_list = para_text.split('(')[1].split(')')[0].split(',')

            parameter['xnxq'] = 20152
            parameter['kcbjbh'] = lesson_number
            parameter['kcid'] = para_list[3][1:-1] # drop "'"
            parameter['kclb'] = para_list[5][1:-1]
            parameter['kcsx'] = para_list[6][1:-1]
            parameter['cxck'] = para_list[9][1:-1]
            parameter['zylx'] = '01' # it seems that this has to be set 01
            parameter['gxkfl'] = para_list[11][1:-1]
            parameter['xlh'] = para_list[12][1:-1]
            parameter['sjpdm'] = para_list[7][1:-1]
            parameter['kssjdm'] = para_list[8][1:-1]
            
            break

    try:
        parameter['xnxq']
    except KeyError: # lesson not found
        return None
    else:
        return parse.urlencode(parameter, encoding='gb2312')
    
def rob_lesson(opener, para):
    insert_page = opener.open(url+"/xkgcinsert.do?"+para)

    result = insert_page.read().decode('gb2312')

    if result[0] == 'D':
        return False
    else:
        return True

def loop(opener, para):
    while rob_lesson(opener, para):
        pass
    return HttpResponse('<script>alert("已选中");</script>')

def main(request):
    opener = get_opener(header)

    opener.open(url)
    # get cookies
    value = request.COOKIES['scgysumis']
    cookiejar = opener.handlers[-2].cookiejar
    cookie = []
    for i in cookiejar:
        cookie.append(i)
    cookie = cookie[0]

    cookie.value = value
    cookiejar.clear()
    cookiejar.set_cookie(cookie)

    data = data_input(request)

    login_page = login(opener, data).read().decode('gb2312')

    para = query_lesson(opener, data)
    if para == None:
        return HttpResponse('<script>alert("未找到该课程");location.assign("http://wechat.ustc.edu.cn/mis");</script>')

    return loop(opener, para)
