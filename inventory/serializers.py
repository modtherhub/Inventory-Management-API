from rest_framework import serializers
from .models import InventoryItem, InventoryChangeLog
from django.contrib.auth import get_user_model

User = get_user_model()

class InventoryItemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    date_added = serializers.DateTimeField(read_only=True)
    last_updated = serializers.DateTimeField(read_only=True)


    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'description', 'quantity', 'price', 'category',
            'date_added', 'last_updated', 'owner'
        ]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError('Name is required.')
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('Quantity cannot be negative.')
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Price cannot be negative.')
        return value
    

class InventoryChangeLogSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(read_only=True)
    changed_by = serializers.ReadOnlyField(source='changed_by.username')

    class Meta:
        model = InventoryChangeLog
        fields = [
            'id', 'item', 'changed_by', 'old_quantity', 'new_quantity', 'change_type', 'change_date'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']
