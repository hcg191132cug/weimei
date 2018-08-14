# -*- coding:utf-8 -*-
__author__ = 'Cliff Huang'
__date__ = '2018/4/23 2:02'
from django import forms

TRANS = {'phoneNum':'账号','passWd':'密码',
         'nickName':'昵称','address':'地址','gender':'性别','birthday':'生日',
         'regPhoneNum': '账号', 'regPassWd': '密码', 'verifyCode': '验证码',
         'image':'头像'}
class LoginForm(forms.Form):
    phoneNum = forms.CharField(required=True,error_messages={"手机号":"请输入11位手机号"})
    passWd = forms.CharField(required=True,min_length=6,error_messages={"密码":"至少是6位"})


class RegistForm(forms.Form):
    regPhoneNum = forms.CharField(required=True,min_length=11,max_length=11,error_messages={"手机号":"请输入11位手机号"})
    regPassWd = forms.CharField(required=True,min_length=6,error_messages={"密码":"至少是6位"})
    verifyCode = forms.CharField(required=True,min_length=6,error_messages={"验证码":"至少是6位数"})


class ModifyForm(forms.Form):
    nickName=forms.CharField(required=False,max_length=50,error_messages={"昵称":"过长"})
    address = forms.CharField(required=False,max_length=100,error_messages={"地址":"过长"})
    gender = forms.CharField(required=True,max_length=6)
    birthday = forms.DateField(required=False,error_messages={"正确的格式为":"2018-01-01"})


class ForgetPwForm(forms.Form):
    phoneNum = forms.CharField(required=True,min_length=11,max_length=11,error_messages={"手机号":"请输入11位手机号"})
    passWd = forms.CharField(required=True,min_length=6,error_messages={"密码":"至少是6位"})
    verifyCode = forms.CharField(required=True, min_length=6, error_messages={"验证码": "至少是6位数"})


class HeadImgForm(forms.Form):
    image = forms.ImageField()