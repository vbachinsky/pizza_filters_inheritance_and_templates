from django import forms
from .models import Topping


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