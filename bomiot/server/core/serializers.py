from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Files

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, required=False)
    email = serializers.CharField(read_only=True, required=False)
    phone = serializers.CharField(read_only=True, required=False)
    permission = serializers.JSONField(read_only=True, required=False)
    request_limit = serializers.IntegerField(read_only=True, required=False)
    is_active = serializers.BooleanField(read_only=True, required=False)
    date_joined = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    last_login = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'is_active', 'request_limit', 'permission', 'date_joined', 'last_login', 'updated_time']
        read_only_fields = ['id']

class FileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, required=False)
    type = serializers.CharField(read_only=True, required=False)
    size = serializers.CharField(read_only=True, required=False)
    owner = serializers.CharField(read_only=True, required=False)
    shared_to = serializers.CharField(read_only=True, required=False)
    is_delete = serializers.BooleanField(read_only=True, required=False)
    created_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Files
        fields = ['id', 'name', 'type', 'size', 'owner', 'shared_to', 'is_delete', 'created_time', 'updated_time']
        read_only_fields = ['id']
