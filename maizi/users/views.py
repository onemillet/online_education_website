#coding:utf-8
from django.shortcuts import render,redirect,HttpResponse
from common.models import UserProfile
from .forms import RegForm,LoginForm
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt
import re
from captcha.models import CaptchaStore
from captcha.views import captcha_image_url
import forms
from forms import forms
from datetime import datetime

#获取表单错误信息
def getFormTips(form):
    errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
    if(len(errors)>0):
        err = errors.pop()
        if err:
            print type(err)
            if isinstance(err, str):
                print 'str'
            else:
                err = err.message
        print err
        return err
    else:
        return u'验证码输入错误'

# 设置表单提示信息
def setFormTips(form, content):
    if content and len(content)>0:
        errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(content)

#用户注册信息
@csrf_exempt
def users_register(request):
    if request.GET.get('newsn') == '1':
        csn = CaptchaStore.generate_key()
        cimageurl = captcha_image_url(csn)
        return HttpResponse(cimageurl)

    if request.method == 'POST':
        if (not request.POST.get('email')) or (not request.POST.get('password')):
            return HttpResponse(u'账号或密码不能为空')
        try:
            form=RegForm(request.POST)
        except Exception as e:
            print e
            err=u'注册失败，请重试'
            return HttpResponse(err)

        if form.is_valid():
            print 'success'
            try:
                human=True
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user=UserProfile.objects.create(email=email,password=make_password(password),
                                                username=datetime.now().strftime('%Y%m%d%H%M%S'))
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                # 验证成功登录
                login(request, user)
                #成功注册后向用户邮箱发送一封验证邮件
                subject='麦子学院邮箱注册验证'
                message='你好，你已注册了麦子学院的账号，请点击链接完成验证http://127.0.0.1:8000/users/email_finish_valid?id=%s'%(user.id)
                from_email='421830508@qq.com'
                user.email_user(subject,message,from_email,fail_silently=False)

                return HttpResponse("success")
            except Exception as e:
                print str(e)
                setFormTips(form, "注册失败，请重试")

        else:
            print "register failed"

            if request.POST.get('captcha_1') == "":
                setFormTips(form, "验证码不能为空")

        # 登录失败 返回错误提示
        err = getFormTips(form)
        return HttpResponse(err)
        #return HttpResponse('登录失败')

    form=RegForm()
    return render(request,'users/register.html',locals())


#用户登录
@csrf_exempt
def users_login(request):
    if request.method == 'POST':
        try:
            #提示账号密码为空，优先级最高
            if (not request.POST.get('email')) or (not request.POST.get('password')):
                error_notify=u'密码或账号不能为空'
                return HttpResponse(error_notify)

            form = LoginForm(request.POST)
            if form.is_valid():
                email=form.cleaned_data['email']
                password=form.cleaned_data['password']
                user = authenticate(email=email,password=password)
                if user is not None:
                    user.backend='django.contrib.auth.backends.ModelBackend'
                    try:
                        login(request,user)
                        return redirect('/')
                    except Exception as e:
                        print e

                #账号或密码错误，提示优先级第二高
                else:
                    error_notify = u'账号或密码错误，请重新输入'
                    return HttpResponse(error_notify)

            #其他原因导致的登录失败，优先级最低
            else:
                error_notify = u'登录失败，请重试'
                return HttpResponse(error_notify)

        # 其他原因导致的登录失败，优先级最低
        except Exception as e:
            print e
            error_notify = u'登录失败，请重试'
            return HttpResponse(error_notify)

    return HttpResponse(u'登录失败，请重试')

