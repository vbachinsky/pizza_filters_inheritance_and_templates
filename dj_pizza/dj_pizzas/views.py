from django.http import HttpResponse
from django.views.generic.edit import UpdateView
from django.views.generic import View, ListView, TemplateView, CreateView
from dj_pizzas.models import *
from dj_pizzas.forms import CreateObject, EditObject


class ListToppings(ListView):
	model = Topping
	template_name = 'list_toppings.html'

	def get_queryset(self):
		return Topping.objects.all()


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