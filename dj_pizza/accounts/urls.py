# coding=utf-8

from .views import *
from django.conf.urls import url, include
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^login/$', EmailLoginView.as_view(), name="email-login"),
    url(r'^profile/$', ProfileView.as_view(), name="profile-url"),
    url(r'^forgot-password/$', ForgotPasswordView.as_view(), name="forgot-password-url"),
    url(r'^change-password/token=(?P<token>\w+)$', ChangePasswordView.as_view(), name="change-password-url"),
    url(r'^confirm-registration/token=(?P<token>\w+)$', ConfirmRegistrationView.as_view(), name="confirm-registration-url"),
    url(r'^registration/$', RegistrationView.as_view(), name="registration-url"),
    url(r'^logout/$', LogoutView.as_view(), name="logout-view"),
    url(r'^switch_user/$', SwitchUser.as_view(), name="switch-user-url"),
]
