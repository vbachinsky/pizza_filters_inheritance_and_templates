# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.db import models


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name_of_your_order = models.CharField(null = False, max_length=200)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    order = models.ManyToManyField('InstancePizza')

    def __str__(self):
        return self.name_of_your_order

#    @staticmethod
#    def add_pizza(pizza_id):
#        pizza_id = form.cleaned_data.get('pizza_id')
#        pizza = Pizza.objects.get(id=pizza_id)
#        pizza_instance = InstancePizza.make_pizza(pizza)
#        order = Order.objects.get(user=request.user)
#        order.pizzas.add(pizza_instance)



class Topping(models.Model):
    description = models.CharField(null = False, max_length = 50)
    price = models.DecimalField(default=0, max_digits = 5, decimal_places = 2)

    def __str__(self):
        return self.topping_description

class Dough(models.Model):
    description = models.CharField(null = False, max_length = 50)
    price = models.DecimalField(default=0, max_digits = 5, decimal_places = 2)

    def __str__(self):
        return self.description


class OrderedToppings(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, default=0)
    topping = models.ForeignKey(Topping, on_delete = models.CASCADE, default=0)

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = "Ordered toppings"
        verbose_name_plural = "Ordered toppings"


class Pizza(models.Model):
    dough = models.ForeignKey(Dough, on_delete=models.CASCADE, default=0)
    ordered_toppings = models.ForeignKey(OrderedToppings, on_delete = models.CASCADE, default=0)
    description = models.CharField(null = False, max_length = 200)

    def __str__(self):
        return self.id


class InstancePizza(Pizza):         #new
    pizza = models.ForeignKey(Pizza, related_name='pizza_template', on_delete=models.SET_NULL, null=True, blank=True)
#    count = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=3, decimal_places=2)

    def make_piza(self):
        pass

    def full_price(self):
        return self.price * self.count


class Snacks(models.Model):
    description = models.CharField(null = False, max_length = 50)
    price = models.DecimalField(default=0, max_digits = 5, decimal_places = 2)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Snacks"


class OrderedSnacks(models.Model):
    snack = models.ForeignKey(Snacks, on_delete = models.CASCADE, default=0)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, default=0)

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = "Ordered snacks"
        verbose_name_plural = "Ordered snacks"


class OrderPayment(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, default=0)
    transaction = models.IntegerField()

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "Ordered payment"
        verbose_name_plural = "Ordered payments"


class Person(models.Model):
    first_name = models.CharField(null = False, max_length = 20)
    last_name = models.CharField(max_length = 20)
    adress = models.CharField(max_length = 20)
    phone = models.CharField(max_length = 20)

    def __str__(self):
        return self.first_name


class ClientAccount(models.Model):
    credit_card_indicator = models.BooleanField(default = False)
    client_deposit = models.BooleanField(default = False)
    date_enroller = models.DateField(auto_now_add = True)
    date_terminate = models.DateField()

    class Meta:
        verbose_name = "Client account"
        verbose_name_plural = "Client accounts"


class ClientAccountPerson(models.Model):
    client_account = models.ForeignKey(ClientAccount, on_delete = models.CASCADE, default=0)
    person = models.ForeignKey(Person, on_delete = models.CASCADE, default=0)

    class Meta:
        verbose_name = "Client account person"
        verbose_name_plural = "Client accounts persons"


class Employee(models.Model):
    person = models.ForeignKey(Person, on_delete = models.CASCADE, default=0)
    employee_tax = models.DecimalField(default=0, max_digits = 5, decimal_places = 2)
    employee_job_category = models.CharField(max_length = 100)


class ClientTransaction(models.Model):
    client_account = models.ForeignKey(ClientAccount, on_delete = models.CASCADE, default=0)
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE, default=0)
    transaction_date = models.DateTimeField(auto_now_add = True)
    sales_tax = models.FloatField(default = 0.05)

    class Meta:
        verbose_name = "Client transaction"
        verbose_name_plural = "Client transactions"
