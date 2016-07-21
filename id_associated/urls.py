from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.associated_page, name='associated_page'),
]
