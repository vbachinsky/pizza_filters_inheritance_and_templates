# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from dj_pizzas.models import Topping, Dough, Pizza, InstancePizza, Snacks, OrderedSnacks, Order, OrderPayment, ClientAccount, ClientAccountPerson, Employee, ClientTransaction


admin.site.register(Order)
admin.site.register(Topping)
admin.site.register(Dough)
admin.site.register(Pizza)
admin.site.register(InstancePizza)
admin.site.register(Snacks)
admin.site.register(OrderedSnacks)
admin.site.register(OrderPayment)
admin.site.register(ClientAccount)
admin.site.register(ClientAccountPerson)
admin.site.register(Employee)
admin.site.register(ClientTransaction)
