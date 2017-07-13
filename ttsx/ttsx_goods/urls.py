# coding=utf-8
from django.conf.urls import url
import views
from search_view import MySearchView

urlpatterns=[
    url('^$',views.index),
    url(r'^list(\d+)_(\d+)_(\d+)/$',views.goods_list),
    url(r'^(\d+)',views.detail),     #展示商品的详细信息
    url('^search/$', MySearchView.as_view())
]