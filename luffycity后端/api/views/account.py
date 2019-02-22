#!/usr/bin/env python
# _*_ encoding:utf-8 _*_
__author__ = '于sir'
__date__ = '2019/2/18 14:09'
import uuid
import json
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection
from rest_framework.viewsets import ViewSetMixin
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db.models import Q

from api import models
from utils.response import BaseResponse, TokenResponse
from api.auth.auth import TokenAuth
from utils.exception import PricePolicyInvalid


# class LoginView(APIView):
#     """登录"""
#
#     def post(self, request, *args, **kwargs):
#         results = {
#             'code': 1000,
#         }
#         try:
#             user = request.data.get('user')
#             pwd = request.data.get('pwd')
#             user_obj = models.UserInfo.objects.get(user=user, pwd=pwd)  # 取不到和取多个都会报错
#             if not user_obj:
#                 results['code'] = 1001
#                 results['error'] = '用户名或密码错误'
#                 return Response(results)
#             token = str(uuid.uuid4())
#             models.UserToken.objects.update_or_create(user=user_obj, defaults={'token': token})
#             results['token'] = token
#         # except ObjectDoesNotExist as e:  # get 数据出现异常
#         #     results['code'] = 1002
#         #     results['error'] = '用户名或密码错误'
#         except Exception as e:
#             results['code'] = 1003
#         return Response(results)


class LoginView(APIView):
    """登录"""

    def post(self, request, *args, **kwargs):
        results = TokenResponse()
        try:
            user = request.data.get('user')
            pwd = request.data.get('pwd')
            user_obj = models.UserInfo.objects.get(user=user, pwd=pwd)  # 取不到和取多个都会报错

            token = str(uuid.uuid4())
            models.UserToken.objects.update_or_create(user=user_obj, defaults={'token': token})
            results.token = token
        except ObjectDoesNotExist as e:  # 捕捉 get 数据出现异常
            results.code = 1002
            results.error = '用户名或密码错误'
        except Exception as e:
            results.code = 1003
        return Response(results.dict)  # 拿到对象里面的所有的东西，以字典的形式、执行dict方法。本质等价于results.__dict__


