from django.conf.urls import url
from django.urls import path
from . import views
from dj_pizzas.views import *

#It creates a scheme for ExampleModels
#dj_pizzas/urls.py

urlpatterns = [
	path('create_topping/', CreateTopping.as_view(), name='create'),
	path('', Home.as_view(), name='home'),
	path('toppings/', ListToppings.as_view(), name='list'),
	path('toppings/<int:pk>/edit', UpdateTopping.as_view(), name='update_topping'),
	path('update/', CommonToppingUpdate.as_view(), name='common_update'),
	path('sorter/', ToppingSorter.as_view(), name='sorter'),
]