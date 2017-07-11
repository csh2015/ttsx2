#coding=utf-8
from django.shortcuts import render
from models import *
# Create your views here.
# 商品查询
def index(request):
    # 分类当中去查询两组数据：1, 最新的商品；2.点击量最高的商品
    type_list=TypeInfo.objects.all()      # 获得所有的分类，
    list1=[]
    for type1 in type_list:
        new_list=type1.goodsinfo_set.order_by('-id')[0:4]   # 按照最新的商品进行降序排列
        click_list=type1.goodsinfo_set.order_by('-gclick')[0:4]    # 根据点击量来进行降序排列
        list1.append({'new_list':new_list,'click_list':click_list,'t1':type1})     #往列表当中添加字典
    context={'list1':list1,'title':'首页','cart_show':'1'}      # 往html页面当中传递的参数
    return render(request,'ttsx_goods/index.html',context)

def goods_list(request, tid):     #tid为分类的对象
    t1 = TypeInfo.objects.get(pk=int(tid))
    # 查最新的两个分类
    new_list = t1.goodsinfo_set.order_by('-id')[0:2]
    context={'cart_show':'1','title':'商品列表','t1':t1,'new_list':new_list}
    return render(request,'ttsx_goods/list.html',context)




