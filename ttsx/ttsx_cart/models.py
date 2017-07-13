#coding=utf-8
from django.db import models
from ttsx_user.models import UserInfo
# Create your models here.
class CartInfo(models.Model):
    goods=models.ForeignKey('ttsx_goods.GoodsInfo')    #与用户是1对N
    user=models.ForeignKey(UserInfo)       #与商品是1对N
    count=models.IntegerField()