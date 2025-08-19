from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

# Serializer for User model
# handles user creation and update, including password hashing
# Password is write-only and must be at least 8 characters
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)


    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # hash the password
        user.save()
        return user

    # Update an existing user
    # allows updating password and other fields
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if password:
            instance.set_password(password) # hash the new password
        instance.save()
        return instance