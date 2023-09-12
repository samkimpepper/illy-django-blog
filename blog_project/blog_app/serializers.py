from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        username = data.get('username')
        is_exists = User.objects.filter(username=username).exists()
        
        if is_exists:
            raise serializers.ValidationError('존재하는 닉네임입니다.')
        
        return data 
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=100, write_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError('유저네임을 입력하세요.')
        
        if password is None:
            raise serializers.ValidationError('비밀번호를 입력하세요.')
        
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('유저네임 혹은 비밀번호가 틀렸습니다.')
        
        return data 