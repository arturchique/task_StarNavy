from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('name', 'content', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ('id', 'username', 'first_name', 'last_name')


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ('id', 'username', 'is_active', 'last_login', 'date_joined')