# 购物车方式一：
"""
redis中的数据结构
redis->{
        shopping_car:{
            用户ID:{
                课程ID:{
                    title:'金融量化分析入门',
                    img:'/xx/xx/xx.png',
                    policy:{
                        10: {'name':'有效期1个月','price':599},
                        11: {'name':'有效期3个月','price':1599},
                        13: {'name':'有效期6个月','price':2599},
                    },
                    default_policy:12
                },
                课程ID:{
                    title:'金融量化分析入门',
                    img:'/xx/xx/xx.png',
                    policy:{
                        10: {'name':'有效期1个月','price':599},
                        11: {'name':'有效期3个月','price':1599},
                        13: {'name':'有效期6个月','price':2599},
                    },
                    default_policy:10
                }
            },
            用户ID:{...},
        }
    }
"""
# class ShoppingCartView(ViewSetMixin, APIView):
#     """购物车"""
#     authentication_classes = [TokenAuth,]
#     def post(self, request, *args, **kwargs):
#         """
#         购物车添加一条数据
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         results = {
#             'code': 1000
#         }
#
#         conn = get_redis_connection('default')
#         course_id = request.data.get('course_id')
#         policy_id = request.data.get('policy_id')
#         user_id = request.data.get('user_id')
#         try:
#             # 根据前端传的请求数据 {course_id:1, policy_id: 1, user_id: 1} 检验当前课程是否有此价格策略。
#             course_obj = models.Course.objects.get(id=course_id)  # 课程对象
#             policy_obj = course_obj.price_policy.filter(id=policy_id).first()  # 价格策略对象
#             if not policy_obj:
#                 results['code'] = 1001
#                 results['error'] = '加入购物车失败'
#                 return Response(results)
#
#             # 还要先判断该用户是否有购物车数据，防止买第二个课程时会覆盖
#             data_json = conn.hget("luffy_shopping_car",user_id)
#             if data_json:  # data_json不为None ,有记录。用已有的data，插入再更新
#                 data_str = str(data_json, encoding='utf-8')
#                 data = json.loads(data_str, encoding='utf-8')
#             else:  # 该用户没有购物车数据，就创建
#                 data = {}
#             # 构造data字典
#             data_course = data[course_id] = {}
#             data_course["title"] = course_obj.name
#             data_course["img"] = course_obj.course_img
#             data_course["default_policy"] = policy_obj.id
#             data_policy = data_course["policy"] = {}
#             for policy in course_obj.price_policy.all():
#                 data_policy[policy.id] = {"name": policy.get_valid_period_display(),
#                                           "price": policy.price}
#
#             # 将 data 数据存入redis
#             data_json = json.dumps(data, ensure_ascii=False)  # ensure_ascii=False 保留中文
#             conn.hmset("luffy_shopping_car", {user_id: data_json})
#
#         except Exception as e:
#             results['code'] = 1001
#             results['error'] = '加入购物车失败'
#         return Response(results)
#
#     def get(self, request, *args, **kwargs):
#         """
#         查看购物车
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         results = {'code': 1000, "data": {}}
#         conn = get_redis_connection('default')
#         user_id = request.data.get('user_id')
#         try:
#             data_json = conn.hget("luffy_shopping_car", user_id)  # 去redis中拿 用户的购物车数据
#             data_str = str(data_json, encoding='utf-8')  # 将bytes 类型转成 字符串，然后再json
#             data = json.loads(data_str, encoding='utf-8')
#             results['data'] = data
#         except Exception as e:
#             results['code'] = 1001
#             results['error'] = '查看购物车失败'
#         return Response(results)
#
#     def delete(self, request, *args, **kwargs):
#         """
#         删除购物车中的数据
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         result = {'code': 1000}
#         conn = get_redis_connection('default')
#         user_id = request.data.get('user_id')
#         course_id_list = request.data.get("course_id")  # 课程的ID列表，可能是批量删除
#         try:
#             data_json = conn.hget("luffy_shopping_car", user_id)  # 去redis中拿 用户的购物车数据
#             data_str = str(data_json, encoding='utf-8')  # 将bytes 类型转成 字符串，然后再json
#             data = json.loads(data_str, encoding='utf-8')
#             for course_id in course_id_list:
#                 del data[str(course_id)]  # 经过序列化后，字典的key由数字变成字符串。
#
#             # 删除处理后，再保存回redis
#             data_json = json.dumps(data, ensure_ascii=False)
#             conn.hset("luffy_shopping_car", user_id, data_json)
#         except Exception as e:
#             result['code'] = 1001
#             result['error'] = '删除失败'
#         return Response(result)
#
#     def put(self, request, *args, **kwargs):
#         """
#         更新价格策略
#         :param request:
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         results = {'code': 1000}
#         conn = get_redis_connection('default')
#         user_id = request.data.get('user_id')
#         course_id = request.data.get('course_id')
#         policy_id = request.data.get('policy_id')
#         try:
#             # 根据前端传的请求数据 {course_id:1, policy_id: 1, user_id: 1} 检验当前课程是否有此价格策略。
#             course_obj = models.Course.objects.get(id=course_id)  # 课程对象
#             policy_obj = course_obj.price_policy.filter(id=policy_id).first()  # 价格策略对象
#             if not policy_obj:
#                 results['code'] = 1001
#                 results['error'] = "更新价格策略失败"
#                 return Response(results)
#             data_json = conn.hget('luffy_shopping_car', user_id)
#             data_str = str(data_json, encoding='utf-8')  # 将bytes 类型转成 字符串，然后再json
#             data = json.loads(data_str, encoding='utf-8')
#             data[str(course_id)]["default_policy"] = policy_id
#
#             data_json = json.dumps(data, ensure_ascii=False)
#             conn.hset("luffy_shopping_car", user_id, data_json)
#         except Exception as e:
#             results['code'] = 1001
#             results['error'] = "更新价格策略失败"
#         return Response(results)


# 购物车方式二：
"""
购物车 redis中的数据结构
redis->{
        shopping_car_用户ID1_课程ID1:{
            title:'金融量化分析入门',
            img:'/xx/xx/xx.png',
            policy:{
                10: {'name':'有效期1个月','price':599},
                11: {'name':'有效期3个月','price':1599},
                13: {'name':'有效期6个月','price':2599},
            },
            default_policy:12
        },
        shopping_car_用户ID1_课程ID2:{
            title:'金融量化分析入门',
            img:'/xx/xx/xx.png',
            policy:{
                10: {'name':'有效期1个月','price':599},
                11: {'name':'有效期3个月','price':1599},
                13: {'name':'有效期6个月','price':2599},
            },
            default_policy:12
        }
    }
    
"""


class ShoppingCartView(APIView):
    """购物车"""
    conn = get_redis_connection('default')

    authentication_classes = [TokenAuth,]
    def post(self, request, *args, **kwargs):
        """
        购物车添加一条数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        results = BaseResponse()
        try:
            # 1.获取用户提交的 课程ID 和 价格策略ID
            course_id = int(request.data.get('course_id'))  # 有可能传来是 str 类型，不管什么类型，都转换成int
            policy_id = int(request.data.get('policy_id'))
            # 2.获取课程信息
            course_obj = models.Course.objects.get(id=course_id)  # 课程对象。 如果取不到或取多个就报错 ObjectDoesNotExist
            # 3.获取该课程的所有的价格策略
            price_policy_list = course_obj.price_policy.all()
            price_policy_dict = {}
            for item in price_policy_list:
                price_policy_dict[item.id] = {
                    "period_display": item.get_valid_period_display(),
                    "period": item.valid_period,
                    "price": item.price
                }
            # 4.检测 用户提交的价格策略id 是否存在(合法) 该课程是否有此 价格策略
            if policy_id not in price_policy_dict:  # 价格策略不合法， 抛出自定义异常
                raise PricePolicyInvalid("价格策略不合法")
            # 5.将购物信息添加到 redis 中
            user_id = request.user.id  # 用户认证过后用  user_id = request.user.id 来获取
            redis_car_key = "shopping_car_{0}_{1}".format(user_id, course_id)  # redis 中存的key
            # redis_car_key = settings.SHOPPING_CART_KEY.format(user_id, course_id)  # 可以配置到 settings.py 里面

            self.conn.hmset(redis_car_key,
                            {"title": course_obj.name, "img": course_obj.course_img,
                             "policy": json.dumps(price_policy_dict),
                             "default_policy": policy_id})
            results.data = "添加成功"
        except ObjectDoesNotExist as e:
            results.code = 3001
            results.error = "课程不存在"
        except PricePolicyInvalid as e:
            results.code = 2001
            results.error = e.error
        except Exception as e:
            results.code = 1001
            results.error = "添加失败"
        return Response(results.dict)

    def get(self, request, *args, **kwargs):
        """
        查看购物车
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        results = BaseResponse()
        try:
            user_id = request.user.id  # 用户认证过后用  user_id = request.user.id 来获取
            redis_car_keys = settings.SHOPPING_CART_KEY.format(user_id, "*")  # 当前用户所有的key
            # 构造该用户购物车里所有的课程列表，并返回
            course_list = []
            for key in self.conn.scan_iter(redis_car_keys, count=10):
                course_id = str(key, encoding='utf-8').rsplit("_", maxsplit=1)[1]  # str 类型
                # print(course_id, type(course_id))
                course_info = {
                    course_id: {
                        "title": self.conn.hget(key, "title").decode('utf-8'),
                        "img": self.conn.hget(key, "img").decode('utf-8'),
                        "default_policy": self.conn.hget(key, "default_policy").decode('utf-8'),
                        "policy": json.loads(self.conn.hget(key, "policy").decode('utf-8')),  # 转换成 字符串
                    }
                }
                course_list.append(course_info)
            results.data = course_list
        except Exception as e:
            results.code = 1001
            results.error = "获取购物车列表失败"
        return Response(results.dict)

    def delete(self, request, *args, **kwargs):
        """
        删除购物车中的数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        result = BaseResponse()
        try:
            course_id_list = request.data.get('course_id')
            user_id = request.user.id  # 用户认证过后用  user_id = request.user.id 来获取
            # key_list = []
            # for course_id in course_id_list:
            #     redis_car_key = settings.SHOPPING_CART_KEY.format(user_id, course_id)
            #     key_list.append(redis_car_key)
            key_list = [settings.SHOPPING_CART_KEY.format(user_id, course_id) for course_id in course_id_list]  # 同上注释掉的
            self.conn.delete(*key_list)  # 删除
        except Exception as e:
            result.code = 1001
            result.error = "删除失败"
        return Response(result.dict)

    def patch(self, request, *args, **kwargs):
        """
        更新价格策略
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        results = BaseResponse()
        try:
            course_id = request.data.get('course_id')
            user_id = request.user.id  # 用户认证过后用  user_id = request.user.id 来获取
            policy_id = str(request.data.get('policy_id'))

            redis_car_key = settings.SHOPPING_CART_KEY.format(user_id, course_id)
            if not self.conn.exists(redis_car_key):  # 判断 key 是否存在。  不存在
                results.code = 2001
                results.error = "购物车不存在此课程"
                return Response(results.dict)
            # 课程存在，判断价格策略是否存在
            policy_dict = json.loads(str(self.conn.hget(redis_car_key, 'policy'), encoding='utf-8'))  # 所有的价格策略
            if policy_id not in policy_dict:  # 价格策略不存在
                raise PricePolicyInvalid("该课程不存在此价格策略")
            # 修改 默认价格策略
            self.conn.hset(redis_car_key, "default_policy", policy_id)
            results.data = "修改成功"
        except PricePolicyInvalid as e:
            results.code = 2002
            results.error = e.error
        except Exception as e:
            results.code = 1001
            results.error = "更新失败"

        return Response(results.dict)


"""
结算中心 redis 中的数据结构

redis -> {
    payment_用户ID_课程ID: {
        'course_id': "1",
        'title': 'Python基础',
        'img': 'Python基础.jpg',
        'policy_id': '2',
        'coupon': {
            3: {
                'coupon_type': 2,
                'coupon_type_display': '折扣券',
                'off_percent': 90
            }
        },
        'default_coupon': 0,
        'name': '2个月',
        'time': 60,
        'price': 1000.0
    },
    payment_用户ID_课程ID: {
        'course_id': 1,
        'title': 'Python基础',
        'img': 'Python基础.jpg',
        'policy_id': '2',  # 价格策略对应的ID
        'coupon': {
            折扣券ID: {
                'coupon_type': 2,
                'coupon_type_display': '折扣券',
                'off_percent': 90
            }
        },
        'default_coupon': 0,  # 默认不选择折扣券
        'name': '2个月',  # 价格策略对应的周期
        'time': 60,  # 价格策略对应的时长
        'price': 1000.0  # 价格策略对应的价格
    },
    payment_global_coupon_用户ID: {  # 用户可用的通用优惠券
        'coupon': {
            2: {'money_equivalent_value': 200},  # 优惠券 ID ：{优惠券信息}
        },
        'default_coupon': 0
    }
}
"""


class PaymentView(APIView):
    """结算中心"""
    authentication_classes = [TokenAuth, ]
    conn = get_redis_connection('default')

    def post(self, request, *args, **kwargs):
        """
        进入结算中心
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        results = BaseResponse()
        try:
            user_id = request.user.id  # 用户认证过后用  user_id = request.user.id 来获取
            course_id_list = request.data.get('course_id')
            course_dict = {}  # 所有课程的信息(课程信息+优惠券信息)
            global_coupon_dict = {  # 通用的优惠券信息
                "coupon": {},
                "default_coupon": 0
            }
            # 0.每次进结算中心之前，先清空 redis 中已经有的该用户的结算信息，再写入。
            # key_list = self.conn.keys(settings.PAYMENT_COURSE_KEY.format(user_id, "*"))
            # self.conn.delete(*key_list)
            keys = self.conn.scan_iter(settings.PAYMENT_COURSE_KEY.format(user_id, "*"),
                                       count=100)  # 获取该用户的课程、优惠券信息的key
            for key in keys:
                self.conn.delete(key)  # 删除该用户的课程、优惠券信息的key
            self.conn.delete(settings.PAYMENT_GLOBAL_COUPON_KEY.format(user_id))  # 删除该用户的通用优惠券信息的 key

            # 1 根据课程ID去redis中购物车获取相应的课程信息（含价格策略价格）
            for course_id in course_id_list:
                redis_car_keys = settings.SHOPPING_CART_KEY.format(user_id, course_id)
                # 1.1检查用户要结算的课程是否已经在购物车
                if not self.conn.exists(redis_car_keys):
                    results.code = 2001
                    results.error = "购物车中不存在该课程"
                    return Response(results.dict)
                # 1.2取到价格策略信息
                default_policy = self.conn.hget(redis_car_keys, "default_policy").decode('utf-8')
                policy = json.loads(self.conn.hget(redis_car_keys, "policy").decode('utf-8'))  # 转换成 字符串再loads成字典
                policy_info = policy[default_policy]

                payment_course_dict = {  # 单课程信息+优惠券信息
                    "course_id": str(course_id),
                    "title": self.conn.hget(redis_car_keys, "title").decode('utf-8'),
                    "img": self.conn.hget(redis_car_keys, "img").decode('utf-8'),
                    "policy_id": str(default_policy),
                    "coupon": {},
                    "default_coupon": 0,
                }
                payment_course_dict.update(policy_info)  # 将 字典policy_info 里的键值对 添加到 payment_course_dict中
                course_dict[str(course_id)] = payment_course_dict

            # 2.获取优惠券相关（当前用户可用的所有优惠券），
            ctime = datetime.date.today()  # 2019-02-21  优惠券在截止日期当天可用
            # 2.1 去数据库获取到符合要求的优惠券列表
            coupon_list = models.CouponRecord.objects.filter(
                account=models.UserInfo.objects.get(id=user_id),  # 该用户的所有优惠券 用户认证过后用  account=request.user来获取
                status=0,  # 未使用的
                coupon__valid_begin_date__lte=ctime,  # 数据库的优惠券使用起始时间 小于等于 当前时间
                coupon__valid_end_date__gte=ctime,  # 数据库的优惠券使用结束时间 大于等于 当前时间
            )
            # 2.2 根据绑定课程和通用处理优惠券分类处理
            for item in coupon_list:
                coupon_course_id = item.coupon.object_id  # 绑定的课程ID
                coupon_id = item.id  # 优惠券ID
                coupon_type = item.coupon.coupon_type  # 优惠券类型
                info = {}
                #  2.2.1 处理通用优惠券
                if not coupon_course_id:  # 绑定的课程ID 为空。
                    if coupon_type == 0:  # 通用类 优惠券
                        info["money_equivalent_value"] = item.coupon.money_equivalent_value  # 等值
                    elif coupon_type == 0:  # 满减券
                        info["money_equivalent_value"] = item.coupon.money_equivalent_value  # 等值
                        info["minimum_consume"] = item.coupon.minimum_consume  # 最低消费
                    else:  # 折扣券
                        info["off_percent"] = item.coupon.off_percent  # 折扣百分比
                    global_coupon_dict["coupon"][coupon_id] = info
                    continue

                # 2.2.2 处理绑定课程的优惠券
                info["coupon_type"] = coupon_type
                info["coupon_type_display"] = item.coupon.get_coupon_type_display()
                if coupon_type == 0:  # 通用类 优惠券
                    info["money_equivalent_value"] = item.coupon.money_equivalent_value  # 等值
                elif coupon_type == 0:  # 满减券
                    info["money_equivalent_value"] = item.coupon.money_equivalent_value  # 等值
                    info["minimum_consume"] = item.coupon.minimum_consume  # 最低消费
                else:  # 折扣券
                    info["off_percent"] = item.coupon.off_percent  # 折扣百分比
                # 将绑定课程的优惠券放到对应的课程信息里
                if str(coupon_course_id) not in course_dict:  # 不添加 有课程优惠券，但没有买课程的
                    continue
                course_dict[str(coupon_course_id)]["coupon"][coupon_id] = info  # 将优惠券设置到绑定的课程信息中。

            # 3 将所有的信息写入到 redis 中（结算中心）
            # 3.1 课程与优惠券
            for item in course_dict:
                redis_payment_course_key = settings.PAYMENT_COURSE_KEY.format(user_id, item)
                course_dict[item]["coupon"] = json.dumps(course_dict[item]["coupon"])  # 将内部的字典 json
                self.conn.hmset(redis_payment_course_key, course_dict[item])
            # 3.2 通用优惠券
            redis_payment_global_coupon_key = settings.PAYMENT_GLOBAL_COUPON_KEY.format(user_id)
            global_coupon_dict['coupon'] = json.dumps(global_coupon_dict['coupon'])  # 将内部的字典 json
            self.conn.hmset(redis_payment_global_coupon_key, global_coupon_dict)

            results.data = "添加结算信息成功"
        except Exception as e:
            results.code = 1001
            results.error = "添加结算失败"
        return Response(results.dict)

    def get(self, request, *args, **kwargs):
        """
        页面刷新get请求，展示结算中心
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        results = BaseResponse()
        try:
            user_id = request.user.id  # 用户认证过后用  user_id = request.user.id 来获取

            # 1 获取课程、优惠券信息
            redis_payment_course_key = settings.PAYMENT_COURSE_KEY.format(user_id, "*")
            course_list = []
            for key in self.conn.scan_iter(redis_payment_course_key):
                info = {}
                data = self.conn.hgetall(key)
                for k, v in data.items():
                    kk = k.decode('utf-8')
                    if kk == 'coupon':
                        info[kk] = json.loads(v.decode('utf-8'))
                        continue
                    info[kk] = v.decode('utf-8')
                course_list.append(info)

            # 2 获取通用优惠券信息
            redis_payment_global_coupon_key = settings.PAYMENT_GLOBAL_COUPON_KEY.format(user_id)
            global_coupon_dict = {
                'coupon': json.loads(self.conn.hget(redis_payment_global_coupon_key, 'coupon').decode('utf-8')),
                "default_coupon": self.conn.hget(redis_payment_global_coupon_key, "default_coupon").decode('utf-8')
            }

            results.data = {
                'course_list': course_list,
                "global_coupon_dict": global_coupon_dict,
            }
        except Exception as e:
            results.code = 1001
            results.error = "获取结算数据失败"
        return Response(results.dict)

    def patch(self, request, *args, **kwargs):
        """
        更新优惠券
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        results = BaseResponse()
        try:
            user_id = request.user.id  # 用户认证过后用  user_id = request.user.id 来获取
            course_id = str(request.data.get('course_id'))  # 取不到时 就是 字符串类型的 None
            coupon_id = str(request.data.get('coupon_id'))

            # 如果没有传 课程ID 就是修改通用优惠券
            redis_payment_global_coupon_key = settings.PAYMENT_GLOBAL_COUPON_KEY.format(user_id)
            if course_id == 'None':
                if coupon_id == '0':  # 不使用优惠券
                    self.conn.hset(redis_payment_global_coupon_key, "default_coupon", coupon_id)
                    results.data = "不使用通用优惠券"
                    return Response(results.dict)
                # 使用 通用优惠券。先判断优惠券是否合法
                coupon_dict = json.loads(self.conn.hget(redis_payment_global_coupon_key, "coupon").decode('utf-8'))
                if coupon_id not in coupon_dict:  # 用户传的优惠券ID 不存在
                    results.code = 2001
                    results.error = "通用优惠券不合法"
                    return Response(results.dict)
                self.conn.hset(redis_payment_global_coupon_key, "default_coupon", coupon_id)  # 通用优惠券合法
                results.data = "使用通用优惠券成功"
                return Response(results.dict)

            # 修改绑定课程的优惠券
            redis_payment_course_key = settings.PAYMENT_COURSE_KEY.format(user_id, course_id)
            if not self.conn.exists(redis_payment_course_key):  # 如果 key 不存在，及用户课程不存在
                results.code = 2002
                results.error = "课程不合法"
                return Response(results.dict)
            if coupon_id == '0':  # 不使用课程优惠券
                self.conn.hset(redis_payment_course_key, "default_coupon", coupon_id)
                results.data = "不使用课程优惠券"
                return Response(results.dict)
            # 使用课程优惠券, 判断该课程是否有此优惠券
            coupon_dict = json.loads(self.conn.hget(redis_payment_course_key, "coupon").decode('utf-8'))  # 取到优惠券字典
            if coupon_id not in coupon_dict:  # 不存在此优惠券
                results.code = 2003
                results.error = "课程优惠券不合法"
                return Response(results.dict)
            self.conn.hset(redis_payment_course_key, "default_coupon", coupon_id)
            results.data = "使用课程优惠券成功"
        except Exception as e:
            results.code = 1001
            results.error = "更新优惠券失败"
        return Response(results.dict)


class OrderView(APIView):
    """支付"""

    def post(self, request, *args, **kwargs):
        """支付"""
        """
        1. 获取用户提交数据
              {
                  balance:1000,
                  money:900
              }
         balance = request.data.get("balance")
         money = request.data.get("money")
        
        2. 数据验证
          - 大于等于0
          - 个人账户是否有1000贝里
        
          if user.auth.user.balance < balance:
              账户贝里余额不足
        
        优惠券ID_LIST = [1,3,4]
        总价
        实际支付
        3. 去结算中获取课程信息
          for course_dict in redis的结算中获取：
              # 获取课程ID
              # 根据course_id去数据库检查状态
        
              # 获取价格策略
              # 根据policy_id去数据库检查是否还依然存在
        
              # 获取使用优惠券ID
              # 根据优惠券ID检查优惠券是否过期
        
              # 获取原价+获取优惠券类型
                  - 立减
                      0 = 获取原价 - 优惠券金额
                      或
                      折后价格 = 获取原价 - 优惠券金额
                  - 满减：是否满足限制
                      折后价格 = 获取原价 - 优惠券金额
                  - 折扣：
                      折后价格 = 获取原价 * 80 / 100
        
        4. 全站优惠券
          - 去数据库校验全站优惠券的合法性
          - 应用优惠券：
              - 立减
                  0 = 实际支付 - 优惠券金额
                  或
                  折后价格 =实际支付 - 优惠券金额
              - 满减：是否满足限制
                  折后价格 = 实际支付 - 优惠券金额
              - 折扣：
                  折后价格 = 实际支付 * 80 / 100
          - 实际支付
        5. 贝里抵扣
        
        6. 总金额校验
          实际支付 - 贝里 = money:900
        
        7. 为当前课程生成订单(数据库事务回滚)
        
              - 订单表创建一条数据 Order
                  - 订单详细表创建一条数据 OrderDetail   EnrolledCourse
                  - 订单详细表创建一条数据 OrderDetail   EnrolledCourse
                  - 订单详细表创建一条数据 OrderDetail   EnrolledCourse
        
              - 如果有贝里支付
                  - 贝里金额扣除  Account
                  - 交易记录     TransactionRecord
        
              - 优惠券状态更新   CouponRecord
        
              注意：
                  如果支付宝支付金额0，  表示订单状态：已支付
                  如果支付宝支付金额110，表示订单状态：未支付
                      - 生成URL（含订单号）
                      - 回调函数：更新订单状态

        """

        return