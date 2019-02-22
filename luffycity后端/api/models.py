from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.db import models
import hashlib


# ########################### 1. 课程相关 ################################
class CourseCategory(models.Model):
    """课程大类, e.g 前端  后端..."""
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name_plural = "01.课程大类"


class CourseSubCategory(models.Model):
    """课程子类, e.g python linux """
    category = models.ForeignKey("CourseCategory")
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name_plural = "02.课程子类"


class DegreeCourse(models.Model):
    """学位课程"""
    name = models.CharField(max_length=128, unique=True)
    course_img = models.CharField(max_length=255, verbose_name="缩略图")
    brief = models.TextField(verbose_name="学位课程简介", )
    total_scholarship = models.PositiveIntegerField(verbose_name="总奖学金(贝里)", default=40000)
    mentor_compensation_bonus = models.PositiveIntegerField(verbose_name="本课程的导师辅导费用(贝里)", default=15000)
    period = models.PositiveIntegerField(verbose_name="建议学习周期(days)", default=150)  # 为了计算学位奖学金
    prerequisite = models.TextField(verbose_name="课程先修要求", max_length=1024)
    teachers = models.ManyToManyField("Teacher", verbose_name="课程讲师")

    # 用于GenericForeignKey反向查询， 不会生成表字段，切勿删除
    coupon = GenericRelation("Coupon")

    # 用于GenericForeignKey反向查询，不会生成表字段，切勿删除
    degreecourse_price_policy = GenericRelation("PricePolicy")

    # 查询常见问题
    asked_question = GenericRelation("OftenAskedQuestion")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "03.学位课"


class Teacher(models.Model):
    """讲师、导师表"""
    name = models.CharField(max_length=32)
    role_choices = ((0, '讲师'), (1, '导师'))
    role = models.SmallIntegerField(choices=role_choices, default=0)
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, help_text="导师签名", blank=True, null=True)
    image = models.CharField(max_length=128)
    brief = models.TextField(max_length=1024, verbose_name='导师简介')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "04.导师或讲师"


class Scholarship(models.Model):
    """学位课程奖学金"""
    degree_course = models.ForeignKey("DegreeCourse")
    time_percent = models.PositiveSmallIntegerField(verbose_name="奖励档位(时间百分比)", help_text="只填百分值，如80,代表80%")
    value = models.PositiveIntegerField(verbose_name="奖学金数额")

    def __str__(self):
        return "%s:%s" % (self.degree_course, self.value)

    class Meta:
        verbose_name_plural = "05.学位课奖学金"


class Course(models.Model):
    """专题课程 OR 学位课模块"""
    name = models.CharField(max_length=128, unique=True, verbose_name="课程名称")  # Python基础
    course_img = models.CharField(max_length=255)

    sub_category = models.ForeignKey("CourseSubCategory")  # 课程所属子类

    course_type_choices = ((0, '付费'), (1, 'VIP专享'), (2, '学位课程'))
    course_type = models.SmallIntegerField(choices=course_type_choices)

    degree_course = models.ForeignKey("DegreeCourse", blank=True, null=True, help_text="若是学位课程，此处关联学位表")

    brief = models.TextField(verbose_name="课程（模块）概述", max_length=2048)
    level_choices = ((0, '初级'), (1, '中级'), (2, '高级'))
    level = models.SmallIntegerField(choices=level_choices, default=1)
    pub_date = models.DateField(verbose_name="发布日期", blank=True, null=True)
    period = models.PositiveIntegerField(verbose_name="建议学习周期(days)", default=7)
    order = models.IntegerField("课程顺序", help_text="从上一个课程数字往后排")
    attachment_path = models.CharField(max_length=128, verbose_name="课件路径", blank=True, null=True)
    status_choices = ((0, '上线'), (1, '下线'), (2, '预上线'))
    status = models.SmallIntegerField(choices=status_choices, default=0)
    template_id = models.SmallIntegerField("前端模板id", default=1)

    # 如果是专题课时，获取相关优惠券
    coupon = GenericRelation("Coupon")

    # 用于GenericForeignKey反向查询，不会生成表字段，切勿删除
    price_policy = GenericRelation("PricePolicy")

    # 查询常见问题
    asked_question = GenericRelation("OftenAskedQuestion")

    def __str__(self):
        return self.name

    class Meta:
        # verbose_name = '用户信息'
        verbose_name_plural = '课程信息'


