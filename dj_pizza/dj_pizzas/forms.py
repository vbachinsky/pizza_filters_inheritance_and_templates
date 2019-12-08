from django import forms
from .models import *
from accounts.models import User

class ShippingForm(forms.Form):
    email = forms.EmailField(max_length=20)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    street_adress = forms.CharField(max_length=20)
    town_adress = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)


class BasketForm(forms.Form):
    pizza_id = forms.IntegerField(min_value=0)
    count = forms.IntegerField(min_value=0)


class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['id', 'price', 'pizzas']
        labels = {'id': 'номер заказа' , 'price': 'цена', 'pizzas': 'пиццы'}


class EditInstancePizzaForm(forms.ModelForm):
    class Meta:
        model = InstancePizza
        fields = ['name', 'count']
        labels = {'name': 'наименование пиц', 'count':'число пицц'}


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