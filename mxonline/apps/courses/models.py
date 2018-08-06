# _*_ encoding:utf-8 _*_
from django.db import models
from datetime import datetime
from organization.models import CourseOrg,Teacher


class Course(models.Model):
    course_org=models.ForeignKey(CourseOrg,verbose_name=u'课程机构',null=True,blank=True)
    name=models.CharField(max_length=50,verbose_name=u'课程名')
    desc=models.CharField(max_length=300,verbose_name=u'课程描述')
    detail=models.TextField(verbose_name=u'课程详情')
    is_banner=models.BooleanField(default=False,verbose_name=u'是否轮播')
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name=u'讲师',null=True,blank=True)
    degree=models.CharField(verbose_name=u'难度',choices=(('cj',u'初级'),('zj',u'中级'),('gj','高级')),max_length=2)
    learn_times=models.IntegerField(default=0,verbose_name=u'学习时长（分钟数）')
    students=models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums=models.IntegerField(default=0,verbose_name=u'收藏人数')
    image=models.ImageField(upload_to='courses/%y/%m',verbose_name=u'封面图',max_length=100)
    click_nums=models.IntegerField(default=0,verbose_name=u'点击数')
    categery=models.CharField(max_length=20,verbose_name=u'课程类别',default=u"后端开发")
    tag=models.CharField(default="",verbose_name=u"课程标签",max_length=10)
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    youneed_know=models.CharField(max_length=300,verbose_name=u'课程须知',default="")
    teacher_tell=models.CharField(max_length=300,verbose_name=u'课程老师提示须知',default="")

    class Meta:
        verbose_name=u'课程'
        verbose_name_plural=verbose_name

    def get_zj_nums(self):
        """获取课程当前数目"""
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        """获取课程所有章节"""
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name=u'课程')
    name=models.CharField(max_length=100,verbose_name=u'章节名')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'章节'
        verbose_name_plural=verbose_name

    def get_lesson_video(self):
        """获取章节视频"""
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson=models.ForeignKey(Lesson,on_delete=models.CASCADE,verbose_name=u'章节')
    learn_times=models.IntegerField(default=0,verbose_name=u'学习时长（分钟数）')
    name=models.CharField(max_length=100,verbose_name=u'视频名')
    url=models.CharField(max_length=200,default="",verbose_name=u'访问地址')
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'视频'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name=u'课程')
    name=models.CharField(max_length=100,verbose_name=u'名称')
    download=models.FileField(upload_to='course/resource/%y/%m',verbose_name=u'资源文件',max_length=100)
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name=u'资源名称'
        verbose_name_plural=verbose_name



