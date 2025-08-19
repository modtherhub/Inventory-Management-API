from django.conf import settings
from django.db import models

CHANGE_TYPES = [
    ("restock", "Restock"),
    ("sale", "Sale"),
    ("adjustment", "Adjustment"),
]

User = settings.AUTH_USER_MODEL


class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=120, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')

    class Meta:
        ordering = ['-last_updated']

    def __str__(self):
        return f"{self.name} (qty={self.quantity})"




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
