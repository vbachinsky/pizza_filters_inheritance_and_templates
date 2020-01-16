from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from dj_pizzas.views import *
from dj_pizzas.models import *
from dj_pizzas.views_api import *
from dj_pizzas.views_rest_api import *
from dj_pizzas.serializers import *
from django.views.decorators.cache import cache_page
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'pizza', PizzaViewSet)
router.register(r'order', BasketViewSet)


urlpatterns = [
    path('', cache_page(60*1)(Home.as_view()), name='home'),
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
    url(r'^alarm', TemplateView.as_view(template_name='alarm.html')),

    # API URL
    path('pizza_api/', PizzaAPI.as_view(), name='pizza_api'),
    path('filter_pizza_api/', FilterPizzaAPI.as_view(), name='sorter_pizza_api'),
    path('basket_api/', BasketAPI.as_view(), name='basket_api'),
    path('update_basket_api/', UpdateBasketAPI.as_view(), name='update_basket_api'),
    path('topping_api/', ToppingAPI.as_view(), name='topping_api'),

    # REST API
    path('pizza_rest_api/', include(router.urls)),
    path('filter_pizza/', PizzaAPIView.as_view(), name="filter_pizza"),
]
