#!/usr/bin/env python
#coding:utf-8
from django.conf.urls import include, url
from django.contrib import admin





urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #注意下面(\d*)后面的斜杠应该去掉，这样访问index时候不会出错
        
]