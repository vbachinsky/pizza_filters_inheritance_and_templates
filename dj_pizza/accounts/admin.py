# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from django.utils.safestring import mark_safe


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'login_as']
    list_filter = ['is_active', 'is_superuser', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)

    def login_as(self, obj):
        return mark_safe('<a href="/accounts/switch_user/?user={}" class="default" type="button" >login as</a>'.format(obj.user_secret_switch_key()))

    def save_model(self, request, obj, form, change):
        super(UserAdmin, self).save_model(request, obj, form, change)
        password = 'password' in form.changed_data
        if password:
            obj.password = make_password(form.cleaned_data.get('password'))
            obj.save()

admin.site.register(User, UserAdmin)
admin.site.register(ResetPasswordData)
