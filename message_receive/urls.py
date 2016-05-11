from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.message_divide, name='message_divide'),
    url(r'^empty', views.empty_page, name='empty_page'),
]
