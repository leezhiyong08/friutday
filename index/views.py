import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *

# Create your views here.
def index_views(request):
    return render(request,'index.html')

# /login 对应的视图
def login_views(request):
    url = '/'
    if request.method == 'GET':
        # get 的流程
        # 判断session中是否有登录信息
        if 'uid' in request.session and 'uphone' in request.session:
            # session中有值,重定向回首页或原路径
            print('session中有数据')
            return redirect(url)
        else:
            # session中没有值
            # 判断cookie中是否有uid和uphone
            if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
                # cookie 中有登录信息
                # 从cookie中取出数据保存进session
                uid = request.COOKIES['uid']
                uphone = request.COOKIES['uphone']
                request.session['uid']=uid
                request.session['uphone']=uphone
                # 重定向到首页或原路径
                return redirect(url)
            else:
                # cookie 中没有登录信息
                # 去往登录页面
                form = LoginForm()
                return render(request,'login.html',locals())
    else:
        # post 的流程
        # 实现登录操作：取出uphone和upwd到db中判断
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        uList = Users.objects.filter(uphone=uphone,upwd=upwd)
        # if uList:
        if uphone=='13511225566' and upwd=='123456':
            # 登录成功
            # uid = uList[0].id
            # 取出 uphone 和 uid 保存进session
            uid = '01'
            request.session['uid'] = uid
            request.session['uphone'] = uphone
            # 判断是否有记住密码，记住密码的话则将值保存进cookie
            resp = redirect(url)
            if 'isSaved' in request.POST:
                # 记住密码，保存进cookie
                expires = 60 * 60 * 24 * 366
                resp.set_cookie('uid',uid,expires)
                resp.set_cookie('uphone',uphone,expires)
            # 重定向到首页或原路径
            return resp
        else:
            #登录失败 ： 回登录页
            form = LoginForm()
            errMsg = "用户名或密码不正确"
            return render(request,'login.html',locals())

# /register 对应的视图
def register_views(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        #实现注册的功能
        dic ={
            "uphone":request.POST['uphone'],
            "upwd":request.POST['upwd'],
            "uname":request.POST['uname'],
            "uemail":request.POST['uemail'],
        }
        #将数据插入进数据库 - 注册
        Users(**dic).save()
        #根据uphone的值再查询数据库
        u = Users.objects.get(uphone=request.POST['uphone'])
        #将用户id和uphone保存进session
        request.session['uid'] = u.id
        request.session['uphone'] = u.uphone

        return redirect('/')

# 检查手机号码是否存在 -> /check_uphone/
def check_uphone_views(request):
    if request.method == 'POST':
        #接收前端传递过来的手机号码
        uphone = request.POST['uphone']
        uList = Users.objects.filter(uphone=uphone)
        if uList:
            # 如果条件为真，则表示手机号码已经存在
            # 响应 status值为0，用于通知客户端手机号码已存在
            # 响应 text值为 “手机号码已存在”
            dic = {
                "status":"0",
                "text":'手机号码已存在',
            }
            return HttpResponse(json.dumps(dic))
        else:
            dic = {
                "status":"1",
                "text":"可以注册",
            }
            return HttpResponse(json.dumps(dic))

# 检查用户是否登录，如果有的话则取出uname的值
def check_login_views(request):
    # 判断 session 中是否有 uid 和 uphone
    if 'uid' in request.session and 'uphone' in request.session:
        # 用户此时处于登录状态
        # 根据 uid 获取 uname 的值
        uid = request.session['uid']
        user = Users.objects.get(id=uid)
        #处理响应数据
        dic = {
            "status":'1',
            'user':json.dumps(user.to_dict())
        }
        return HttpResponse(json.dumps(dic))
    else:
        # 判断cookie是否有登录信息
        if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
            # 从cookie中取出数据保存进session
            uid = request.COOKIES['uid']
            uphone = request.COOKIES['uphone']
            request.session['uid']=uid
            request.session['uphone']=uphone
            # 根据uid查询处对应的user信息转换成字典，响应给客户端
            user = Users.objects.get(id=uid)
            jsonStr = json.dumps(user.to_dict())

            dic = {
                "status":"1",
                "user":jsonStr,
            }
            return HttpResponse(json.dumps(dic))
        else:
            # session和cookie中都没有登录信息
            dic = {
                "status":0,
                'text':'用户尚未登录'
            }
            if request.method == 'POST':
                tmp_url = '/'
                uphone = request.POST['uphone']
                tmp_resp = redirect(tmp_url)
                tmp_expires = 60 * 60 * 24 * 366
                tmp_resp.set_cookie('uphone', uphone, tmp_expires)
                return redirect(tmp_url)
            return HttpResponse(json.dumps(dic))

# 退出登录
# 清除 session 和 cookie 中的数据
# 原路返回
def logout_views(request):
    #获取请求源地址，如果没有，则返回首页 /
    url = request.META.get('HTTP_REFERER','/')
    resp = redirect(url)
    # 判断 session 中是否有登录信息
    if 'uid' in request.session and 'uphone' in request.session:
        del request.session['uid']
        del request.session['uphone']
    if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
        resp.delete_cookie('uid')
        resp.delete_cookie('uphone')

    return resp

def type_goods_views(request):
    all_list=[]
    types=GoodsType.objects.all()
    for type in types:
        type_json=json.dumps(type.to_dic())
        g_list=type.goods_set.all()
        g_list_json=serializers.serialize('json',g_list)

        dic={
            'type':type_json,
            'goods':g_list_json,
        }
        all_list.append(dic)

    return HttpResponse(json.dumps(all_list))







