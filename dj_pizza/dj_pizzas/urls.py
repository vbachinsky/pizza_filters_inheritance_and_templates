from django.conf.urls import url
from django.urls import path
from . import views
from dj_pizzas.views import *

#It creates a scheme for ExampleModels
#dj_pizzas/urls.py

urlpatterns = [
	path('', Home.as_view(), name='home'),
	path('create_topping/', CreateTopping.as_view(), name='create_topping'),
	path('create_order/', CreateOrder.as_view(), name='create_order'),
	path('create_snacks/', CreateSnacks.as_view(), name='create_snacks'),
	path('create_dough/', CreateDough.as_view(), name='create_dough'),

	path('toppings/', ListToppings.as_view(), name='list_toppings'),
	path('orders/', ListOrders.as_view(), name='list_orders'),
	path('snacks/', ListSnacks.as_view(), name='list_snacks'),
	path('dough/', ListDough.as_view(), name='list_dough'),

	path('toppings/<int:pk>/edit', UpdateTopping.as_view(), name='update_topping'),
	path('orders/<int:pk>/edit', UpdateOrder.as_view(), name='update_order'),
	path('snacks/<int:pk>/edit', UpdateSnack.as_view(), name='update_snacks'),
	path('dough/<int:pk>/edit', UpdateDough.as_view(), name='update_dough'),

	path('update/', CommonToppingUpdate.as_view(), name='common_update'),
	path('sorter/', ToppingSorter.as_view(), name='sorter'),
]