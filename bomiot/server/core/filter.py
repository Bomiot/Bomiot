from django.contrib.auth import get_user_model
from django.db.models import JSONField
from django_filters import CharFilter
from django_filters import rest_framework as filters
from . import models

# Get user model
User = get_user_model()

# define JSONField filter support more lookup_expr
def generate_jsonfield_filter(lookup_expr):
    """
    create JSONField filter parameter
    :param lookup_expr: get（exact, icontains...）
    :return: filter parameter
    """
    return {
        JSONField: {
            'filter_class': CharFilter,
            'extra': lambda f: {
                'lookup_expr': lookup_expr,
            },
        }
    }

# combine lookup_expr
JSONFIELD_FILTER_OVERRIDE = {
    **generate_jsonfield_filter('exact'),
    **generate_jsonfield_filter('iexact'),
    **generate_jsonfield_filter('contains'),
    **generate_jsonfield_filter('icontains'),
    **generate_jsonfield_filter('startswith'),
    **generate_jsonfield_filter('endswith'),
    **generate_jsonfield_filter('gt'),
    **generate_jsonfield_filter('gte'),
    **generate_jsonfield_filter('lt'),
    **generate_jsonfield_filter('lte'),
}

class UserFilter(filters.FilterSet):
    """
    User filter
    """
    class Meta:
        model = models.User
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class FileFilter(filters.FilterSet):
    """
    File filter
    """
    class Meta:
        model = models.Files
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class TeamFilter(filters.FilterSet):
    """
    Team filter
    """
    class Meta:
        model = models.Team
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class DepartmentFilter(filters.FilterSet):
    """
    Team filter
    """
    class Meta:
        model = models.Department
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class PidsFilter(filters.FilterSet):
    """
    Pids filter
    """
    class Meta:
        model = models.Pids
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class PyPiFilter(filters.FilterSet):
    """
    Pids filter
    """
    class Meta:
        model = models.PyPi
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class CPUFilter(filters.FilterSet):
    """
    CPU filter
    """
    class Meta:
        model = models.CPU
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class MemoryFilter(filters.FilterSet):
    """
    Memory filter
    """
    class Meta:
        model = models.Memory
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class DiskFilter(filters.FilterSet):
    """
    Disk filter
    """
    class Meta:
        model = models.Disk
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE



class NetworkFilter(filters.FilterSet):
    """
    Network filter
    """
    class Meta:
        model = models.Network
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE