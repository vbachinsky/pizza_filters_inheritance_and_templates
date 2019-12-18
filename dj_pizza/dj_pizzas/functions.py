from dj_pizzas.forms import *
from django.views.generic.edit import UpdateView


class BaseUpdate(UpdateView):
    def form_valid(self, form):
        instance = super().form_valid(form)
        order = Order.objects.get(user=self.request.user)
        order.update_price()
        return instance
