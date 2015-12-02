# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('act_type', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=40)),
                ('key', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('media_id', models.CharField(max_length=128)),
                ('position', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('position', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='button',
            name='up_menu',
            field=models.ForeignKey(to='menu.Menu'),
        ),
    ]
