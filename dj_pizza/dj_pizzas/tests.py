from django.test import TestCase

from .models import Topping, Order


# Create your tests here.

class MyTestClass(TestCase):
    def setUp(self):
        pass
    @classmethod
    def setUpTestData(cls):
        Topping.objects.create(description='salamy', price=5)
        Topping.objects.create(description='cheese', price=6)
#        Order.objects.create()

    def test_created_model(self):
        topping = Topping.objects.get(id=1)
        self.assertEqual(topping.description, 'salamy')

    def test_topping_page(self):
        response = self.client.get('/sorter/')
        self.assertContains(response, 'salamy')

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to pizza 'У Ашота'!")

    def test_change_price_method(self):
        response = self.client.get('/update/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Введите ценовую поправку :")

        response = self.client.post('/update/', {'price_change': 5})
        self.assertEqual(response.status_code, 302)
        topping = Topping.objects.get(id=1)
        self.assertEqual(topping.price, 10)
        self.assertNotEqual(topping.price, 5)

