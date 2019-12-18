from django.test import TestCase, Client

from .models import Topping, Order, Dough, Pizza, InstancePizza, Snack
from accounts.models import User


# My tests.

class MyTestClass(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='fred', password='secret', email='a@b.c', phone='7777777', street_adress='Gotem', town_adress='Jmirenka')
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        topping1 = Topping.objects.create(description='mushrooms', price=5)
        Topping.objects.create(description='cheese', price=6)
        Dough.objects.create(description='30sm', price=10)
        Dough.objects.create(description='24sm', price=9)
        Pizza.objects.create(name='Mushroom', dough_id=1, topping=topping1, price=20)
        Pizza.objects.create(name='Cheese', dough_id=2, topping_id=2, price=25)
        Snack.objects.create(description='crisps', price=3)
        Snack.objects.create(description='Crackers', price=2)
        InstancePizza.objects.create(pizza_template_id=1, count=2, name='Mushroom', price=20)
        InstancePizza.objects.create(pizza_template_id=2, count=4, name='Cheese', price=25)
        Order.objects.create(user_id=1, price=333)

# test create model
    def test_created_topping(self):
        topping = Topping.objects.get(id=1)
        self.assertEqual(topping.description, 'mushrooms')

    def test_create_dough(self):
        dough = Dough.objects.get(id=1)
        self.assertEqual(dough.description, '30sm')

    def test_create_pizza(self):
        pizza = Pizza.objects.get(id=1)
        self.assertEqual(pizza.name, 'Mushroom')

    def test_create_snack(self):
        snack = Snack.objects.get(id=1)
        self.assertEqual(snack.description, 'crisps')

    def test_create_order(self):
        order = Order.objects.get(id=1)
        self.assertEqual(order.price, 333)

# test page
    def test_topping_page(self):
        response = self.client.get('/sorter/')
        self.assertContains(response, 'mushrooms')

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to pizza 'У Ашота'!")

# test url
    def test_change_price_toppings(self):
        response = self.client.get('/update/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Введите ценовую поправку :")
        response = self.client.post('/update/', {'price_change': 5})
        self.assertEqual(response.status_code, 302)
        topping = Topping.objects.get(id=1)
        self.assertEqual(topping.price, 10)
        self.assertNotEqual(topping.price, 5)

    def test_change_dough(self):
        response = self.client.get('/dough/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "цена")
        response = self.client.post('/dough/1/edit', {'description': '16sm', 'price': 12})
        self.assertEqual(response.status_code, 302)
        dough = Dough.objects.get(id=1)
        self.assertEqual(dough.price, 12)

    def test_change_topping(self):
        response = self.client.get('/toppings/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "цена")
        response = self.client.post('/toppings/1/edit', {'description': 'MUSHROOMS', 'price': 10})
        self.assertEqual(response.status_code, 302)
        topping = Topping.objects.get(id=1)
        self.assertEqual(topping.price, 10.0)

    def test_change_snack(self):
        response = self.client.get('/snacks/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "цена")
        response = self.client.post('/snacks/1/edit', {'description': 'CRISPS', 'price': 10})
        self.assertEqual(response.status_code, 302)
        snack = Snack.objects.get(id=1)
        self.assertEqual(snack.price, 10.0)

    def test_change_instance_pizza(self):
        response = self.client.get('/insttance_pizza/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "число пиц")
        response = self.client.post('/insttance_pizza/1/edit', {'count': 5})
        self.assertEqual(response.status_code, 302)
        instance_pizza = InstancePizza.objects.get(id=1)
        self.assertEqual(instance_pizza.count, 5)

    def test_loggin(self):
        self.client.login(username=self.user.email, password='secret')
        response = self.client.post('/accounts/login/', {'email': self.user.email, 'password': 'secret'})
        self.assertEqual(response.status_code, 200)

    def test_create_basket(self):
        self.client.login(username=self.user.email, password='secret')
        response = self.client.get('/add_pizza/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ваша корзина")
        response = self.client.post('/add_pizza/', {'pizza_id': 1, 'count': 6})
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(id=1)
        self.assertEqual(order.price, 120)

    def test_chancge_order(self):
        self.client.login(username=self.user.email, password='secret')
        response = self.client.get('/orders/1/edit')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Форма изменения заказа")
        response = self.client.post('/orders/1/edit', {'pizzas': 2})
        order = Order.objects.get(id=1)
        self.assertEqual(order.price, 100)

    def test_delete_instance_pizza(self):
        response = self.client.get('/delete_insttance_pizza/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure you want to delete")

    def test_sorter_toppings(self):
        response = self.client.get('/sorter/?ordering=price')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1 -- mushrooms -- 5.00")
        self.assertEqual(response.status_code, 200)

    def test_list_doughs(self):
        response = self.client.get('/dough/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1 -- 30sm -- 10.00")
        self.assertEqual(response.status_code, 200)

    def test_list_snacks(self):
        response = self.client.get('/snacks/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1 -- crisps -- 3.00")
        self.assertEqual(response.status_code, 200)

    def test_basket(self):
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Список заказов")
        self.assertEqual(response.status_code, 200)

    def test_add_dough(self):
        response = self.client.get('/create_dough/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "описание коржа")
        response = self.client.post('/create_dough/', {'description': '30sm thin', 'price': 15})
        self.assertEqual(response.status_code, 302)
        dough = Dough.objects.get(id=3)
        self.assertEqual(dough.price, 15)

    def test_add_shack(self):
        response = self.client.get('/create_snacks/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "описание закуски")
        response = self.client.post('/create_snacks/', {'description': 'beer', 'price': 5})
        self.assertEqual(response.status_code, 302)
        snack = Snack.objects.get(id=3)
        self.assertEqual(snack.price, 5)

    def test_add_topping(self):
        response = self.client.get('/create_topping/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "описание топинга")
        response = self.client.post('/create_topping/', {'description': 'chicken', 'price': 4})
        self.assertEqual(response.status_code, 302)
        topping = Topping.objects.get(id=3)
        self.assertEqual(topping.price, 4)

# test shipping

    def test_set_shipping(self):
        self.client.login(username=self.user.email, password='secret')
        response = self.client.get('/set_shipping/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Информация о Вашем заказе')
        response = self.client.post('/set_shipping/', {
            'first_name': 'Chilapuk',
            'last_name': 'Batmanovich',
            'email': 'example@example.ru',
            'phone': '6666666',
            'street_adress': 'Garlem',
            'town_adress': 'Babruisk'
        })
        self.assertEqual(response.status_code, 302)
        curent_user = User.objects.get(id=1)
        self.assertEqual(curent_user.phone, '6666666')
