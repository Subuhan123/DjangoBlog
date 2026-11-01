from django.db import models
from django.conf import settings
from django.utils import timezone
from mdeditor.fields import MDTextField


class Club(models.Model):
    """社团"""
    name = models.CharField('社团名称', max_length=50, unique=True)
    description = models.TextField('简介', blank=True)
    logo = models.ImageField('Logo', upload_to='club_logo/', blank=True, null=True)
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='led_clubs', verbose_name='负责人'
    )
    founded_date = models.DateField('成立时间', default=timezone.now)
    is_active = models.BooleanField('是否招新中', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'campus_club'
        verbose_name = '社团'
        verbose_name_plural = '社团'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Activity(models.Model):
    """活动"""
    STATUS_CHOICES = [
        ('open', '报名中'),
        ('full', '已满'),
        ('ended', '已结束'),
        ('canceled', '已取消'),
    ]

    title = models.CharField('活动标题', max_length=100)
    club = models.ForeignKey(
        Club, on_delete=models.CASCADE,
        related_name='activities', verbose_name='所属社团'
    )
    description = models.TextField('活动详情', blank=True)
    cover = models.ImageField('封面', upload_to='activity_cover/', blank=True, null=True)
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')
    location = models.CharField('活动地点', max_length=100)
    capacity = models.PositiveIntegerField('人数上限', default=50)
    signup_deadline = models.DateTimeField('报名截止')
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'campus_activity'
        verbose_name = '活动'
        verbose_name_plural = '活动'
        ordering = ['-start_time']

    def __str__(self):
        return self.title

    @property
    def approved_count(self):
        """已通过报名人数"""
        return self.signups.filter(status='approved').count()

    @property
    def is_full(self):
        return self.approved_count >= self.capacity


class Signup(models.Model):
    """活动报名"""
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('canceled', '已取消'),
    ]

    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE,
        related_name='signups', verbose_name='活动'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='signups', verbose_name='报名用户'
    )
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='pending')
    remark = models.CharField('备注', max_length=200, blank=True)
    created_at = models.DateTimeField('报名时间', auto_now_add=True)

    class Meta:
        db_table = 'campus_signup'
        verbose_name = '活动报名'
        verbose_name_plural = '活动报名'
        unique_together = ('activity', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} -> {self.activity}'


class CourseNote(models.Model):
    """课程笔记"""
    title = models.CharField('标题', max_length=100)
    course = models.CharField('课程名', max_length=50)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='course_notes', verbose_name='作者'
    )
    content = MDTextField('内容')
    is_public = models.BooleanField('是否公开', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'campus_course_note'
        verbose_name = '课程笔记'
        verbose_name_plural = '课程笔记'
        ordering = ['-updated_at']

    def __str__(self):
        return self.title
