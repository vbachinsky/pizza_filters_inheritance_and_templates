from django import forms
from .models import *


class CreateToppingForm(forms.ModelForm):
	class Meta:
		model = Topping
		fields = ['id', 'description', 'price']
		labels = {'id': 'номер топпинга','description': 'описание топинга', 'price': 'цена'}


class EditToppingForm(forms.ModelForm):
	class Meta:
		model = Topping
		fields = ['description', 'price']
		labels = {'description': 'описание топинга', 'price': 'цена'}


class CreateOrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['name_of_your_order']
		labels = {'name_of_your_order': 'наименование заказа'}


class EditOrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['id', 'name_of_your_order', 'price']
		labels = {'id': 'номер заказа' , 'name_of_your_order': 'наименование заказа', 'price': 'цена'}


class CreateDoughForm(forms.ModelForm):
	class Meta:
		model = Dough
		fields = ['id' ,'description', 'price']
		labels = {'id': 'ID коржа', 'description': 'описание коржа', 'price': 'цена'}


class EditDoughForm(forms.ModelForm):
	class Meta:
		model = Dough
		fields = ['description', 'price']
		labels = {'description': 'описание коржа', 'price': 'цена'}


class CreateSnacksForm(forms.ModelForm):
	class Meta:
		model = Snacks
		fields = ['id', 'description', 'price']
		labels = {'id': 'ID закуски', 'description': 'описание закуски', 'price': 'цена'}


class EditSnackForm(forms.ModelForm):
	class Meta:
		model = Snacks
		fields = ['description', 'price']
		labels = {'description': 'описание закуски', 'price': 'цена'}


class UpdateObject(forms.Form):
	price_change = forms.DecimalField(label='Введите ценовую поправку ', max_digits=5, decimal_places=2)


class SorterObject(forms.Form):
	ORDER = (('id', 'id'), ('price', 'цена'), ('description', 'по имени'))

	order = forms.ChoiceField(label='Порядок сортировки: ', choices=ORDER)
