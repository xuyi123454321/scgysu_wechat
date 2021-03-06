"""scgtsu_wechat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from message_receive import urls as message_receive_urls
from review import urls as review_urls
from mis import urls as mis_urls
from id_associated import urls as id_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(message_receive_urls)),
    url(r'^review/', include(review_urls)),
    # url(r'^mis/', include(mis_urls)),
    url(r'^id_associated/', include(id_urls))
]
