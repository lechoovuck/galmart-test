from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'status', 'created_at', 'expires_at')
    list_filter = ('status', 'created_at', 'expires_at')
    search_fields = ('product__name',)
    readonly_fields = ('created_at', 'expires_at', 'confirmed_at', 'cancelled_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('product', 'quantity', 'status')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'expires_at', 'confirmed_at', 'cancelled_at'),
            'classes': ('collapse',)
        }),
    )
