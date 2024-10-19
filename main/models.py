from django.db import models
from django.conf import settings
# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    transaction_id = models.CharField(max_length=100, unique=True)  # Unique transaction ID from payment gateway
    merchant_transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ProductName = models.CharField(max_length=250, default="Video Editing Bundle")

    def __str__(self):
        return f"Payment {self.transaction_id} - User {self.user.username if self.user else 'Unknown'} - Status: {self.status}"
