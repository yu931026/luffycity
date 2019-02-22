#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2019/2/18 17:45'
from django.db.models import F
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response

from api import models
from api.auth.auth import TokenAuth
from api.serializers.article import ArticleSerializer, ArticleContentSerializer


class ArticleView(ViewSetMixin, APIView):
    """深科技 文章咨询"""

    def list(self, request, *args, **kwargs):
        """咨询文章列表"""
        results = {
            'code': 1000,
            'data': [],
        }
        try:
            article = models.Article.objects.all()
            article_ser = ArticleSerializer(instance=article, many=True)
            results['data'] = article_ser.data
        except Exception as e:
            results['code'] = 1001
            results['error'] = '获取咨询文章列表失败'
        return Response(results)

    def retrieve(self, request, *args, **kwargs):
        """咨询文章详情"""
        results = {
            'code': 1000,
            'data': []
        }
        try:
            nid = kwargs.get('pk')
            article = models.Article.objects.filter(id=nid).first()
            article_ser = ArticleContentSerializer(instance=article, many=False)
            results['data'] = article_ser.data
        except Exception as e:
            results['code'] = 1001,
            results['error'] = '获取文章详情失败'
        return Response(results)


class NewsAgreeView(APIView):
    """点赞"""
    authentication_classes = [TokenAuth, ]

    def post(self, request, *args, **kwargs):
        results = {
            'code': 1000,
        }
        nid = request.data.get('id')
        article = models.Article.objects.filter(id=nid).first()
        if not article:
            results['code'] = 1001
            results['error'] = "点赞失败"
            results['url'] = 'http://127.0.0.1:8000/api/v1/login/'
        else:
            # 方式一：更新 赞数
            article.agree_num += 1
            article.save()
            results['status'] = True
            # 方式二：更新 赞数
            # models.Article.objects.filter(id=nid).update(agree_num=F('agree_num') + 1)
            # results['status'] = True
        return Response(results)


class CollectionView(APIView):
    """收藏"""
    authentication_classes = [TokenAuth, ]

    def post(self, request, *args, **kwargs):
        results = {
            'code': 1000
        }
        try:
            nid = kwargs.get('pk')
            token = request.query_params.get('token')
            with transaction.atomic():  # 多张表进行操作时，要用 事务。
                models.Article.objects.filter(id=nid).update(collect_num=F('collect_num') + 1)  # 文章表里 收藏数 +1
                models.Collection.objects.create(  # 在 收藏表中创建数据
                    user_info=models.UserToken.objects.get(token=token).user,  # 创建 关联user_info
                    content_object=models.Article.objects.get(id=nid)  # 收藏表与 文章表的关联
                )
            results['status'] = True
        except Exception as e:
            print('事务回滚')
            results['code'] = 1001
            results['error'] = '收藏失败'
            # results['status'] = True
        return Response(results)
