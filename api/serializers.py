from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Event
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email','phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None or password is None:
            raise serializers.ValidationError('Username and password are required to log in.')
        user = get_user_model().objects.filter(username=username).first()
        if user is None:
            raise serializers.ValidationError('No user with this username.')
        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password.')
        data['user'] = user
        return data

class EventSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'location', 'creator']

    def validate_date(self, value):
        # Add any validation logic for the date field if needed
        return value