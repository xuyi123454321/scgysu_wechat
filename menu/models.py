from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length = 40)
    position = models.IntegerField() #the right side one counts 0

class Button(models.Model):
    act_type = models.CharField(max_length = 30)
    name = models.CharField(max_length = 40)
    key = models.CharField(max_length = 128)
    url = models.URLField()
    media_id = models.CharField(max_length = 128)
    up_menu = models.ForeignKey(Menu)
    position = models.IntegerField() #the lowest one counts 0
