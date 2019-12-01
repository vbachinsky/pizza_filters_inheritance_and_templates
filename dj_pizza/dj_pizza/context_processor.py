# coding=utf-8
from django.conf import settings
from dj_pizzas.models import Pizza


def contex_core(request):
    return {'pizzas': Pizza.objects.all(),}
