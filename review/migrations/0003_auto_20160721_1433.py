# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 06:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_content_news_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content',
            field=models.CharField(max_length=40000),
        ),
    ]
