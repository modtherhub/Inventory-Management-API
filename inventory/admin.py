from django.contrib import admin
from .models import InventoryItem, InventoryChangeLog

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'quantity', 'price', 'category', 'last_updated')
    list_filter = ('category', 'owner')
    search_fields = ('name', 'description', 'category', 'owner__username')
    ordering = ('-last_updated',)


@admin.register(InventoryChangeLog)
class InventoryChangeLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'changed_by', 'old_quantity', 'new_quantity', 'change_type', 'change_date')
    list_filter = ('change_type', 'changed_by')
    search_fields = ('item__name', 'changed_by__username')
    ordering = ('-change_date',)
