"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from apps.users.views import LoginView,LogoutView,DynamicLoginView,SendSmsView
from apps.organizations.views import OrgView
from django.views.decorators.csrf import csrf_exempt
import xadmin


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('',  TemplateView.as_view(template_name='index.html'),name='index'),
    path('login/',  LoginView.as_view(),name='login'),
    path('d_login/', DynamicLoginView.as_view(), name="d_login"),
    path('logout/',  LogoutView.as_view(),name='logout'),
    path('captcha/', include('captcha.urls')),
    path('send_sms/', csrf_exempt(SendSmsView.as_view()), name="send_sms" ),
    path('org_list/',OrgView.as_view(), name="org_list" ),
]
