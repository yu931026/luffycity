#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2019/2/18 19:45'

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from api import models


class TokenAuth(BaseAuthentication):  # 自定义的认证类, 继承此类
    """登录认证"""

    def authenticate(self, request):  # 必须是此方法
        token = request.query_params.get("token")  # 等价于  request._request.GET.get("token")
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:  # 认证失败 要抛错误
            raise exceptions.AuthenticationFailed("验证失败!")
        else:  # 认证成功， 返回元组，赋值给 request.user 和 request.auth
            return token_obj.user, token_obj.token
        # return None 返回空 为匿名用户
