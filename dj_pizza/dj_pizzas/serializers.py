from django.conf.urls import url, include
from django.contrib.auth.models import User
from .models import *
from accounts.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class DoughSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dough
        fields = ['description', 'price']


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ['description', 'price']


class PizzaSerializer(serializers.ModelSerializer):
    dough = DoughSerializer()
    topping = ToppingSerializer()

    class Meta:
        model = Pizza
        fields = ['id', 'name', 'price', 'dough', 'topping']


class InstancePizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstancePizza
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    pizzas = InstancePizzaSerializer(many=True, required=False)
    user = UserSerializer(required=False)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        basket_id = instance.id
        pizza_id = self.initial_data['pizza_id']
        count = self.initial_data['count']
        if pizza_id.isdigit() and count.isdigit():
            pizza = Pizza.objects.get(id=pizza_id)
            instance_pizza = pizza.make_order(count)
            order = Order.objects.get(id=basket_id)
            order.pizzas.add(instance_pizza)
            order.update_price()
            return instance
        else:
            return instance
