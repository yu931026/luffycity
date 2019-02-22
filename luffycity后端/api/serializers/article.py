#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2019/2/18 17:55'

from rest_framework import serializers

from api import models


class ArticleSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source='source.name')
    article_type = serializers.CharField(source='get_article_type_display')
    position = serializers.CharField(source='get_position_display')

    class Meta:
        model = models.Article
        fields = ['id', 'title', 'source', 'article_type', 'brief', 'head_img', 'order', 'comment_num', 'agree_num',
                  'view_num', 'collect_num', 'position']


class ArticleContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Article
        fields = ['id', 'title', 'content', 'comment_num', 'agree_num', 'view_num', 'collect_num',]