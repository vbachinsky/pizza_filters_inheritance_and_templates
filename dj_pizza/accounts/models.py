# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.db.models.manager import BaseManager
from django.core import signing


def unique_token_key():
    import uuid
    return str(uuid.uuid4().hex) + str(uuid.uuid4().hex)


class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    delete_date = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ["pk"]

    def __unicode__(self):
        return self.__str__()


class User(AbstractUser, BaseModel):
    email = models.EmailField('Email address', unique=True)
    token = models.CharField(default=unique_token_key(), max_length=300, null=True, blank=True)
    first_login = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __unicode__(self):
        return self.email

    def set_active(self):
        self.token = None
        self.is_active = True
        self.save()

    def user_secret_switch_key(self):
        return signing.dumps({settings.SWITCH_HASH_KEY: self.pk})

    @staticmethod
    def exists(email):
        return User.objects.filter(email=email).exists()

    @staticmethod
    def get_by_email(email):
        return User.objects.filter(email=email).first()

    @staticmethod
    def get_by_id(id):
        return User.objects.filter(id=id).first()

    @staticmethod
    def get_confirm_token(token):
        return User.objects.filter(token=token).first()

    @staticmethod
    def clean_user_pk_by_secret_switch_key(hash):
        return signing.loads(hash)


class ResetPasswordData(models.Model):
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.CASCADE)
    token = models.CharField(default=unique_token_key(), max_length=300, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    changed = models.BooleanField(default=False)

    @staticmethod
    def create_reset_data(user):
        reset_data = ResetPasswordData.objects.create(user=user, expiration_date=None)
        reset_data.expiration_date = reset_data.create_date + datetime.timedelta(hours=24)
        reset_data.save()
        return reset_data

    @staticmethod
    def get_by_token(token):
        return ResetPasswordData.objects.filter(token=token).first()

    @staticmethod
    def get_by_id(id):
        return ResetPasswordData.objects.filter(id=id).first()
