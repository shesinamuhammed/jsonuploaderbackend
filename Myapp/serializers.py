import imp
from rest_framework import serializers
from django.contrib.auth.models import User
from Myapp.models import JsonData
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user
    
class JsonUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonData
        fields = ('json_data', 'user')
        


    def create(self, validated_data):
        json_data = JsonData.objects.create(json_data = validated_data['json_data'], user = validated_data['user'])

        return json_data
        