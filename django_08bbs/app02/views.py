#!/usr/bin/env python
#coding:utf-8
from django.shortcuts import render,render_to_response,redirect
from app02 import models
from django.http.response import HttpResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

#from datetime import datetime
import datetime
from mimify import repl
#from distutils.tests.setuptools_build_ext import if_dl


class CJsonEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, datetime.datetime):
            #时间格式化
            return obj.strftime('%Y-%m-%d %H:%M%S')
        elif isinstance(obj,datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return obj.JSONEncoder.default(self,obj)
# Create your views here.
 
def login(request):
    ret={'login_flag':0,'username':''}
    if request.method == 'POST':
        #get 从对话框输入的，或者是从前端其他地方传来的值
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            currentObj = models.Admin.objects.get(username = username,password = password)

        except Exception,e:
            currentObj = None
        if currentObj:
            #这个id就是这个用户在Admin表中的id，而且是唯一的，将这个存入seesion中，直到退出时进行销毁
            request.session['current_user_id'] = currentObj.id
            ret['username'] = username
            ret['login_flag'] = 1
            return redirect('/app02/catIndex/',ret)

        else: 
            ret['login_flag'] = 0
            ret['status'] = '请输入正确的用户名和密码'
            return render_to_response('app02/login.html',ret)
        
    return render_to_response('app02/login.html',ret)

def logout(request):
    ret = {'login_flag':0}
    ret['login_flag'] = 0
    del request.session['current_user_id']
        
    return redirect('/app02/catIndex/',ret)
    

def register(request):
    ret = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        passwordagain = request.POST.get('passwordagain')
        email = request.POST.get('email')
        if password != passwordagain:
            ret['status'] = '两次密码输入不一致，请重新输入'
            return render_to_response('app02/register.html',ret)
        
        try:
            currentObj = models.Admin.objects.get(username = username,password = password)
        except Exception,e:
            currentObj = None
        
        if currentObj:
            ret['status'] = '已存在该用户名，请填写其他用户名'
            return render_to_response('app02/register.html',ret)
        else:
             models.Admin.objects.create(username=username,
                                         password=password,
                                         email=email,
                                         user_type_id = models.UserType.objects.get(display='manage').id)
  
             ret['status'] = '你已注册成功,  请登录！'
             return render_to_response('app02/register.html',ret)
    return render_to_response('app02/register.html',ret)



def catIndex(request):
    ret={'login_flag':0,'data':'','username':''}
    all_data = models.News.objects.all()   
    ret['data'] = all_data
    user_dict = request.session.get('current_user_id',None)

    if not user_dict:
        ret['message'] = '你还未登录，请先登录！'
        ret['login_flag'] = 0
    else:
        username = models.Admin.objects.get(id=user_dict)
        ret['username'] = username        
        ret['login_flag'] = 1
 
    return render_to_response('app02/catIndex.html',ret) 

def addfavor(request):
    ret = {'status':0,'data':'','message':''}
    user_dict = request.session.get('current_user_id',None)
    
    
    if not user_dict:
        ret['message'] = '请先登录'
     
    
    else:    
        try:
            #从前端传来的数据，nid是新闻的id，
            id = request.POST.get('nid')
            #前端点击率某个新闻id的赞，所以现在后端要获取这个新闻id的赞的个数有多少，加1后返回去
            #其实newObj是News的一个对象，里面含有
            newsObj = models.News.objects.get(id=id)
            temp = newsObj.favor_count + 1
            newsObj.favor_count = temp
            newsObj.save()
            ret['status'] = 1
            ret['data'] = temp
            
        except Exception,e:
            ret['message'] = e.message
    
    return HttpResponse(json.dumps(ret))


#获取某条新闻的回复，或者是获取回复中的指定内容

def getreply(request):
    
    #从前端传来的数据，nid是新闻的id，
    id = request.POST.get('nid')
    #获取到这条新闻的内容，然后取出其中一些。
    reply_list = models.Reply.objects.filter(new__id=id).values('id','content','create_date','user__username')
    #reply_list = models.Reply.objects.filter(new__id=id)
    #json.dumps()只能python提供的数据结构，而reply_list是django提供的一个类或者一个对象
    #reply_list = list(reply_list)这是方法之一，但是date那里还是无法序列化，所以用django提供的序列号包
    #假如调试的时候想看错误信息，那么可以使用try来看看
    #reply_list = serializers.serialize('json', reply_list)
    
    reply_list = list(reply_list)
    #因为json只能序列化字符串
    reply_list = json.dumps(reply_list,cls=CJsonEncoder)
    return HttpResponse(reply_list)

    
def submitreply(request):
    ret = {'status':0,'data':'','message':''}
    try:
        #新闻的id；data就是你在文本框输入的内容；将这条新闻的全部内容也就是对象获取到
        nid = request.POST.get('nid')
        data = request.POST.get('data')
        newObj = models.News.objects.get(id=nid)
        #然后在再将这条数据插入到数据库中
        obj = models.Reply.objects.create(content=data,
                                    user = models.Admin.objects.get(id=request.session['current_user_id']),
                                    new = newObj)
        temp = newObj.reply_count + 1
        newObj.reply_count = temp
        newObj.save()
        ret['data'] = {'reply_count':temp,'content':obj.content,'user__username':obj.user.username,'create_date':obj.create_date.strftime('%Y-%m-%d %H:%M:%S')}    
        ret['status'] = 1
    except Exception,e:
        ret['message'] = e.message
    return HttpResponse(json.dumps(ret))
    
    
def submitchat(request):
    ret = {'status':0,'data':'','message':''}
    try:
        #获取用户发的聊天内容
        value = request.POST.get('data')
        #当前登录的用户 request.session['current_user_id'] 记住，这是一个全局
        userObj = models.Admin.objects.get(id=request.session['current_user_id'])
        #将聊天内容，以及用户名称插入聊天记录表中，时间会自己生成
        chatObj = models.Chat.objects.create(content=value,user=userObj)
        #返回了聊天记录的id；
        ret['data'] = {'id':chatObj.id,'username':userObj.username,'create_date':chatObj.create_date.strftime('%Y-%m-%d %H:%M:%S')}    
        ret['status'] = 1
        
    except Exception,e:
        ret['message'] = e.message

    return HttpResponse(json.dumps(ret))     

     
def getchat(request):
    
    #-id是倒序的意思
    chatList = models.Chat.objects.all().order_by('-id')[0:10].values('id','content','user__username','create_date')
    chatList = list(chatList)
    chatList = json.dumps(chatList,cls=CJsonEncoder)
    return HttpResponse(chatList)

def getchat2(request):
    #最后一条新闻的id
    last_id = request.POST.get('lastid')   
    chatList = models.Chat.objects.filter(id__gt=last_id).values('id','content','user__username','create_date')
    chatList = list(chatList) 
    chatList = json.dumps(chatList,cls=CJsonEncoder)
    return HttpResponse(chatList)    
    
    
    
    
    