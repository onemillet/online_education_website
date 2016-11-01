# -*- coding:utf-8 -*-
from django import forms
from captcha.fields import CaptchaField
from common.models import UserProfile

class RegForm(forms.Form):
    '''
    注册表单
    '''
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}),
                              max_length=50,error_messages={"required": u"email不能为空","invalid":u"请输入正确的邮箱"})

    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=50,min_length=7,
                               error_messages={"required": "password不能为空",})
    captcha = CaptchaField()

    def clean(self):
        try:
            email=self.cleaned_data['email']
        except Exception as e:
            print 'except:'+str(e)
            raise forms.ValidationError(u"注册账号需为邮箱格式")

        # 登录验证
        is_email_exist = UserProfile.objects.filter(email=email).exists()
        if is_email_exist:
            raise forms.ValidationError(u"该账号已被注册")

        # 密码
        try:
            password = self.cleaned_data['password']
        except Exception as e:
            print 'except: ' + str(e)
            raise forms.ValidationError(u"请输入至少8位密码")

        return self.cleaned_data

class LoginForm(forms.Form):
    '''
    登录Form
    '''
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}),
                             max_length=50, error_messages={"required": "email不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                               max_length=50,min_length=7,
                               error_messages={"required": "password不能为空",})
