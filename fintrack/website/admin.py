from django.contrib import admin
from website.models import Payment

# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_date', 'category', 'description', 'amount', 'user']
    list_filter = ['user', 'payment_date', 'category']
    ordering = ['user', '-payment_date']
    search_fields = ['payment_date', 'category', 'description', 'amount']