class CourseDetail(models.Model):
    """课程详情页内容"""
    course = models.OneToOneField("Course")
    hours = models.IntegerField("课时")
    course_slogan = models.CharField(max_length=125, blank=True, null=True, verbose_name='课程口号')
    video_brief_link = models.CharField(verbose_name='课程介绍', max_length=255, blank=True, null=True)
    why_study = models.TextField(verbose_name="为什么学习这门课程")
    what_to_study_brief = models.TextField(verbose_name="我将学到哪些内容")
    career_improvement = models.TextField(verbose_name="此项目如何有助于我的职业生涯")
    prerequisite = models.TextField(verbose_name="课程先修要求", max_length=1024)
    recommend_courses = models.ManyToManyField("Course", related_name="recommend_by", blank=True, verbose_name='推荐课程')
    teachers = models.ManyToManyField("Teacher", verbose_name="课程讲师")

    def __str__(self):
        return "%s" % self.course

    class Meta:
        verbose_name_plural = "07.课程或学位模块详细"


class OftenAskedQuestion(models.Model):
    """常见问题"""
    content_type = models.ForeignKey(ContentType)  # 关联course or degree_course
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    question = models.CharField(max_length=255)
    answer = models.TextField(max_length=1024)

    def __str__(self):
        return "%s-%s" % (self.content_object, self.question)

    class Meta:
        unique_together = ('content_type', 'object_id', 'question')
        verbose_name_plural = "08. 常见问题"


class CourseOutline(models.Model):
    """课程大纲"""
    course_detail = models.ForeignKey("CourseDetail")

    # 前端显示顺序
    order = models.PositiveSmallIntegerField(default=1)

    title = models.CharField(max_length=128)
    content = models.TextField("内容", max_length=2048)

    def __str__(self):
        return "%s" % self.title

    class Meta:
        unique_together = ('course_detail', 'title')
        verbose_name_plural = "09. 课程大纲"


class CourseChapter(models.Model):
    """课程章节"""
    course = models.ForeignKey("Course", related_name='coursechapters')
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128)
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        unique_together = ("course", 'chapter')
        verbose_name_plural = "10. 课程章节"

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)


class CourseSection(models.Model):
    """课时目录"""
    chapter = models.ForeignKey("CourseChapter", related_name='coursesections')
    name = models.CharField(max_length=128)
    order = models.PositiveSmallIntegerField(verbose_name="课时排序", help_text="建议每个课时之间空1至2个值，以备后续插入课时")
    section_type_choices = ((0, '文档'), (1, '练习'), (2, '视频'))
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices)
    # 59EE3275E977AADB9C33DC5901307461
    section_link = models.CharField(max_length=255, blank=True, null=True, help_text="若是video，填vid,若是文档，填link")

    video_time = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)  # 仅在前端展示使用
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField("是否可试看", default=False)

    class Meta:
        unique_together = ('chapter', 'section_link')
        verbose_name_plural = "11. 课时"

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)


class Homework(models.Model):
    chapter = models.ForeignKey("CourseChapter")
    title = models.CharField(max_length=128, verbose_name="作业题目")
    order = models.PositiveSmallIntegerField("作业顺序", help_text="同一课程的每个作业之前的order值间隔1-2个数")
    homework_type_choices = ((0, '作业'), (1, '模块通关考核'))
    homework_type = models.SmallIntegerField(choices=homework_type_choices, default=0)
    requirement = models.TextField(max_length=1024, verbose_name="作业需求")
    threshold = models.TextField(max_length=1024, verbose_name="踩分点")
    recommend_period = models.PositiveSmallIntegerField("推荐完成周期(天)", default=7)
    scholarship_value = models.PositiveSmallIntegerField("为该作业分配的奖学金(贝里)")
    note = models.TextField(blank=True, null=True, verbose_name='笔记')
    enabled = models.BooleanField(default=True, help_text="本作业如果后期不需要了，不想让学员看到，可以设置为False")

    class Meta:
        unique_together = ("chapter", "title")
        verbose_name_plural = "12. 章节作业"

    def __str__(self):
        return "%s - %s" % (self.chapter, self.title)


