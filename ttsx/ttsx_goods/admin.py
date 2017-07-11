#coding=utf-8
from django.contrib import admin
from models import *

# Register your models here.

class TypeAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle']  # 呈现出id和标题

admin.site.register(TypeInfo,TypeAdmin)   # 括号里为模型类，和显示方式


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'gtitle','gprice']  # 呈现出id和标题以及价格
    list_per_page = 15

admin.site.register(GoodsInfo, GoodsAdmin)  # 括号里为模型类，和显示方式