from django.shortcuts import render
from django.views.generic.base import View
from apps.users.forms import LoginForm
from django.contrib.auth import authenticate
# Create your views here.

class LoginView(View):
    def get(self,request,*args,**kwargs):
        return  render(request,'login.html')
    def post(self,request,*args,**kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user:
                return render(request,'index.html')
        else:
            return  render(request,'login.html')