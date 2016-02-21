from django.conf.urls import url

from . import views
from . import lesson_robber

urlpatterns = [
    url(r'^$', views.init_page, name='init_page'),
    url(r'^addtask$', lesson_robber.main, name='addtask'),
]
