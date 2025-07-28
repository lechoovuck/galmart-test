from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer
from .tasks import confirm_booking
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(
        summary="List all bookings",
        description="Retrieve a list of all bookings in the system."
    ),
    retrieve=extend_schema(
        summary="Retrieve a booking",
        description="Get details of a specific booking by its ID."
    ),
    create=extend_schema(
        summary="Create a booking",
        description="Create a new booking for a product."
    ),
    confirm=extend_schema(
        summary="Confirm a booking",
        description="Confirm a pending booking if it hasn't expired."
    ),
    cancel=extend_schema(
        summary="Cancel a booking",
        description="Cancel a pending or confirmed booking and update product quantity if needed."
    ),
)
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        if product.quantity < quantity:
            return Response(
                {'error': f'Недостаточно товара на складе. Доступно: {product.quantity}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking = Booking.objects.create(
            product=product,
            quantity=quantity
        )

        confirm_booking.delay(booking.id)

        response_serializer = BookingSerializer(booking)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        booking = self.get_object()

        if booking.status != 'pending':
            return Response(
                {'error': 'Бронь не может быть подтверждена'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if booking.expires_at < timezone.now():
            booking.status = 'expired'
            booking.save()
            return Response(
                {'error': 'Время брони истекло'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'confirmed'
        booking.confirmed_at = timezone.now()
        booking.save()

        product = booking.product
        product.quantity -= booking.quantity
        product.save()

        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'Бронь не может быть отменена'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = 'cancelled'
        booking.cancelled_at = timezone.now()
        booking.save()

        if booking.status == 'confirmed':
            product = booking.product
            product.quantity += booking.quantity
            product.save()

        serializer = self.get_serializer(booking)
        return Response(serializer.data)
