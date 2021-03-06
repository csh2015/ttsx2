# coding=utf-8
"""ttsx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/',include('ttsx_user.urls')),
    url(r'^',include('ttsx_goods.urls')),   # 什么都不添的时候就显示首页
    url(r'^tinymce/',include('tinymce.urls')),
    #url(r'^search/', include('haystack.urls')),   #配置全文检索的url
    url(r'^cart/',include('ttsx_cart.urls')),
]
