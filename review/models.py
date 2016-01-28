from django.db import models
from menu.models import Button

class News(models.Model):
    media_id = models.CharField(max_length = 256)
    update_time = models.IntegerField()

    def __str__(self):
        return self.media_id

class Content(models.Model):
    news_from = models.ForeignKey(News, null=True)
    category = models.ForeignKey(Button)

    title = models.CharField(max_length = 256)
    thumb_media_id = models.CharField(max_length = 256)
    show_cover_pic = models.BooleanField()
    author = models.CharField(max_length = 32)
    digest = models.CharField(max_length = 64)
    content = models.CharField(max_length = 20000)
    url = models.URLField()
    content_source_url = models.URLField()

    def __str__(self):
        return self.title
