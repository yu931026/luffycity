#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2019/2/18 14:09'

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet, mixins

from api import models
from api.serializers.course import CourseSerializer, CourseDetailSerializer


class CourseView(viewsets.ViewSetMixin, APIView):
    """课程列表及课程详情"""

    def list(self, request, *args, **kwargs):
        """获取课程列表"""
        courses = {
            'code': 1000,
            'data': [],
        }
        try:
            # 在公司需要加分页
            course_list = models.Course.objects.all()
            all_course = CourseSerializer(instance=course_list, many=True)
            courses['data'] = all_course.data
        except Exception as e:
            courses['code'] = 1001
            courses['error'] = '获取课程列表失败'
        return Response(courses)

    def retrieve(self, request, *args, **kwargs):
        course = {
            'code': 1000,
            'data': [],
        }
        try:
            course_id = kwargs.get('pk')
            course_obj = models.CourseDetail.objects.filter(course_id=course_id).first()
            course_ser = CourseDetailSerializer(instance=course_obj, many=False)
            course['data'] = course_ser.data
        except Exception as e:
            course['code'] = 1001
            course['error'] = '获取课程详情失败'

        return Response(course)


# class CourseView(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
#     queryset = models.Course.objects.all()
#     serializer_class = CourseSerializer

