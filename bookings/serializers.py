from rest_framework import serializers
from .models import Booking
from products.models import Product

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['product', 'quantity']

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if product.quantity < quantity:
            raise serializers.ValidationError(
                f"Недостаточно товара на складе. Доступно: {product.quantity}"
            )

        return data

class BookingSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['status', 'created_at', 'expires_at', 'confirmed_at', 'cancelled_at']
