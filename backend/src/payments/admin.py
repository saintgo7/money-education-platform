from django.contrib import admin
from .models import Payment, Subscription


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'tier', 'status', 'started_at', 'expires_at']
    list_filter = ['tier', 'status']
