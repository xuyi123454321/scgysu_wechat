from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.message_select, name='message_divide'),
]
