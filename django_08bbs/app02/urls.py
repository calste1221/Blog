#!/usr/bin/env python
#coding:utf-8
from django.conf.urls import include, url
from django.contrib import admin

from app02 import views



urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #注意下面(\d*)后面的斜杠应该去掉，这样访问index时候不会出错
    url(r'^login/',views.login),
    url(r'^logout/',views.logout),
    url(r'^register/',views.register),
    #url(r'^index/',views.index),
    url(r'^catIndex/',views.catIndex),
    url(r'^addfavor/',views.addfavor),
    url(r'^getreply/',views.getreply),
    url(r'^submitreply/',views.submitreply),
    url(r'^submitchat/',views.submitchat),
    url(r'^getchat/',views.getchat),
    url(r'^getchat2/',views.getchat2),
    
    
]