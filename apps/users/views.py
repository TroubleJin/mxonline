from django.shortcuts import render,redirect
from django.views.generic.base import View
from apps.users.forms import LoginForm
from django.contrib.auth import authenticate,logout,login
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

class LogoutView(View):
    def get(self,requset,*args,**kwargs):
        logout(requset)
        return HttpResponseRedirect(reverse('index'))

class LoginView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request,'login.html')

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