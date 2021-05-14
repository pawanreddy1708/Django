from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4),

    class Meta:
        model = User
        fields = ['username', 'email', 'password','phone']

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Email is already in use'})
        return attrs


    def create(self, validated_data):
      return User.objects.create_user(**validated_data)



class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=32,min_length=4)
    password = serializers.CharField(max_length=32,min_length=5,write_only=True)

    class Meta:
        model = User
        fields = ['username','password']