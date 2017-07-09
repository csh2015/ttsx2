#coding=utf-8
# 这里创建一个装饰器来进行对登陆之后保存用户名，用于访问和用户有关视图的验证
from django.shortcuts import redirect
def user_islogin(func):
    def func1(request,*args,**kwargs):       # *args是从url中小括号中提取的值，而**kwargs是p<>中提取的键值对
        #判断是否登录
        if request.session.has_key('uid'):
            #如果登录，则执行func函数
            return func(request,*args,**kwargs)
        else:
            #如果没登录，则转到login视图/user/login/
            return redirect('/user/login/')
    return func1
