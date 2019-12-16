# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from accounts.models import User


class Topping(models.Model):
    description = models.CharField(null=False, max_length=50)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.description


class Dough(models.Model):
    description = models.CharField(null=False, max_length=50)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.description


class Pizza(models.Model):
    name = models.CharField(null=False, max_length=200)
    dough = models.ForeignKey(Dough, on_delete=models.CASCADE, default=0)
    topping = models.ForeignKey(Topping, on_delete=models.CASCADE, default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def make_order(self, count):
        return InstancePizza.objects.create(name=self.name, price=self.price, pizza_template=self, count=count)


class InstancePizza(models.Model):
    pizza_template = models.ForeignKey(Pizza, related_name='pizza_template', on_delete=models.SET_NULL, null=True, blank=True)
    count = models.PositiveIntegerField(default=1)
    name = models.CharField(null=True, blank=True, max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    
    def __str__(self):
        return 'name: {}, price: {}, full price: {}'.format(self.name, str(self.price), str(self.price * self.count))

    @property
    def full_price(self):
        return self.price * self.count


class Order(models.Model):
    pizzas = models.ManyToManyField(InstancePizza, related_name='order_template')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    price = models.DecimalField(default=0, max_digits=7, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return 'OrderID: {}, price: {}'.format(str(self.id), str(self.price))

    def update_price(self):
        self.price = sum([pizza.full_price for pizza in self.pizzas.all()])
        self.save()


class Snacks(models.Model):
    description = models.CharField(null=False, max_length=50)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Snacks"


class OrderedSnacks(models.Model):
    snack = models.ForeignKey(Snacks, on_delete=models.CASCADE, default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = "Ordered snacks"
        verbose_name_plural = "Ordered snacks"


class OrderPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=0)
    transaction = models.IntegerField()

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "Ordered payment"
        verbose_name_plural = "Ordered payments"


class ClientAccount(models.Model):
    credit_card_indicator = models.BooleanField(default=False)
    client_deposit = models.BooleanField(default=False)
    date_enroller = models.DateField(auto_now_add=True)
    date_terminate = models.DateField()

    class Meta:
        verbose_name = "Client account"
        verbose_name_plural = "Client accounts"


class ClientAccountPerson(models.Model):
    client_account = models.ForeignKey(ClientAccount, on_delete=models.CASCADE, default=0)
    person = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    class Meta:
        verbose_name = "Client account person"
        verbose_name_plural = "Client accounts persons"


class Employee(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    employee_tax = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    employee_job_category = models.CharField(max_length=100)


class ClientTransaction(models.Model):
    client_account = models.ForeignKey(ClientAccount, on_delete=models.CASCADE, default=0)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, default=0)
    transaction_date = models.DateTimeField(auto_now_add=True)
    sales_tax = models.FloatField(default=0.05)

    class Meta:
        verbose_name = "Client transaction"
        verbose_name_plural = "Client transactions"
