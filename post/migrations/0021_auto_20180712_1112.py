# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-12 11:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0020_auto_20180712_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=64),
        ),
    ]
