from django.test import TransactionTestCase
from rest_framework.test import APIClient
from products.models import Product
from bookings.models import Booking


class BookingTestCase(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(
            name="Test Product",
            price=100,
            quantity=10
        )

    def test_create_booking_success(self):
        url = '/api/bookings/'
        data = {'product': self.product.id, 'quantity': 2}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data['quantity'], 2)
        self.assertEqual(response_data['status'], 'pending')

    def test_create_booking_insufficient_quantity(self):
        url = '/api/bookings/'
        data = {'product': self.product.id, 'quantity': 1000}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn('Недостаточно товара', str(response_data))


class BookingActionTestCase(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(
            name="Test Product",
            price=100,
            quantity=10
        )
        self.booking = Booking.objects.create(
            product=self.product,
            quantity=2
        )

    def test_confirm_booking(self):
        url = f'/api/bookings/{self.booking.id}/confirm/'

        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'confirmed')

    def test_cancel_booking(self):
        url = f'/api/bookings/{self.booking.id}/cancel/'

        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, 'cancelled')
