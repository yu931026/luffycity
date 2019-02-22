#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2019/2/22 12:56'

import xadmin
from xadmin import views


from api.models import UserInfo, Course

class UserInfoXadmin():
    list_display = ["user", "balance"]



class CourseXadmin():
    list_display = ["name", "course_type"]


xadmin.site.register(UserInfo, UserInfoXadmin)
xadmin.site.register(Course, CourseXadmin)