#用户找回密码
@csrf_exempt
def users_forget(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        pattern=re.compile('[a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+')
        user=UserProfile.objects.filter(email=email)

        if not email:
             return HttpResponse(u'请填写邮箱账号')
        if not pattern.match(email):
             return HttpResponse(u'账号需为邮箱格式')
        if not user:
            return HttpResponse(u'该账户不存在')

        #发送邮件,用sleep来模拟发送邮件过程
        user=UserProfile.objects.get(email=email)
        subject='麦子学院用户密码找回'
        message='请将此链接复制到浏览器地址栏，进入页面修改密码（如果直接点击可能会无法完成修改）：http://127.0.0.1:8000/users/find_password?id=%s'%(user.id)
        from_email = '421830508@qq.com'
        try:
            user.email_user(subject, message, from_email, fail_silently=False)
            return HttpResponse('success')
        except Exception as e:
            print e
            return HttpResponse(u'找回密码申请提交失败，请重试')

    return HttpResponse(u'找回密码申请提交失败，请重试')

#用户注销
def users_logout(request):
    try:
        logout(request)
    except Exception as e:
        print e
    return redirect(request.META['HTTP_REFERER'])

#用户个人信息页面（邮箱注册）
def info_email(request):
    #print(request.user.id)
    id = request.user.id
    if hasattr(request.user,'is_teacher'):
        if request.user.is_teacher():
            user = UserProfile.objects.get(id=id)
            last_name = user.last_name
            first_name=user.first_name
            province = user.province
            city = user.city
            qq = user.qq
            description=user.description
            position=user.position
            return render(request, 'users/info_thr_email.html', locals())
        else:
            user = UserProfile.objects.get(id=id)
            username = user.username
            province = user.province
            city = user.city
            qq = user.qq
            return render(request, 'users/info_stu_email.html', locals())
    else:
        return redirect('/')

#用户（学生）个人信息更改
@csrf_exempt
def stu_info_save(request):
    id=request.user.id
    username=request.POST.get('username')
    qq=request.POST.get('qq')
    city=request.POST.get('city')
    province=request.POST.get('province')

    UserProfile.objects.filter(id=id).update(username=username,province=province,
                                             city=city,qq=qq)
    #print(id,username,qq,city,province)
    return HttpResponse('success')

#用户（教师）个人信息更改
@csrf_exempt
def thr_info_save(request):
    id = request.user.id
    #username = request.POST.get('username')
    qq = request.POST.get('qq')
    city = request.POST.get('city')
    province = request.POST.get('province')
    description=request.POST.get('description')
    position=request.POST.get('position')
    last_name=request.POST.get('name')[0:1]
    first_name=request.POST.get('name')[1:]
    #print qq

    try:
        UserProfile.objects.filter(id=id).update( province=province,city=city,qq=qq,
                                              description=description,position=position,
                                              last_name=last_name,
                                             first_name=first_name)
    except Exception as e:
        print 10000000
        print e
    #print(id,username,qq,city,province)
    return HttpResponse('success')

#用户密码更改
@csrf_exempt
def change_password(request):
    id=request.user.id
    old1=request.POST.get('old_password1')
    old2=request.POST.get('old_password2')
    new_pwd=request.POST.get('new_password')

    if (not old1) or (not old2) or (not new_pwd):
        return HttpResponse(u'不能有空值')
    if not (old1 == old2):
        return HttpResponse(u'旧密码前后输入不一致')
    pattern_password = re.compile('(.){8,50}')
    if not pattern_password.match(new_pwd):
        return HttpResponse(u'新密码至少需要8位')

    now_pwd=UserProfile.objects.get(id=id).password
    if check_password(old1,now_pwd):
        try:
            UserProfile.objects.filter(id=id).update(password=make_password(new_pwd))
        except Exception as e:
            print(e)
            return HttpResponse(u'密码修改失败，请重试')
    else:
        return HttpResponse(u'密码修改失败，请重试')

    return HttpResponse('success')

#用户注册后完成邮箱验证
def email_finish_valid(request):
    id = request.GET.get('id')
    user=UserProfile.objects.get(id=id)
    user.valid_email=1
    user.save()
    return HttpResponse('注册验证完成，请返回麦子官网首页http://127.0.0.1:8000')

#用户修改邮箱
@csrf_exempt
def change_email(request):
    id=request.user.id
    email=request.POST.get('email')
    pattern = re.compile('[a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+')
    if not email:
        return HttpResponse('输入不能为空')
    if not pattern.match(email):
        return HttpResponse('请输入正确的邮箱格式')
    user=UserProfile.objects.get(id=id)
    user.email=email
    user.save()

    return HttpResponse('success')

#返回找密码的界面
def find_password(request):
    if request.method == 'GET':
        id=request.GET.get('id')
        return render(request,'users/find_pwd.html',{'user_id':id})

#处理找密码界面的修改操作
@csrf_exempt
def find_change_pwd(request):
    pwd1=request.POST.get('pwd1')
    pwd2=request.POST.get('pwd2')
    id=request.POST.get('id')
    pattern=re.compile('.{8,50}')
    print id

    if not pwd1==pwd2:
        return HttpResponse('两次输入的内容不同')
    if not pattern.match(pwd1):
        return HttpResponse('密码至少是8位')

    user=UserProfile.objects.get(id=id)
    print id
    user.password=make_password(pwd1)
    user.save()
    return HttpResponse('success')