class PricePolicy(models.Model):
    """价格与有课程效期表"""
    content_type = models.ForeignKey(ContentType)  # 关联course or degree_course
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # course = models.ForeignKey("Course")
    valid_period_choices = ((1, '1天'), (3, '3天'),
                            (7, '1周'), (14, '2周'),
                            (30, '1个月'),
                            (60, '2个月'),
                            (90, '3个月'),
                            (180, '6个月'), (210, '12个月'),
                            (540, '18个月'), (720, '24个月'),
                            )
    valid_period = models.SmallIntegerField(choices=valid_period_choices)
    price = models.FloatField()

    class Meta:
        unique_together = ("content_type", 'object_id', "valid_period")
        verbose_name_plural = "15. 价格策略"

    def __str__(self):
        return "%s(%s)%s" % (self.content_object, self.get_valid_period_display(), self.price)


# ########################### 2. 深科技相关 ################################
class ArticleSource(models.Model):
    """文章来源"""
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name_plural = "16. 文章来源"

    def __str__(self):
        return self.name


class Article(models.Model):
    """文章资讯"""
    title = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="标题")
    source = models.ForeignKey("ArticleSource", verbose_name="来源")
    article_type_choices = ((0, '资讯'), (1, '视频'))
    article_type = models.SmallIntegerField(choices=article_type_choices, default=0)
    brief = models.TextField(max_length=512, verbose_name="摘要")
    head_img = models.CharField(max_length=255)
    content = models.TextField(verbose_name="文章正文")
    pub_date = models.DateTimeField(verbose_name="上架日期")
    offline_date = models.DateTimeField(verbose_name="下架日期")
    status_choices = ((0, '在线'), (1, '下线'))
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="状态")
    order = models.SmallIntegerField(default=0, verbose_name="权重", help_text="文章想置顶，可以把数字调大，不要超过1000")
    vid = models.CharField(max_length=128, verbose_name="视频VID", help_text="文章类型是视频, 则需要添加视频VID", blank=True, null=True)
    comment_num = models.SmallIntegerField(default=0, verbose_name="评论数")
    agree_num = models.SmallIntegerField(default=0, verbose_name="点赞数")
    view_num = models.SmallIntegerField(default=0, verbose_name="观看数")
    collect_num = models.SmallIntegerField(default=0, verbose_name="收藏数")

    # tags = models.ManyToManyField("Tags", blank=True, verbose_name="标签")
    date = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")

    position_choices = ((0, '信息流'), (1, 'banner大图'), (2, 'banner小图'))
    position = models.SmallIntegerField(choices=position_choices, default=0, verbose_name="位置")

    # comment = GenericRelation("Comment")

    class Meta:
        verbose_name_plural = "17. 文章"

    def __str__(self):
        return "%s-%s" % (self.source, self.title)


class Collection(models.Model):
    """收藏"""
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user_info = models.ForeignKey("UserInfo")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('content_type', 'object_id', 'user_info')
        verbose_name_plural = "18. 通用收藏表"


class Comment(models.Model):
    """通用的评论表"""
    content_type = models.ForeignKey(ContentType, blank=True, null=True, verbose_name="类型")
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    p_node = models.ForeignKey("self", blank=True, null=True, verbose_name="父级评论")
    content = models.TextField(max_length=1024)
    user_info = models.ForeignKey("UserInfo", verbose_name="会员名")
    disagree_number = models.IntegerField(default=0, verbose_name="踩")
    agree_number = models.IntegerField(default=0, verbose_name="赞同数")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = "19. 通用评论表"


# ########################### 3. 用户相关 ################################
class UserInfo(models.Model):
    # 用户信息表
    user = models.CharField(max_length=32, verbose_name='用户名')
    pwd = models.CharField(max_length=64, verbose_name='密码')

    uid = models.CharField(max_length=64, unique=True, help_text='微信用户绑定和CC视频统计')  # 与第3方交互用户信息时，用这个uid,以避免泄露敏感用户信息
    openid = models.CharField(max_length=128, blank=True, null=True)
    # 贝里余额
    balance = models.PositiveIntegerField(default=0, verbose_name="可提现和使用余额")

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

class UserToken(models.Model):
    # 用户 Token 表
    user = models.OneToOneField(to='UserInfo')
    token = models.CharField(max_length=64)


# ########################### 4. 奖惩相关 ################################

