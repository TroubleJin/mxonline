#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from captcha.fields import  CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


class DynamicLoginForm(forms.Form):
     captcha = CaptchaField( )