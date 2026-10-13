from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ["id", "email", "password","first_name", "last_name"]
        read_only_fields = ["id"]
        
    def validate_email(self, value):
        return value.strip().lower()
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]
        read_only_fields = fields
