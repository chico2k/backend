from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserListSerializer(serializers.Serializer):
    """
    Serializer for User List
    """
    id = serializers.IntegerField()
    email = serializers.EmailField()
    name = serializers.CharField()
    date_joined = serializers.DateTimeField()
