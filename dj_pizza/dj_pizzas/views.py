from django.http import HttpResponse
from django.views.generic.edit import UpdateView, FormView
from django.views.generic import ListView, TemplateView, CreateView
from dj_pizzas.models import *
from dj_pizzas.forms import *
from django.template import Context, Template

sort_order = 'id'


class Home(TemplateView):
	template_name = 'index.html'


class CreateOrder(FormView):
	model = Order
	template_name = 'create_object.html'
	form_class = CreateOrderForm
	success_url = '/'

	def get_context_data(self, **kwargs):
		context = {'object_name': 'заказа'}
		return super().get_context_data(**context)

	def form_valid(self, form):
		Order.add_pizza(pizza_id, self.request.user)
		pizza_id = form.cleaned_data.get('pizza_id')
		pizza = Pizza.objects.get(id=pizza_id)
		pizza_instance = PizzaInstance.make_pizza(pizza)
		order.pizzas.add(pizza_instance)


class ListOrders(ListView):
	model = Order
	template_name = 'list_objects.html'

	def get_queryset(self):
		order = Order.objects.all()
		return order

	def get_context_data(self, **kwargs):
		context = {'object_name1': 'заказов', 'object_name2': 'заказа'}
		return super().get_context_data(**context)


class UpdateOrder(UpdateView):
	model = Order
	form_class = EditOrderForm
	template_name = 'update.html'
	success_url = '/'


class CreateDough(CreateView):
	model = Dough
	form_class = CreateDoughForm
	template_name = 'create_object.html'
	success_url = '/'

	def get_context_data(self, **kwargs):
		context = {'object_name': 'коржа'}
		return super().get_context_data(**context)


class ListDough(ListView):
	model = Dough
	template_name = 'list_objects.html'

	def get_queryset(self):
		order = Dough.objects.all()
		return order

	def get_context_data(self, **kwargs):
		context = {'object_name1': 'коржей', 'object_name2': 'коржа'}
		return super().get_context_data(**context)


class UpdateDough(UpdateView):
	model = Dough
	form_class = EditDoughForm
	template_name = 'update.html'
	success_url = '/'


class CreateSnacks(CreateView):
	model = Snacks
	form_class = CreateSnacksForm
	template_name = 'create_object.html'
	success_url = '/'

	def get_context_data(self, **kwargs):
		context = {'object_name': 'закусок'}
		return super().get_context_data(**context)


class ListSnacks(ListView):
	model = Snacks
	template_name = 'list_objects.html'

	def get_queryset(self):
		order = Snacks.objects.all()
		return order

	def get_context_data(self, **kwargs):
		context = {'object_name1': 'закусок', 'object_name2': 'закуски'}
		return super().get_context_data(**context)


class UpdateSnack(UpdateView):
	model = Snacks
	form_class = EditSnackForm
	template_name = 'update.html'
	success_url = '/'


class CreateTopping(CreateView):
	model = Topping
	form_class = CreateToppingForm
	template_name = 'create_object.html'
	success_url = '/'

	def get_context_data(self, **kwargs):
		context = {'object_name': 'топпинга'}
		return super().get_context_data(**context)


class ListToppings(ListView):
	model = Topping
	template_name = 'list_objects.html'

	def get_context_data(self, **kwargs):
		context = {'object_name1': 'топпингов', 'object_name2': 'топпинга'}
		return super().get_context_data(**context)

	def get_queryset(self):
		global sort_order
		order = Topping.objects.all().order_by(sort_order)
		return order


class UpdateTopping(UpdateView):
	model = Topping
	form_class = EditToppingForm
	template_name = 'update.html'
	success_url = '/'


class CommonToppingUpdate(FormView):
	model = Topping
	form_class = UpdateObject
	template_name = 'common_update.html'
	success_url = '/toppings/'

	def form_valid(self, form):
		price_change = form.cleaned_data.get('price_change')
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


#class CreatePizza(ListView):
#	model = Pizza
#	template_name = 'pizza_constructor.html'
#
#	def get_context_data(self, **kwargs):
#		context = super(CreatePizza, self).get_context_data(**kwargs)
#		context['']
#		return context