class ScoreRule(models.Model):
    """积分规则"""
    score_rule_choices = (
        (0, '未按时交作业'),
        (1, '未及时批改作业'),
        (2, '作业成绩'),
        (3, '未在规定时间内对学员进行跟进'),
        (4, '未在规定时间内回复学员问题'),
        (5, '收到学员投诉'),
        (6, '导师相关'),
        (7, '学位奖学金'),
    )
    rule = models.SmallIntegerField(choices=score_rule_choices, verbose_name="积分规则")
    score_type_choices = ((0, '奖励'), (1, '惩罚'), (2, '初始分配'))
    score_type = models.SmallIntegerField(choices=score_type_choices, verbose_name="奖惩", default=0)
    score = models.IntegerField(help_text="扣分数与贝里相等,若为0则代表规则的值可以从别处取得")
    # maturity_days = models.IntegerField("成熟周期", help_text="自纪录创建时开始计算")
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s-%s:%s" % (self.get_rule_display(), self.get_score_type_display(), self.score)

    class Meta:
        unique_together = ('rule', 'score_type')
        verbose_name_plural = "29. 奖惩规则"


class ScoreRecord(models.Model):
    """积分奖惩记录"""
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    degree_course = models.ForeignKey("DegreeCourse", blank=True, null=True, verbose_name="关联学位课程")
    score_rule = models.ForeignKey("ScoreRule", verbose_name="关联规则")
    account = models.ForeignKey("UserInfo", verbose_name="被执行人")
    score = models.IntegerField(
        verbose_name="金额(贝里)")  # 这里单独有一个字段存积分而不是从score_rule里引用的原因是考虑到如果引用的话， # 一旦score_rule里的积分有变更，那么所有用户的历史积分也会被影响
    received_score = models.IntegerField("实际到账金额贝里)", help_text="仅奖励用", default=0)
    balance = models.PositiveIntegerField(verbose_name="奖金余额(贝里)")

    maturity_date = models.DateField("成熟日期(可提现日期)")
    applied = models.BooleanField(default=False, help_text="奖赏纪录是否已被执行", verbose_name="是否已被执行")
    applied_date = models.DateTimeField(blank=True, null=True, verbose_name="事件生效日期")
    date = models.DateTimeField(auto_now_add=True, verbose_name="事件触发日期")
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s-%s - %s - %s 奖金余额:%s" % (self.id, self.score_rule, self.account, self.score, self.balance)

    class Meta:
        verbose_name_plural = "30. 奖惩记录"


# ########################### 5. 支付相关 ################################
class Coupon(models.Model):
    """优惠券生成规则"""
    name = models.CharField(max_length=64, verbose_name="活动名称")
    brief = models.TextField(blank=True, null=True, verbose_name="优惠券介绍")
    coupon_type_choices = ((0, '通用券'), (1, '满减券'), (2, '折扣券'))
    coupon_type = models.SmallIntegerField(choices=coupon_type_choices, default=0, verbose_name="券类型")

    """
    通用：
        money_equivalent_value=100
        off_percent=null
        minimum_consume=0
    满减：
        money_equivalent_value=100
        off_percent=null
        minimum_consume=1000
    折扣：
        money_equivalent_value=0
        off_percent=79
        minimum_consume=0
    """
    money_equivalent_value = models.IntegerField(verbose_name="等值货币")
    off_percent = models.PositiveSmallIntegerField(verbose_name="折扣百分比", help_text="只针对折扣券，例7.9折，写79", blank=True,
                                                   null=True)
    minimum_consume = models.PositiveIntegerField(verbose_name="最低消费", default=0, help_text="仅在满减券时填写此字段")

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField("绑定课程", blank=True, null=True, help_text="可以把优惠券跟课程绑定")
    content_object = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField("数量(张)", default=1)
    open_date = models.DateField("优惠券领取开始时间")
    close_date = models.DateField("优惠券领取结束时间")
    valid_begin_date = models.DateField(verbose_name="有效期开始时间", blank=True, null=True)
    valid_end_date = models.DateField(verbose_name="有效结束时间", blank=True, null=True)
    coupon_valid_days = models.PositiveIntegerField(verbose_name="优惠券有效期（天）", blank=True, null=True,
                                                    help_text="自券被领时开始算起")
    date = models.DateTimeField(auto_now_add=True, verbose_name="创建优惠券的日期")

    class Meta:
        verbose_name_plural = "31. 优惠券生成记录"

    def __str__(self):
        return "%s(%s)" % (self.get_coupon_type_display(), self.name)

    def save(self, *args, **kwargs):
        if not self.coupon_valid_days or (self.valid_begin_date and self.valid_end_date):
            if self.valid_begin_date and self.valid_end_date:
                if self.valid_end_date <= self.valid_begin_date:
                    raise ValueError("valid_end_date 有效期结束日期必须晚于 valid_begin_date ")
            if self.coupon_valid_days == 0:
                raise ValueError("coupon_valid_days 有效期不能为0")
        if self.close_date < self.open_date:
            raise ValueError("close_date 优惠券领取结束时间必须晚于 open_date优惠券领取开始时间 ")

        super(Coupon, self).save(*args, **kwargs)


