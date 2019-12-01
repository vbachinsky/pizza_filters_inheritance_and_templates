from django.http import HttpResponse
from django.views.generic.edit import UpdateView, FormView
from django.views.generic import View, ListView, TemplateView, CreateView
from dj_pizzas.models import *
from dj_pizzas.forms import CreateObject, EditObject, UpdateObject, SorterObject

sort_order = 'id'


class ListToppings(ListView):
	model = Topping
	template_name = 'list_toppings.html'

	def get_queryset(self):
		global sort_order
		order = Topping.objects.all().order_by(sort_order)
		return order


class CreateTopping(CreateView):
	model = Topping
	form_class = CreateObject
	template_name = 'create_topping.html'
	success_url = '/'


class Home(TemplateView):
	template_name = 'index.html'


class UpdateTopping(UpdateView):
	model = Topping
	form_class = EditObject
	template_name = 'update_topping.html'
	success_url = '/'


class CommonToppingUpdate(FormView):
	model = Topping
	form_class = UpdateObject
	template_name = 'common_update.html'
	success_url = '/toppings/'

	def form_valid(self, form):
		price_change = form.cleaned_data.get('price_change')
		print(price_change)
		all_toppings = Topping.objects.all()
		for topping in all_toppings:
			topping.topping_price = topping.topping_price + price_change
			topping.save()
		return super().form_valid(form)


class ToppingSorter(FormView):
	model = Topping
	form_class = SorterObject
	template_name = 'common_update.html'
	success_url = '/toppings/'

	def form_valid(self, form):
		global sort_order
		order = form.cleaned_data.get('order')
		sort_order = order
		return super().form_valid(form)