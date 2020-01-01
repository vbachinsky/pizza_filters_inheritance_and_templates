from .serializers import *
from .models import *
from rest_framework import viewsets, generics, views
from rest_framework.response import Response
import django_filters.rest_framework


class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer


class PizzaAPIView(generics.ListAPIView):
    serializer_class = PizzaSerializer

    def get_queryset(self):
        queryset = Pizza.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__lt=name)
            return queryset


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'
