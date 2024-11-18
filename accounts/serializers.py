from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password, check_password

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user and check_password(data['password'], user.password):
            return user
        raise serializers.ValidationError("Invalid login credentials")
