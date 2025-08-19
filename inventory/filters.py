import django_filters
from .models import InventoryItem

# FilterSet for InventoryItem
# Provides advanced filtering for the inventory API
# Supports filtering by price range, category, & low stock threshold
class InventoryItemFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte') # Praice >= min_praice
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte') # Praice <= max_praice
    
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact') # exact category match
    low_stock = django_filters.NumberFilter(method='filter_low_stock') # custom filter for items with low quantity


    class Meta:
        model = InventoryItem
        fields = ['category', 'min_price', 'max_price', 'low_stock']

    # custom filter method
    # returns items with quantity less than - equal to the given threshold
    # defaults to 5 if value is missing - invalid
    def filter_low_stock(self, queryset, name, value):
        try:
            threshold = int(value)
        except (TypeError, ValueError):
            threshold = 5
        return queryset.filter(quantity__lte=threshold)