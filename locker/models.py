from django.db import models
from django.utils import timezone

class LockCommand(models.Model):
    device_id = models.CharField(max_length=255, unique=True)
    should_lock = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_checked = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Device: {self.device_id} - Lock: {self.should_lock}"
    
    def mark_checked(self):
        self.last_checked = timezone.now()
        self.save()
    
    def update_at_time(self):
        self.update_at = timezone.now()
        self.save()
        
    class Meta:
        app_label = 'locker'

class PurchaseRecord(models.Model):
    device_id = models.CharField(max_length=255, db_index=True)
    product_id = models.CharField(max_length=255, db_index=True)
    receipt_data = models.TextField() # Base64 encoded receipt data
    transaction_id = models.CharField(max_length=255, unique=True) # Apple's transaction ID
    original_transaction_id = models.CharField(max_length=255, null=True, blank=True, db_index=True) # For subscriptions
    purchase_date = models.DateTimeField()
    client_reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase: {self.product_id} by {self.device_id} on {self.purchase_date.strftime('%Y-%m-%d')}"

    class Meta:
        app_label = 'locker'
        ordering = ['-purchase_date']
