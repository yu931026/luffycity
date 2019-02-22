#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2019/2/18 14:10'

from django.conf.urls import url
from api.views import course, article, account

urlpatterns = [
    # 课程
    url(r'^course/$', course.CourseView.as_view({'get': 'list'})),
    url(r'^course/(?P<pk>\d+)/$', course.CourseView.as_view({'get': 'retrieve'})),

    # 深科技
    url(r'^news/$', article.ArticleView.as_view({'get': 'list'})),
    url(r'^news/(?P<pk>\d+)/$', article.ArticleView.as_view({'get': 'retrieve'})),
    url(r'^news/agree/$', article.NewsAgreeView.as_view()),  # 咨询文章点赞
    url(r'^news/collect/(?P<pk>\d+)/$', article.CollectionView.as_view()),  # 咨询文章收藏

    # 登录
    url(r'^login/$', account.LoginView.as_view()),

    # 购物车相关
    # url(r'^shopping_cart/$',account.ShoppingCartView.as_view({"get": "get", "post": "post", "delete": "delete", "put": "put"})),  # 方式一
    url(r'^shopping_cart/$', account.ShoppingCartView.as_view()),  # 方式二

    # 结算中心
url(r'^payment/$', account.PaymentView.as_view()),
]
