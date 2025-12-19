from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

User = get_user_model()

# Serializer for User Registration
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['username', 'password', 'bio', 'profile_picture', 'followers']
        extra_kwargs = {
            'bio': {'required': False},
            'profile_picture': {'required': False},
            'followers': {'required': False},
        }

    def create(self, validated_data):
        # Hash the password and create the user
        password = validated_data.pop('password')
        user = get_user_model().objects.create_user(**validated_data)  # Using create_user to ensure password hashing
        user.set_password(password)
        user.save()

        # Create a token for the newly created user
        Token.objects.create(user=user)
        return user

# Serializer for User Profile (viewing profile)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'bio', 'profile_picture', 'followers']

# Serializer for Login (authentication)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        # Create or retrieve a token
        token, created = Token.objects.get_or_create(user=user)
        return {'token': token.key}
