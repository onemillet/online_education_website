#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2015/11/3
@author: yopoing
users模块的url配置。
"""

from django.conf.urls import patterns,url,include

urlpatterns = patterns('users.views',
    url(r'^register', 'users_register', name='register'),
    url(r'^login','users_login',name='login'),
    url(r'^forget','users_forget',name='forget'),
    url(r'^logout','users_logout',name='logout'),
    url(r'^info_email','info_email',name='info_email'),
    url(r'^stu_info_save','stu_info_save',name='stu_info_save'),
    url(r'^thr_info_save', 'thr_info_save', name='thr_info_save'),
    url(r'^change_password','change_password',name='change_password'),
    url(r'^email_finish_valid','email_finish_valid',name='email_finish_valid'),
    url(r'^change_email','change_email',name='change_email'),
    url(r'^find_password','find_password',name='find_password'),
    url(r'^find_change_pwd','find_change_pwd',name='find_change_pwd'),
)

# urlpatterns = [
#     url(r'^register','register',name='register'),
# ]