class CouponRecord(models.Model):
    """优惠券发放、消费纪录"""
    coupon = models.ForeignKey("Coupon")
    number = models.CharField(max_length=64, unique=True, verbose_name="优惠券的编号")
    account = models.ForeignKey("UserInfo", verbose_name="拥有者")
    status_choices = ((0, '未使用'), (1, '已使用'), (2, '已过期'))
    status = models.SmallIntegerField(choices=status_choices, default=0)
    get_time = models.DateTimeField(verbose_name="领取时间", help_text="用户领取时间")
    used_time = models.DateTimeField(blank=True, null=True, verbose_name="使用时间")

    # order = models.ForeignKey("Order", blank=True, null=True, verbose_name="关联订单")  # 一个订单可以有多个优惠券

    class Meta:
        verbose_name_plural = "32. 用户优惠券"

    def __str__(self):
        return '%s-%s-%s' % (self.account, self.number, self.status)


class CourseSchedule(models.Model):
    """课程进度计划表,针对学位课程，每开通一个模块，就为这个学员生成这个模块的推荐学习计划表，后面的奖惩均按此表进行"""
    study_record = models.ForeignKey("StudyRecord")
    homework = models.ForeignKey("Homework")
    recommend_date = models.DateField("推荐交作业日期")

    def __str__(self):
        return "%s - %s - %s " % (self.study_record, self.homework, self.recommend_date)

    class Meta:
        unique_together = ('study_record', 'homework')
        verbose_name_plural = "33. 课程模块计划表（学位课）"


class EnrolledCourse(models.Model):
    """已报名课程,不包括学位课程"""
    account = models.ForeignKey("UserInfo")
    course = models.ForeignKey("Course", limit_choices_to=~Q(course_type=2))
    enrolled_date = models.DateTimeField(auto_now_add=True)
    valid_begin_date = models.DateField(verbose_name="有效期开始自")
    valid_end_date = models.DateField(verbose_name="有效期结束至")
    status_choices = ((0, '已开通'), (1, '已过期'))
    status = models.SmallIntegerField(choices=status_choices, default=0)
    order_detail = models.OneToOneField("OrderDetail")  # 使订单购买后支持 课程评价

    # order = models.ForeignKey("Order",blank=True,null=True)

    def __str__(self):
        return "%s:%s" % (self.account, self.course)

    class Meta:
        verbose_name_plural = "34. 报名专题课"


class DegreeRegistrationForm(models.Model):
    """学位课程报名表"""
    enrolled_degree = models.OneToOneField("EnrolledDegreeCourse")
    current_company = models.CharField(max_length=64, )
    current_position = models.CharField(max_length=64, )
    current_salary = models.IntegerField()
    work_experience_choices = ((0, "应届生"),
                               (1, "1年"),
                               (2, "2年"),
                               (3, "3年"),
                               (4, "4年"),
                               (5, "5年"),
                               (6, "6年"),
                               (7, "7年"),
                               (8, "8年"),
                               (9, "9年"),
                               (10, "10年"),
                               (11, "超过10年"),
                               )
    work_experience = models.IntegerField()
    open_module = models.BooleanField("是否开通第1模块", default=True)
    stu_specified_mentor = models.CharField("学员自行指定的导师名", max_length=32, blank=True, null=True)
    study_plan_choices = ((0, "1-2小时/天"),
                          (1, "2-3小时/天"),
                          (2, "3-5小时/天"),
                          (3, "5小时+/天"),
                          )
    study_plan = models.SmallIntegerField(choices=study_plan_choices, default=1)
    why_take_this_course = models.TextField("报此课程原因", max_length=1024)
    why_choose_us = models.TextField("为何选路飞", max_length=1024)
    your_expectation = models.TextField("你的期待", max_length=1024)
    memo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "35. 报名表（学位课）"

    def __str__(self):
        return "%s" % self.enrolled_degree


