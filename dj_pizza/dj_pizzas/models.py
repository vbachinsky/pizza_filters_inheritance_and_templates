# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.db import models


class Order(models.Model):
	date_order = models.DateTimeField(auto_now_add=True)
	name_of_your_order = models.CharField(null = False, max_length = 200)
	price_order = models.DecimalField(default=0, max_digits = 5, decimal_places = 2)

	def __str__(self):
		return self.name_of_your_order


class Topping(models.Model):
	topping_description = models.CharField(null = False, max_length = 50)
	topping_price = models.DecimalField(default=0, max_digits = 5, decimal_places = 2)

	def __str__(self):
		return self.topping_description

class Dough(models.Model):
	dough_description = models.CharField(null = False, max_length = 50)
	dough_price = models.DecimalField(default=0, max_digits = 5, decimal_places = 2)

	def __str__(self):
		return self.dough_description


class OrderedToppings(models.Model):
	order_id = models.ForeignKey(Order, on_delete = models.CASCADE, default=0)
	topping_id = models.ForeignKey(Topping, on_delete = models.CASCADE, default=0)

	def __str__(self):
		return str(self.order_id)

	class Meta:
		verbose_name = "Ordered toppings"
		verbose_name_plural = "Ordered toppings"


class Pizza(models.Model):
	order_id = models.ForeignKey(Order, on_delete = models.CASCADE, default=0)
	dough_id = models.ForeignKey(Dough, on_delete = models.CASCADE, default=0)
	ordered_toppings_id = models.ForeignKey(OrderedToppings, on_delete = models.CASCADE, default=0)
	pizza_description = models.CharField(null = False, max_length = 200)

	def __str__(self):
		return self.pizza_description


class Snacks(models.Model):
	snack_description = models.CharField(null = False, max_length = 50)
	snack_price = models.DecimalField(default=0, max_digits = 5, decimal_places = 2)

	def __str__(self):
		return self.snack_description

	class Meta:
		verbose_name_plural = "Snacks"


class OrderedSnacks(models.Model):
	snack_id = models.ForeignKey(Snacks, on_delete = models.CASCADE, default=0)
	order_id = models.ForeignKey(Order, on_delete = models.CASCADE, default=0)

	def __str__(self):
		return str(self.order_id)

	class Meta:
		verbose_name = "Ordered snacks"
		verbose_name_plural = "Ordered snacks"


class OrderPayment(models.Model):
	order_id = models.ForeignKey(Order, on_delete = models.CASCADE, default=0)
	transaction_id = models.IntegerField()

	def __str__(self):
		return self.transaction_id

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
	client_account_id = models.ForeignKey(ClientAccount, on_delete = models.CASCADE, default=0)
	person_id = models.ForeignKey(Person, on_delete = models.CASCADE, default=0)

	class Meta:
		verbose_name = "Client account person"
		verbose_name_plural = "Client accounts persons"


class Employee(models.Model):
	person_id = models.ForeignKey(Person, on_delete = models.CASCADE, default=0)
	employee_tax_id = models.DecimalField(default=0, max_digits = 5, decimal_places = 2)
	employee_job_category = models.CharField(max_length = 100)


class ClientTransaction(models.Model):
	client_account_id = models.ForeignKey(ClientAccount, on_delete = models.CASCADE, default=0)
	employee_id = models.ForeignKey(Employee, on_delete = models.CASCADE, default=0)
	transaction_date = models.DateTimeField(auto_now_add = True)
	sales_tax = models.FloatField(default = 0.05)

	class Meta:
		verbose_name = "Client transaction"
		verbose_name_plural = "Client transactions"