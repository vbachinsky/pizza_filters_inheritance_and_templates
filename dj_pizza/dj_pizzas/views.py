from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import UpdateView, FormView, DeleteView, CreateView
from django.views.generic import ListView, TemplateView, CreateView
from dj_pizzas.models import *
from dj_pizzas.forms import *
from accounts.models import User
from django.template import Context, Template
from django.core.cache import cache
from dj_pizzas.functions import *


class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cache.set('cached_client_ip', self.request.META['REMOTE_ADDR'], 60*2)
        curent_client_ip = self.request.META['REMOTE_ADDR']
        if curent_client_ip != cache.get('cached_client_ip'):
            print('IP was changed on ', curent_client_ip)
        return context


class SetShipping(FormView):
    template_name = 'shipping_information.html'
    form_class = ShippingForm
    success_url = '/'

    def form_valid(self, form):
        instance = super().form_valid(form)
        curent_user = User.objects.get(id=self.request.user.id)
        curent_user.first_name = form.cleaned_data.get('first_name')
        curent_user.last_name = form.cleaned_data.get('last_name')
        curent_user.email = form.cleaned_data.get('email')
        curent_user.phone = form.cleaned_data.get('phone')
        curent_user.street_adress = form.cleaned_data.get('street_adress')
        curent_user.town_adress = form.cleaned_data.get('town_adress')
        curent_user.save()
        return instance


class CreateBasket(FormView):
    template_name = 'pizza_constructor.html'
    form_class = BasketForm
    success_url = '/basket/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curent_order, created = Order.objects.get_or_create(user=self.request.user)
        context['instances_pizzas'] = curent_order.pizzas.all()
        return context

    def form_valid(self, form):
        pizza = Pizza.objects.get(id=form.cleaned_data.get('pizza_id'))
        count = form.cleaned_data.get('count')
        instance_pizza = pizza.make_order(count)
        order, created = Order.objects.get_or_create(user=self.request.user)
        order.pizzas.add(instance_pizza)
        order.update_price()
        return super().form_valid(form)


class UpdateOrder(BaseUpdate):
    model = Order
    form_class = UpdateOrderForm
    template_name = 'update_order.html'
    success_url = '/basket/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instances_pizzas'] = InstancePizza.objects.all().filter(order_template__user=self.request.user)
        return context


class ListOrders(ListView):
    model = Order
    template_name = 'list_objects.html'

    def get_queryset(self):
        order = Order.objects.all()
        return order

    def get_context_data(self, **kwargs):
        context = {'object_name1': 'заказов', 'object_name2': 'заказа'}
        return super().get_context_data(**context)


class UpdateInstancePizza(BaseUpdate):
    model = InstancePizza
    form_class = EditInstancePizzaForm
    template_name = 'update.html'
    success_url = '/basket/'


class DeleteInstancePizza(DeleteView):
    model = InstancePizza
    template_name = 'instance_pizza_confirm_delete.html'
    success_url = '/basket/'

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        order = Order.objects.get(user=request.user)
        order.update_price()
        return HttpResponseRedirect(self.success_url)


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
    model = Snack
    form_class = CreateSnacksForm
    template_name = 'create_object.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = {'object_name': 'закусок'}
        return super().get_context_data(**context)


class ListSnacks(ListView):
    model = Snack
    template_name = 'list_objects.html'

    def get_queryset(self):
        order = Snack.objects.all()
        return order

    def get_context_data(self, **kwargs):
        context = {'object_name1': 'закусок', 'object_name2': 'закуски'}
        return super().get_context_data(**context)


class UpdateSnack(UpdateView):
    model = Snack
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


class UpdateTopping(UpdateView):
    model = Topping
    form_class = EditToppingForm
    template_name = 'update.html'
    success_url = '/'


class CommonToppingUpdate(FormView):
    model = Topping
    form_class = UpdateObject
    template_name = 'common_update.html'
    success_url = '/sorter/'

    def form_valid(self, form):
        price_change = form.cleaned_data.get('price_change')
        all_toppings = Topping.objects.all()
        for topping in all_toppings:
            topping.price = topping.price + price_change
            topping.save()
        return super().form_valid(form)


class ToppingSorter(TemplateView):
    template_name = 'list_toppings.html'
    sortering_fields = ['description', 'price', '-price']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordering = self.request.GET.get('ordering')
        if ordering not in self.sortering_fields:
            ordering = 'id'
        context['toppings'] = Topping.objects.all().order_by(ordering)
        return context
