# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from .models import User, ResetPasswordData
from .email_service import AccountsEmailService
from .forms import ChangePasswordForm, RegistrationForm, UserForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from django.conf import settings
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired


class LogoutView(View):

    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('/')


class EmailLoginView(TemplateView):

    template_name = 'accounts/login.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EmailLoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.get_by_email(email)
        if not user:
            context['error'] = True
            context['error_message'] = "User with this email does not exist"
            return render(request, self.template_name, context)

        login_password = authenticate(username=email, password=password)
        if not login_password:
            context['error'] = True
            context['error_message'] = "Please write correct password"
            return render(request, self.template_name, context)

        login(request, user)
        return redirect('/accounts/profile/')


class EmailLoginAPI(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EmailLoginAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        login_password = authenticate(username=email, password=password)
        if not login_password:
            return JsonResponse({'status': False, 'message': "User does not exist"})
        login(request, request.user)
        return JsonResponse({'authenticated': True})


class RegistrationView(TemplateView):

    template_name = 'accounts/registration.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    @never_cache
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = RegistrationForm(request.POST)
        context['form'] = form
        if form.is_valid():
            user = User(email=form.cleaned_data['email'], is_active=False, username=form.cleaned_data['email'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            AccountsEmailService.send_registration_email(user)
            context['success'] = True
            context['success_message'] = "Please look your email to continue registration"
        return render(request, self.template_name, context)


class ConfirmRegistrationView(TemplateView):

    template_name = 'accounts/confirm_registration.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user = User.get_confirm_token(kwargs.get('token'))
        if user:
            user.set_active()
            login(request, user)
            return redirect('/accounts/profile/?registration=completed')
        context['error'] = True
        context['error_message'] = "Invalid token"
        return render(request, self.template_name, context)


class ForgotPasswordView(TemplateView):

    template_name = 'accounts/forgot_password.html'

    @never_cache
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        email = request.POST.get('email')
        user = User.get_by_email(email)
        context['email_form'] = email
        if user:
            reset_data = ResetPasswordData.create_reset_data(user)
            AccountsEmailService.send_forgot_password(reset_data)
            context['success'] = True
            context['success_message'] = "Please look your email."
        else:
            context['error'] = True
            context['error_message'] = "User with this email does not exist"
        return render(request, self.template_name, context)


class ChangePasswordView(TemplateView):

    template_name = 'accounts/change_password.html'

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)
        context['context'] = {'change_password': True}
        context['token'] = kwargs.get('token')
        return context

    @never_cache
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        reset_data = ResetPasswordData.get_by_token(context['token'])
        if not reset_data or timezone.now() > reset_data.expiration_date:
            context['expired'] = True
        return render(request, self.template_name, context)

    @never_cache
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        reset_data = ResetPasswordData.get_by_token(context['token'])
        current_time = timezone.now()
        form = ChangePasswordForm(request.POST)
        context['form'] = form

        if not reset_data or current_time > reset_data.expiration_date:
            context['expired'] = True
            return render(request, self.template_name, context)

        if reset_data and form.is_valid():
            password = form.cleaned_data['new_password']
            user = reset_data.user
            user.set_password(password)
            user.save()
            reset_data.expiration_date = current_time
            reset_data.changed = True
            reset_data.save()
            return redirect(reverse('email-login', ), permanent=True)
        return render(request, self.template_name, context)


class ProfileView(TemplateView):

    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['registration_completed'] = self.request.GET.get('registration')
        context['form'] = UserForm(instance=self.request.user)
        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return render(request, self.template_name, context)


class SwitchUser(View):

    def get(self, request, **kwargs):
        try:
            if request.user.is_authenticated and request.user.is_superuser:
                loaded_data = User.clean_user_pk_by_secret_switch_key(request.GET.get('user'))
                user = User.get_by_id(loaded_data.get(settings.SWITCH_HASH_KEY))
                login(request, user)
            return redirect('/')
        except (ValueError, BadSignature):
            return redirect('/')