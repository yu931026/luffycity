# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-02-22 05:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190222_1203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name_plural': '用户信息'},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name': '用户信息', 'verbose_name_plural': '用户信息'},
        ),
    ]
