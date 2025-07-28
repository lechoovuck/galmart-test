from django.test import TransactionTestCase
from rest_framework.test import APIClient
from decimal import Decimal
from .models import Product


class ProductModelTestCase(TransactionTestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="testname",
            description="testdesc",
            price=Decimal('99.99'),
            quantity=5
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "testname")
        self.assertEqual(self.product.description, "testdesc")
        self.assertEqual(self.product.price, Decimal('99.99'))
        self.assertEqual(self.product.quantity, 5)
        self.assertIsNotNone(self.product.created_at)
        self.assertIsNotNone(self.product.updated_at)

    def test_product_string_representation(self):
        self.assertEqual(str(self.product), "testname")

    def test_product_default_quantity(self):
        product = Product.objects.create(
            name="Test",
            price=Decimal('50.00')
        )
        self.assertEqual(product.quantity, 0)


class ProductAPITestCase(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(
            name="testname",
            description="testdesc",
            price=Decimal('0.01'),
            quantity=10
        )

    def test_list_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "testname")
        self.assertEqual(Decimal(str(data[0]['price'])), Decimal('0.01'))

    def test_retrieve_product(self):
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], "testname")
        self.assertEqual(data['description'], "testdesc")
        self.assertEqual(Decimal(str(data['price'])), Decimal('0.01'))
        self.assertEqual(data['quantity'], 10)

    def test_create_product(self):
        data = {
            'name': 'testname',
            'description': 'testdesc',
            'price': '0.01',
            'quantity': 1
        }
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, 201)
        created_data = response.json()
        self.assertEqual(created_data['name'], 'testname')
        self.assertEqual(created_data['description'], 'testdesc')
        self.assertEqual(Decimal(str(created_data['price'])), Decimal('0.01'))
        self.assertEqual(created_data['quantity'], 1)

    def test_update_product(self):
        data = {
            'name': 'testname',
            'description': 'testdesc',
            'price': '99.99',
            'quantity': 20
        }
        response = self.client.put(f'/api/products/{self.product.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        updated_data = response.json()
        self.assertEqual(updated_data['name'], 'testname')
        self.assertEqual(updated_data['description'], 'testdesc')
        self.assertEqual(Decimal(str(updated_data['price'])), Decimal('99.99'))
        self.assertEqual(updated_data['quantity'], 20)

    def test_partial_update_product(self):
        data = {
            'price': '89.99'
        }
        response = self.client.patch(f'/api/products/{self.product.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        updated_data = response.json()
        self.assertEqual(Decimal(str(updated_data['price'])), Decimal('89.99'))
        self.assertEqual(updated_data['name'], 'testname')

    def test_delete_product(self):
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)

        get_response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(get_response.status_code, 404)
