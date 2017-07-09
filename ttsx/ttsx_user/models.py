# coding=utf-8
from django.db import models


# Create your models here.

class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)      #sha1密码
    umail = models.CharField(max_length=30)
    ushou = models.CharField(default='',max_length=20)    # default设置为空字符串，是因为注册时没有传值
    uaddress = models.CharField(default='',max_length=100)
    ucode = models.CharField(default='',max_length=6)
    uphone = models.CharField(default='',max_length=11)