class EnrolledDegreeCourse(models.Model):
    """已报名的学位课程"""
    account = models.ForeignKey("UserInfo")
    degree_course = models.ForeignKey("DegreeCourse")
    enrolled_date = models.DateTimeField(auto_now_add=True)
    valid_begin_date = models.DateField(verbose_name="有效期开始自", blank=True, null=True)  # 开通第一个模块时，再添加课程有效期，2年
    valid_end_date = models.DateField(verbose_name="有效期结束至", blank=True, null=True)
    status_choices = (
        (0, '在学中'),
        (1, '休学中'),
        (2, '已毕业'),
        (3, '超时结业'),
        (4, '未开始'),
        # (3, '其它'),
    )
    study_status = models.SmallIntegerField(choices=status_choices, default=0)
    mentor = models.ForeignKey("UserInfo", verbose_name="导师", related_name='my_students',
                               blank=True, null=True, limit_choices_to={'role': 1})
    mentor_fee_balance = models.PositiveIntegerField("导师费用余额", help_text="这个学员的导师费用，每有惩罚，需在此字段同时扣除")
    order_detail = models.OneToOneField("OrderDetail")  # 使订单购买后支持填写报名表

    def __str__(self):
        return "%s:%s" % (self.account, self.degree_course)

    class Meta:
        unique_together = ('account', 'degree_course')
        verbose_name_plural = "36. 报名学位课"


class Order(models.Model):
    """订单"""
    payment_type_choices = ((0, '微信'), (1, '支付宝'), (2, '优惠码'), (3, '贝里'))
    payment_type = models.SmallIntegerField(choices=payment_type_choices)

    payment_number = models.CharField(max_length=128, verbose_name="支付第3方订单号", null=True, blank=True)
    order_number = models.CharField(max_length=128, verbose_name="订单号", unique=True)  # 考虑到订单合并支付的问题
    account = models.ForeignKey("UserInfo")
    actual_amount = models.FloatField(verbose_name="实付金额")

    status_choices = ((0, '交易成功'), (1, '待支付'), (2, '退费申请中'), (3, '已退费'), (4, '主动取消'), (5, '超时取消'))
    status = models.SmallIntegerField(choices=status_choices, verbose_name="状态")
    date = models.DateTimeField(auto_now_add=True, verbose_name="订单生成时间")
    pay_time = models.DateTimeField(blank=True, null=True, verbose_name="付款时间")
    cancel_time = models.DateTimeField(blank=True, null=True, verbose_name="订单取消时间")

    class Meta:
        verbose_name_plural = "37. 订单表"

    def __str__(self):
        return "%s" % self.order_number


class OrderDetail(models.Model):
    """订单详情"""
    order = models.ForeignKey("Order")

    content_type = models.ForeignKey(ContentType)  # 可关联普通课程或学位
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    original_price = models.FloatField("课程原价")
    price = models.FloatField("折后价格")
    content = models.CharField(max_length=255, blank=True, null=True)  # ？
    valid_period_display = models.CharField("有效期显示", max_length=32)  # 在订单页显示
    valid_period = models.PositiveIntegerField("有效期(days)")  # 课程有效期
    memo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s - %s - %s" % (self.order, self.content_type, self.price)

    class Meta:
        verbose_name_plural = "38. 订单详细"
        unique_together = ("order", 'content_type', 'object_id')


class StudyRecord(models.Model):
    """学位课程的模块学习进度，报名学位课程后，每个模块会立刻生成一条学习纪录"""
    enrolled_degree_course = models.ForeignKey("EnrolledDegreeCourse")
    course_module = models.ForeignKey("Course", verbose_name="学位模块", limit_choices_to={'course_type': 2})
    open_date = models.DateField(blank=True, null=True, verbose_name="开通日期")
    end_date = models.DateField(blank=True, null=True, verbose_name="完成日期")
    status_choices = ((2, '在学'), (1, '未开通'), (0, '已完成'))
    status = models.SmallIntegerField(choices=status_choices, default=1)

    class Meta:
        verbose_name_plural = "39. 学习记录表（报名学位课程后，每个模块会立刻生成一条学习纪录）"
        unique_together = ('enrolled_degree_course', 'course_module')

    def __str__(self):
        return '%s-%s' % (self.enrolled_degree_course, self.course_module)

    def save(self, *args, **kwargs):
        if self.course_module.degree_course_id != self.enrolled_degree_course.degree_course_id:
            raise ValueError("学员要开通的模块必须与其报名的学位课程一致！")

        super(StudyRecord, self).save(*args, **kwargs)


