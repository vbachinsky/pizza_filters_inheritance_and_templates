from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from dj_pizzas.views import *

from django.views.decorators.cache import cache_page


#It creates a scheme for ExampleModels
#dj_pizzas/urls.py

urlpatterns = [
	path('', cache_page(1*1)(Home.as_view()), name='home'),
	path('create_topping/', CreateTopping.as_view(), name='create_topping'),
	path('create_snacks/', CreateSnacks.as_view(), name='create_snacks'),
	path('create_dough/', CreateDough.as_view(), name='create_dough'),
	path('add_pizza/', CreateBasket.as_view(), name='add_pizza'),

	path('basket/', ListOrders.as_view(), name='basket'),
	path('snacks/', ListSnacks.as_view(), name='list_snacks'),
	path('dough/', ListDough.as_view(), name='list_dough'),

	path('toppings/<int:pk>/edit', UpdateTopping.as_view(), name='update_topping'),
	path('orders/<int:pk>/edit', UpdateOrder.as_view(), name='update_order'),
	path('insttance_pizza/<int:pk>/edit', UpdateInstancePizza.as_view(), name='update_instance_pizza'),
	path('delete_insttance_pizza/<int:pk>/', DeleteInstancePizza.as_view(), name='delete_instance_pizza'),
	path('snacks/<int:pk>/edit', UpdateSnack.as_view(), name='update_snack'),
	path('dough/<int:pk>/edit', UpdateDough.as_view(), name='update_dough'),

	path('set_shipping/', SetShipping.as_view(), name='set_shipping'),

	path('update/', CommonToppingUpdate.as_view(), name='common_update'),
	url(r'^sorter/$', ToppingSorter.as_view(), name='sorter'),
]