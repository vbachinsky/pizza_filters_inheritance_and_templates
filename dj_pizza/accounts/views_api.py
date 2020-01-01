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


class UserAPI(View):
    pass