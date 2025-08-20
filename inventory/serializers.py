from rest_framework import serializers
from .models import InventoryItem, InventoryChangeLog
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

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

    # Field-level validations
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
    
# serializer for inventory Change logs
# read-only, Display changes made to inventory items
# shows the user who made the change & the item affected
class InventoryChangeLogSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(read_only=True)
    changed_by = serializers.ReadOnlyField(source='changed_by.username')

    class Meta:
        model = InventoryChangeLog
        fields = [
            'id', 'item', 'changed_by', 'old_quantity', 'new_quantity', 'change_type', 'change_date'
        ]

# Serializer for Users
# Admin-facing to manage users
# Only includes basic fields for display and management
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

class UserRegisterSerializer(serializers.ModelSerializer):
    # ensure username is required and unique across all users
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]  
    )
    # validate email as required and enforce uniqueness
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]  
    )
    # password is write-only and must meet minimum length
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # use Django's built-in user creation to handle password hashing
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    