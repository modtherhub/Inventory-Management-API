from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# types of inventory changes
CHANGE_TYPES = [
    ("restock", "Restock"),
    ("sale", "Sale"),
    ("adjustment", "Adjustment"),
]

User = settings.AUTH_USER_MODEL

# Inventory item model
# Represents an item in the inventory
# Tracks owner, quantity, price, category, & timestamps
class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=120, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory_items')

    class Meta:
        ordering = ['-last_updated']

    def __str__(self):
        return f"{self.name} (qty={self.quantity})"


# Inventory change log model
# Logs all changes to inventory items for auditing purposes
# Stores who made the change, type of change, and old/new quantities
class InventoryChangeLog(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='changes')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    old_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPES)
    change_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-change_date']


    def __str__(self):
        return f"{self.item.name}: {self.change_type} {self.old_quantity}->{self.new_quantity}"
    
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_items")  # ✅ صاحب العنصر

    def __str__(self):
        return self.name
