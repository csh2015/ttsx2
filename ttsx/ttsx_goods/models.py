# coding=utf-8
from django.db import models
from tinymce.models import HTMLField
# Create your models here.

class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode('utf-8')

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)    #标题
    gpic = models.ImageField(upload_to='goods/')     #图片，需要设置上传路径
    gprice = models.DecimalField(max_digits=5, decimal_places=2) #最大价格不超过5位数，最多两位小数
    gclick = models.IntegerField()      #点击数来展现人气
    gunit = models.CharField(max_length=10)  #单位
    isDelete = models.BooleanField(default=False)
    gsubtitle = models.CharField(max_length=200)    #副标题
    gkucun = models.IntegerField(default=100)    #库存
    gcontent = HTMLField()        #评论，用富文本编辑器
    gtype = models.ForeignKey('TypeInfo')    # 创建外键
