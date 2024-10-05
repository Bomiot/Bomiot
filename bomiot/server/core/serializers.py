from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, required=False)
    email = serializers.CharField(read_only=True, required=False)
    phone = serializers.CharField(read_only=True, required=False)
    is_active = serializers.BooleanField(read_only=True, required=False)
    vip_level = serializers.IntegerField(read_only=True, required=False)
    vip_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    date_joined = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    last_login = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(read_only=True, required=False, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'is_active', 'date_joined', 'last_login', 'update_time']
        read_only_fields = ['id']
