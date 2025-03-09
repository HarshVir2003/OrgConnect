from rest_framework import serializers
from django.contrib.auth.models import User
from User.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={"input_type": 'password'})
    image = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password_confirm', 'image']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("password does not match!")
        return data

    def create(self, data):
        data.pop("password_confirm")
        user = User.objects.create_user(**data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True, style={"input_type": 'password'})

    class Meta:
        fields = ['username', 'password']
