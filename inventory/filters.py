import django_filters
from .models import InventoryItem


class InventoryItemFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    low_stock = django_filters.NumberFilter(method='filter_low_stock')


    class Meta:
        model = InventoryItem
        fields = ['category']


    def filter_low_stock(self, queryset, name, value):
        try:
            threshold = int(value)
        except (TypeError, ValueError):
            threshold = 5
        return queryset.filter(quantity__lte=threshold)