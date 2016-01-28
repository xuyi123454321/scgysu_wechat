from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import time
import redis
import json
import urllib3
from urllib import parse, request
from .models import News, Content

def review_page(request):
    '''
    the page to show news review
    '''
    template = loader.get_template("review/review.html")
    thumb_pic_list = Content.objects.filter
    context = RequestContext(request, {'thumb_pic_list': thumb_pic_list})

    return HttpResponse(template.render(context))
