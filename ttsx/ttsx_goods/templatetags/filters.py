#coding=utf-8
# 自定义过滤器
#引入注册对象
from django.template import Library
register=Library()

#使用装饰器进行注册
@register.filter
def multi(num1):
    return int(num1)*-1