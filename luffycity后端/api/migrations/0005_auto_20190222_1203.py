# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-02-22 04:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190222_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uid',
            field=models.CharField(help_text='微信用户绑定和CC视频统计', max_length=64, unique=True),
        ),
    ]
