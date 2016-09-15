from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.core import serializers
from app1 import models
import datetime
import json
# Create your views here.


def Filter(before_func, after_func):
    def outer(main_func):
        def wrapper(request, *args, **kwargs):
            before_result = before_func(request, *args, **kwargs)
            if(before_result != None):
                return before_result
            main_result = main_func(request, *args, **kwargs)
            if(main_result != None):
                return main_result
            after_result = after_func(request, *args, **kwargs)
            if(after_result != None):
                return after_result
        return wrapper
    return outer


def before(request):
    data = {'status': 0, 'message':''}
    if 'current_user_id' not in request.session:
        data['message'] = '请先登录!'
        return HttpResponse(json.dumps(data))


def after(request):
    pass


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            currentObj = models.Admin.objects.get(username=username,password=password)
        except Exception as e:
            currentObj = None
        if currentObj:
            request.session['current_user_id'] = currentObj.id
            return redirect('/index/')
        else:
            data = {'message': '用户名或密码错误！'}
            return render_to_response('login.html')
    return render_to_response('login.html')


def index(request):
    all_data = models.News.objects.all()
    return render_to_response('index.html',{'data': all_data})


def addfavor(request):
    ret = {'status':0, 'data':'', 'message':''}
    try:
        id = request.POST.get('nid')
        newsObj = models.News.objects.get(id=id)
        temp = newsObj.favor_count + 1
        newsObj.favor_count = temp
        newsObj.save()
        ret['status'] = 1
        ret['data'] = temp
    except Exception as e:
        ret['message'] = e.args
    return HttpResponse(json.dumps(ret))


class CJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, o)


def getreply(request):
    id = request.POST.get('nid')
    reply_list = models.Reply.objects.filter(new__id=id).values('id','content','create_date','user__username')
    reply_list = list(reply_list)
    return HttpResponse(json.dumps(reply_list,cls=CJsonEncoder))


@Filter(before, after)
def submitreply(request):
    ret = {'status':0, 'data':'', 'message':''}
    try:
        nid = request.POST.get('nid')
        data = request.POST.get('data')
        newObj = models.News.objects.get(id=nid)
        obj = models.Reply.objects.create(content=data,
                                    user=models.Admin.objects.get(id=request.session['current_user_id']),
                                    new=models.News.objects.get(id=nid))
        temp = newObj.reply_count + 1
        newObj.reply_count = temp
        newObj.save()
        ret['status'] = 1
        ret['data'] = {'content': obj.content, 'user_username':obj.user.username,
                       'create_date': obj.create_date.strftime('%Y-%m-%d %H:%M:%S'),
                       'reply_count':temp}
    except Exception as e:
        ret['message'] = e.args
    return HttpResponse(json.dumps(ret))


@Filter(before, after)
def submitchat(request):
    ret = {'status': 0, 'data': '', 'message': ''}
    try:
        value = request.POST.get('data')
        chatObj = models.Chat.objects.create(content=value,
                                   user=models.Admin.objects.get(id=request.session['current_user_id']),
                                   )
        ret['status']=1
        ret['data']={
                    'id': chatObj.id,
                    'username': chatObj.user.username,
                     'content':chatObj.content,
                     'create_date':chatObj.create_date.strftime('%Y-%m-%d %H:%M:%S')
                     }
    except Exception as e:
        ret['message']=e.args
    return HttpResponse(json.dumps(ret))


def getchat(request):
    chatObj = models.Chat.objects.all().order_by('-id')[0:10].values('id', 'content', 'user__username', 'create_date')
    chatObj = list(chatObj)
    chatObj = json.dumps(chatObj, cls=CJsonEncoder)
    return HttpResponse(chatObj)


def getchat2(request):
    last_id = request.POST.get('last_id')
    chatObj = models.Chat.objects.filter(id__gt=last_id).values('id', 'content', 'user__username', 'create_date')
    chatObj = list(chatObj)
    chatObj = json.dumps(chatObj, cls=CJsonEncoder)
    return HttpResponse(chatObj)


@Filter(before, after)
def username(request):
    data = {'status':1, 'user': ''}
    id = request.session['current_user_id']
    data['user'] = models.Admin.objects.get(id=id).username
    return HttpResponse(json.dumps(data))


def logout(request):
    try:
        del request.session['current_user_id']
        return HttpResponse(json.dumps(None))
    except Exception as e:
        return HttpResponse(json.dumps(e.args))
