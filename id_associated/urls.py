from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^init', views.init_page, name='get_code'),
    url(r'^sep', views.sep_page, name='seperate'),
    url(r'^res', views.res_page, name='get_stu_id')
]
