#coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator    # 导入分页包
# Create your views here.
# 商品查询
def index(request):
    # 分类当中去查询两组数据：1, 最新的商品；2.点击量最高的商品
    type_list=TypeInfo.objects.all()      # 获得所有的分类，
    list1=[]     #创建一个列表，用来存储最新商品和根据点击量排序的商品的键值对
    for type1 in type_list:    #遍历分类，创建type1对象
        new_list=type1.goodsinfo_set.order_by('-id')[0:4]   # 按照最新的商品进行降序排列
        click_list=type1.goodsinfo_set.order_by('-gclick')[0:4]    # 根据点击量来进行降序排列
        list1.append({'new_list':new_list,'click_list':click_list,'t1':type1}) # type1为实际分类对象    #往列表当中添加字典
    context={'list1':list1,'title':'首页','cart_show':'1'}      # 往html页面当中传递的参数
    return render(request,'ttsx_goods/index.html',context)

def goods_list(request, tid ,pindex ,orderby):   #三个参数分别为分类.页码,排序规则
    #tid为分类的对象,从url中的d+参数传递过来
    t1 = TypeInfo.objects.get(pk=int(tid))   #获得类别 ,
    orderby_str = '-id'   #默认按照id进行降序排序
    desc = '1'
    if int(orderby) == 2:    # 当参数为2时，默认按照价格排列
        desc = request.GET.get('desc')     # 通过GET方法从服务器中获得desc的值
        if desc == '1':    #根据价格进行降序排列
            orderby_str = '-gprice'
        else:
            orderby_str = 'gprice'  #根据价格进行升序排列
    elif int(orderby) == 3:    # 当参数为3时，默认按照人气（点击次数）降序排列
        orderby_str = '-gclick'

    # 查最新的两个分类
    new_list = t1.goodsinfo_set.order_by('-id')[0:2]     # 新品推荐,降序排列
    glist = t1.goodsinfo_set.order_by(orderby_str)    #搜索到的商品,goodsinfo_set通过外键指向t1获得所有的商品
    paginator = Paginator(glist, 10)   # 创建分页对象，对商品进行分页
    # 做页码判断
    pindex1 = int(pindex)
    if pindex1 <= 1:
        pindex1 = 1
    if pindex1 >= paginator.num_pages:
        pindex1 = paginator.num_pages

    page = paginator.page(int(pindex1))         # 获取分页对象，拿到分页的索引数据
    context={'cart_show':'1','title':'商品列表','t1':t1,'new_list':new_list,'page':page,'orderby':orderby,'desc':desc}
    return render(request,'ttsx_goods/list.html',context)

def detail(request,id):
    try:
        goods = GoodsInfo.objects.get(pk = int(id))
        # 此处涉及到一对多的查找，#找到商品所对应的分类中的所有的商品，降序排列之后并找到其中最新的两个
        new_list = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context = {'cart_show': 1, 'title': '商品详细信息', 'new_list': new_list, 'goods': goods}
        response= render(request, 'ttsx_goods/detail.html', context)
        # 最近浏览 <-->1,2,3,4,5 ，存入到cookie中，缓解服务器压力 ，用列表存储5次浏览记录
        # 从本地浏览器中向服务器拿cookie值，由键拿值,对id进行切分
        ids = request.COOKIES.get('goods_ids','').split(',')
        if id in ids:
            ids.remove(id)   #如果当前id在列表中，将这个id去掉，
        ids.insert(0,id)     # 将此id加到最前面，即可满足最近浏览的呈现需求
        if len(ids)>5:   # 如果id大于5个则将最后一个弹出，以保证只有5个
            ids.pop()        #下一步将ids用逗号进行拼接，形成一个只包含5个数的列表
        response.set_cookie('goods_ids',','.join(ids),max_age=60*60*24*7)  #用cookie存储的键值对和过期时间
        return response
    except:
        return render(request,'404.html')