class TransactionRecord(models.Model):
    """贝里交易纪录"""
    account = models.ForeignKey("UserInfo")
    amount = models.IntegerField("金额")
    # balance = models.IntegerField("账户余额")
    transaction_type_choices = ((0, '收入'), (1, '支出'), (2, '退款'), (3, "提现"))  # 2 为了处理 订单过期未支付时，锁定期贝里的回退
    transaction_type = models.SmallIntegerField(choices=transaction_type_choices)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="关联对象")
    content_object = GenericForeignKey('content_type', 'object_id')

    transaction_number = models.CharField(unique=True, verbose_name="流水号", max_length=128)
    date = models.DateTimeField(auto_now_add=True)
    memo = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        verbose_name_plural = "40. 贝里交易记录"

    def __str__(self):
        return "%s" % self.transaction_number


class HomeworkRecord(models.Model):
    """学员作业记录及成绩"""
    homework = models.ForeignKey("Homework")
    student = models.ForeignKey("EnrolledDegreeCourse", verbose_name="学生")
    score_choices = ((100, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (80, 'B'),
                     (70, 'B-'),
                     (60, 'C+'),
                     (50, 'C'),
                     (40, 'C-'),
                     (-1, 'D'),
                     (0, 'N/A'),
                     (-100, 'COPY'),
                     )
    score = models.SmallIntegerField(verbose_name="分数", choices=score_choices, null=True, blank=True)
    mentor = models.ForeignKey("UserInfo", related_name="my_stu_homework_record", limit_choices_to={'role': 1},
                               verbose_name="导师")
    mentor_comment = models.TextField(verbose_name="导师批注", blank=True, null=True)  # 导师
    status_choice = (
        (0, '待批改'),
        (1, '已通过'),
        (2, '不合格'),
    )
    status = models.SmallIntegerField(verbose_name='作业状态', choices=status_choice, default=0)

    submit_num = models.SmallIntegerField(verbose_name='提交次数', default=0)
    correct_date = models.DateTimeField('备注日期', blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    date = models.DateTimeField("作业提交日期", auto_now_add=True)

    check_date = models.DateTimeField("批改日期", null=True, blank=True)

    update_time = models.DateTimeField(auto_now=True, verbose_name="提交日期")

    # homework_path = models.CharField(verbose_name='作业路径', max_length=256,blank=True,null=True) 作业路径可以动态拿到，没必要存

    reward_choice = ((0, '新提交'),
                     (1, '按时提交'),
                     (2, '未按时提交'),
                     (3, '成绩已奖励'),
                     (4, '成绩已处罚'),
                     (5, '未作按时检测'),
                     )
    reward_status = models.SmallIntegerField(verbose_name='作业记录奖惩状态', default=0)

    def __str__(self):
        return "%s %s" % (self.homework, self.student)

    class Meta:
        verbose_name_plural = "41. 作业"
        unique_together = ("homework", "student")


class StuFollowUpRecord(models.Model):
    """学员跟进记录"""
    enrolled_degree_course = models.ForeignKey("EnrolledDegreeCourse", verbose_name="学生")
    mentor = models.ForeignKey("UserInfo", related_name='mentor', limit_choices_to={'role': 1}, verbose_name="导师")
    followup_tool_choices = ((0, 'QQ'), (1, '微信'), (2, '电话'), (3, '系统通知'))
    followup_tool = models.SmallIntegerField(choices=followup_tool_choices, default=1)
    record = models.TextField(verbose_name="跟进记录")
    attachment_path = models.CharField(max_length=128, blank=True, null=True, verbose_name="附件路径", help_text="跟进记录的截图等")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "42. 学员跟进记录"

    def __str__(self):
        return "%s --%s --%s" % (self.enrolled_degree_course, self.record, self.date)
