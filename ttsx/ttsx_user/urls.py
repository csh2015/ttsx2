from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$',views.register),
    url(r'^register_handle/$',views.register_handle),
    url(r'^login/$',views.login),
    url(r'^login_handle/$',views.login_handle),
    url(r'^$',views.center),
    url(r'^order/$',views.order),
    url(r'^site/$',views.site),
    url(r'^logout/$',views.logout),
    url(r'^islogin/$',views.islogin)
]

