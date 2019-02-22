#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2019/2/18 14:17'

from rest_framework import serializers
from api import models


class CourseSerializer(serializers.ModelSerializer):
    """ course 表"""
    course_type = serializers.CharField(source='get_course_type_display')
    level = serializers.CharField(source='get_level_display')
    status = serializers.CharField(source='get_status_display')
    sub_category = serializers.CharField(source='sub_category.name')  # 所属子类
    cour_category = serializers.CharField(source='sub_category.category.name')  # 所属大类
    # degree_course = serializers.CharField(source='degree_course.name')
    degree_course = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['id', 'name', 'course_img', 'cour_category', 'sub_category', 'course_type', 'degree_course', 'brief',
                  'level',
                  'pub_date', 'period', 'order', 'attachment_path', 'status', 'template_id'
                  ]

    def get_degree_course(self, obj):
        degree_course_obj = obj.degree_course
        if degree_course_obj:
            return degree_course_obj.name
        else:
            return obj.degree_course


class CourseDetailSerializer(serializers.ModelSerializer):
    """CourseDetail 表"""
    course = serializers.CharField(source='course.name')
    recommend_courses = serializers.SerializerMethodField()
    teachers = serializers.SerializerMethodField()
    course_outline = serializers.SerializerMethodField()  # 课程大纲
    often_asked_question = serializers.SerializerMethodField()  # 常见问题
    course_chapters = serializers.SerializerMethodField()  # 章节
    course_sections = serializers.SerializerMethodField()  # 课时
    homework = serializers.SerializerMethodField()  # 作业
    price_policy = serializers.SerializerMethodField()  # 价格策略
    class Meta:
        model = models.CourseDetail
        fields = ['id', 'course', 'hours', 'course_slogan', 'video_brief_link', 'why_study', 'what_to_study_brief',
                  'career_improvement', 'prerequisite', 'recommend_courses', 'teachers', 'course_outline',
                  'often_asked_question', 'course_chapters', 'course_sections', 'homework', 'price_policy'
                  ]

    def get_recommend_courses(self, obj):
        temp = []
        recommend_course_querysets = obj.recommend_courses.all()
        for recommend_course in recommend_course_querysets:
            temp.append({'id': recommend_course.id, 'name': recommend_course.name})
        return temp

    def get_teachers(self, obj):
        temp = []
        teachers_querysets = obj.teachers.all()
        for teacher in teachers_querysets:
            temp.append({'id': teacher.id, 'name': teacher.name})
        return temp

    def get_course_outline(self, obj):
        temp = []
        course_outline_querysets = obj.courseoutline_set.all()
        for course_outline in course_outline_querysets:
            temp.append(
                {'order': course_outline.order, 'title': course_outline.title, 'content': course_outline.content})
        return temp

    def get_often_asked_question(self, obj):
        temp = []
        question_querysets = obj.course.asked_question.all()
        for question in question_querysets:
            temp.append({"id": question.id, 'question': question.question, 'answer': question.answer})
        return temp

    def get_course_chapters(self, obj):
        temp = []
        course_chapters_querysets = obj.course.coursechapters.all()
        for course_chapters in course_chapters_querysets:
            temp.append(
                {'chapter': course_chapters.chapter, 'name': course_chapters.name, 'summary': course_chapters.summary,
                 'pub_date': course_chapters.pub_date
                 })
        return temp

    def get_course_sections(self, obj):
        temp = []
        course_chapters_querysets = obj.course.coursechapters.all()
        for course_chapters in course_chapters_querysets:
            course_sections_querysets = course_chapters.coursesections.all()
            for course_sections in course_sections_querysets:
                temp.append({
                    'name': course_sections.name,
                    'order': course_sections.order,
                    'section_type': course_sections.get_section_type_display(),
                    'section_link': course_sections.section_link,
                    'video_time': course_sections.video_time,
                    'pub_date': course_sections.pub_date,
                    'free_trail': course_sections.free_trail
                })
        return temp

    def get_homework(self, obj):
        temp = []
        course_chapters_querysets = obj.course.coursechapters.all()
        for course_chapters in course_chapters_querysets:
            homework_querysets = course_chapters.homework_set.all()
            for homework in homework_querysets:
                temp.append({
                    'title': homework.title,
                    'order': homework.order,
                    'homework_type': homework.get_homework_type_display(),
                    'requirement': homework.requirement,
                    'threshold': homework.threshold,
                    'recommend_period': homework.recommend_period,
                    'scholarship_value': homework.scholarship_value,
                    'note': homework.note,
                    'enabled': homework.enabled
                })
        return temp

    def get_price_policy(self,obj):
        temp = []
        price_policy_querysets = obj.course.price_policy.all()
        for price_policy in price_policy_querysets:
            temp.append({
                'valid_period': price_policy.valid_period,
                'price': price_policy.price
            })
        return temp