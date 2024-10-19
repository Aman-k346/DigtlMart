from django.contrib import admin
from .models import Payment

# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'amount', 'status', 'created_at')
    search_fields = ('transaction_id', 'user__username', 'status')
    list_filter = ('status',)

admin.site.register(Payment, PaymentAdmin)
