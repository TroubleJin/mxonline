from django.shortcuts import render,redirect
from django.views.generic.base import View
from apps.users.forms import LoginForm,DynamicLoginForm,DynamicLoginPostForm
from django.contrib.auth import authenticate,logout,login
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from mxonline.settings import REDIS_HOST,REDIS_PORT
from apps.utils.random_str import generate_random
from apps.users.models import UserProfile
import redis
# Create your views here.

class LogoutView(View):
    def get(self,requset,*args,**kwargs):
        logout(requset)
        return HttpResponseRedirect(reverse('index'))

class LoginView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        login_form = DynamicLoginForm()
        return render(request,'login.html',
                      {"login_form": login_form})

    def post(self,request,*args,**kwargs ):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            print(user)
            if user is not None:
                # 查询到用户,登陆
                login(request,user)
                return HttpResponseRedirect(reverse("index"))
            else:
                #未查询到用户
                return render(request, "login.html", {"msg":"用户名或密码错误", "login_form": login_form})
        else:
            return  render(request,'login.html')

class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            # 假设生产验证码随机生成数字验证码
            code = generate_random(4, 0)
            print(code)
            r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
            r.set(str(mobile), code)
            r.expire(str(mobile), 60*5) #设置验证码五分钟过期
        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]

        return JsonResponse(re_dict)

class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        return render(request, "login.html",{
            "login_form":login_form,
            "next":next,
        })

    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        if login_form.is_valid():
            #没有注册账号依然可以登录
            mobile = login_form.cleaned_data["mobile"]
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                #新建一个用户
                user = UserProfile(username=mobile)
                password = generate_random(10, 2)
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)
            next = request.GET.get("next", "")
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse("index"))
        else:
            d_form = DynamicLoginForm()
            return render(request, "login.html", {"login_form": login_form,
                                                  "d_form": d_form,
                                                  "dynamic_login":dynamic_login})