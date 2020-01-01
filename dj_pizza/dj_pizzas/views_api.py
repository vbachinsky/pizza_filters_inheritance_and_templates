from django.http import JsonResponse
from dj_pizzas.models import *
from dj_pizzas.forms import *
from accounts.models import User
from django.template import Context, Template
from django.views.generic.base import View


class PizzaAPI(View):
    def get(self, request, *args, **kwargs):
        pizzas = Pizza.objects.all()
        pizzas_list = []
        for pizza in pizzas:
            pizzas_list.append({'name': pizza.name, 'price': pizza.price})
        return JsonResponse({'message': 'Full list pizzas', "pizza list": pizzas_list})

    def post(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Список пицц', })


class ToppingAPI(View):
    def get(self, request, *args, **kwargs):
        toppings = Topping.objects.all()
        toppings_list = []
        for topping in toppings:
            toppings_list.append({'name': topping.description, 'price': topping.price})
        return JsonResponse({'message': 'Full list toppings', "toppings list": toppings_list})

    def post(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Список топпингов', })


class FilterPizzaAPI(View):
    def get(self, request, *args, **kwargs):
        filtering = request.GET.get('filter')
        limit = request.GET.get('limit')
        pizzas_list = []
        if filtering in ('price', 'name', 'id') and limit==None:
            for pizza in Pizza.objects.all().order_by(filtering):
                pizzas_list.append(pizza.get_serializer_pizza())
            return JsonResponse({'Filtered list pizzas': pizzas_list})
        if filtering =='price' and limit.isdigit():
            for pizza in Pizza.objects.all().order_by(filtering).filter(price__lt=limit):
                pizzas_list.append(pizza.get_serializer_pizza())
            return JsonResponse({'Filtered list pizzas': pizzas_list})
        if filtering == 'name' and limit.isalpha():
            for pizza in Pizza.objects.all().order_by(filtering).filter(name__icontains=limit):
                pizzas_list.append(pizza.get_serializer_pizza())
            return JsonResponse({'Filtered list pizzas': pizzas_list})
        if filtering == 'id' and limit.isdigit():
            for pizza in Pizza.objects.all().order_by(filtering).filter(id__lt=limit):
                pizzas_list.append(pizza.get_serializer_pizza())
            return JsonResponse({'Filtered list pizzas': pizzas_list})
        else:
            pizzas_list = {'message': 'Неверный запрос. Допустимые параметры фильтрации: price, name, id'}
            return JsonResponse({'Filtered list pizzas': pizzas_list})

    def post(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Фильтрация пицц по названию, id или цене', })


class BasketAPI(View):
    def get(self, request, *args, **kwargs):
        basket_id = request.GET.get('basket_id')
        if basket_id.isdigit():
            basket = Order.objects.get(id=basket_id)
            return JsonResponse({'Basket': basket.get_serializer_basket()})
        else:
            return JsonResponse({'message': 'Неверный запрос. Укажите id корзины'})

    def post(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Получение корзины', })


class UpdateBasketAPI(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Добавление пицц в корзину', })

    def post(self, request, *args, **kwargs):
        basket_id = self.request.POST['basket_id']
        pizza_id = self.request.POST['pizza_id']
        count = self.request.POST['count']
        if basket_id.isdigit() and pizza_id.isdigit() and count.isdigit():
            pizza = Pizza.objects.get(id=pizza_id)
            instance_pizza = pizza.make_order(count)
            order = Order.objects.get(id=basket_id)
            order.pizzas.add(instance_pizza)
            order.update_price()
            answer = 'В заказ №' + str(basket_id) + ' добовленно ' + str(count) + ' пицц ' + pizza.name
            return JsonResponse({'message': answer})
        else:
            return JsonResponse({'message': 'Неверный запрос. Укажите id корзины, id заказанных пицц и их число'})
