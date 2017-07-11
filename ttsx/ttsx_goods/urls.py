# coding=utf-8
from django.conf.urls import url
import views

urlpatterns=[
    url('^$',views.index),
    url(r'^list(\d+)/$',views.goods_list),
]