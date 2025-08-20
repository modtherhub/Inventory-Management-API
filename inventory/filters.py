import django_filters
from .models import InventoryItem

# FilterSet for InventoryItem
# Provides advanced filtering for the inventory API
# Supports filtering by price range, category, & low stock threshold
class InventoryItemFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte') # Praice >= min_praice
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte') # Praice <= max_praice
    
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains') # category Flexible Match
    # Custom boolean filter for low stock items
    # ﻻy default, returns items with quantity less than 5
    # هf the user provides a custom threshold (low_stock_threshold), use that instead
    low_stock = django_filters.BooleanFilter(method='filter_low_stock')


    class Meta:
        model = InventoryItem
        fields = ['category', 'min_price', 'max_price', 'low_stock']

    
    def filter_low_stock(self, queryset, name, value):
        if value:  # filter only if user activated the boolean filter
            try:
                # try to get the user-defined threshold from query params
                threshold = int(self.request.query_params.get('low_stock_threshold', 5))
            except (TypeError, ValueError):
                # fallback to default threshold if invalid input
                threshold = 5
            return queryset.filter(quantity__lt=threshold)  # return items below the threshold
        return queryset  # return all items if filter not activated