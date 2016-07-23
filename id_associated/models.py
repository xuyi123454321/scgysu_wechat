from django.db import models
from menu.models import Button

class student(models.Model):
    stu_id = models.IntegerField() # as wechat of scgy PB won't be stored
    openid = models.CharField(max_length = 28) # openid of a wechat user

    def __str__(self):
        return str(self.stu_id)
