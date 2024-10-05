from django_filters import FilterSet
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = '__all__'
