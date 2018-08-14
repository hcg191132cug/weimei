# -*- coding:utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from clothes.models import Clothes
# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="名称",default="",null=True,blank=True)
    birthday = models.DateField(verbose_name="生日", null=True,blank=True)
    gender = models.CharField(verbose_name="性别", choices=(("male","男"),("female","女")),default="female",max_length = 6)
    address = models.CharField(verbose_name="地址", max_length=100,default="",null=True)
    mobile = models.CharField(verbose_name="电话", max_length=11,null=False,default='',blank=False,unique=True)
    reg_date = models.DateField(verbose_name='注册时间', null=False, default=datetime.now)

    def user_path(self,file_name):
        return 'image/user/user_{0}/{1}'.format(self.mobile, file_name)

    image = models.ImageField(verbose_name="头像", upload_to=user_path,default="image/default.png",max_length=100)
    fav = models.ManyToManyField(Clothes, related_query_name="user", related_name="users", verbose_name="收藏")

    class Meta:
        verbose_name = "客户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class MobileVerifyRecord(models.Model):
    code = models.CharField(max_length=10,verbose_name="验证码")
    phone = models.CharField(verbose_name="电话",max_length=11)
    send_type = models.CharField(choices=(("register","注册"),("forget","密码找回")),max_length=16,verbose_name="类型")
    send_time = models.DateTimeField(default=datetime.now,verbose_name="发送时间")

    class Meta:
        verbose_name = "手机验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        template = '{0.phone},{0.code}'
        return template.format(self)

