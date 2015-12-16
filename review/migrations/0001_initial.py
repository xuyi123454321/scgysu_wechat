# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('thumb_media_id', models.CharField(max_length=256)),
                ('show_cover_pic', models.BooleanField()),
                ('author', models.CharField(max_length=32)),
                ('digest', models.CharField(max_length=64)),
                ('content', models.CharField(max_length=20000)),
                ('url', models.URLField()),
                ('content_source_url', models.URLField()),
                ('category', models.ForeignKey(to='menu.Button')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('media_id', models.CharField(max_length=256)),
                ('update_time', models.IntegerField()),
            ],
        ),
    ]
