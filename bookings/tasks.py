from celery import shared_task
from django.utils import timezone
from django.apps import apps
from .models import Booking


@shared_task
def expire_bookings():
    expired_bookings = Booking.objects.filter(
        status='pending',
        expires_at__lte=timezone.now()
    )

    expired_bookings.update(status='expired')
    return f"Истекло {expired_bookings.count()} броней"


@shared_task
def confirm_booking(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, status='pending')
        product = booking.product

        if product.quantity >= booking.quantity:
            product.quantity -= booking.quantity
            product.save()

            booking.status = 'confirmed'
            booking.confirmed_at = timezone.now()
            booking.save()

            return f"Бронь {booking_id} успешно подтверждена"
        else:
            booking.status = 'cancelled'
            booking.cancelled_at = timezone.now()
            booking.save()

            return f"Недостаточно товара для брони {booking_id}"
    except Booking.DoesNotExist:
        return f"Бронь {booking_id} не найдена"


@shared_task
def sync_to_replica():
    for model in apps.get_models():
        model.objects.using('replica').all().delete()
        for obj in model.objects.using('default').all():
            obj.save(using='replica')
