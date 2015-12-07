from django.db import models
from menu.models import SubButton

class material(models.Model):
    media_id = models.IntegerField()
    category = models.ForeignKey(SubButton)
