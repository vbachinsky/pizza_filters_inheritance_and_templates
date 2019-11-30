from django import forms
from .models import Topping
from django import forms


ORDER = (('id', 'id'), ('topping_price', 'цена'), ('topping_description', 'по имени'))


class CreateObject(forms.ModelForm):
	class Meta:
		model = Topping
		fields = ['id', 'topping_description', 'topping_price']
		labels = {'id': 'номер топпинга','topping_description': 'описание топинга', 'topping_price': 'цена'}


class EditObject(forms.ModelForm):
	class Meta:
		model = Topping
		fields = ['topping_description', 'topping_price']
		labels = {'topping_description': 'описание топинга', 'topping_price': 'цена'}


class UpdateObject(forms.Form):
	price_change = forms.DecimalField(label='Введите ценовую поправку ', max_digits=5, decimal_places=2)


class SorterObject(forms.Form):
	order = forms.ChoiceField(label='Порядок сортировки: ', choices=ORDER)