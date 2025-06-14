from django.contrib.auth import get_user_model
from django.db.models import JSONField
from django_filters import CharFilter, NumberFilter, DateFilter, DateTimeFilter, BooleanFilter, RangeFilter
from django_filters import FilterSet
from . import models

# Get user model
User = get_user_model()

# define JSONField filter support more lookup_expr
def generate_jsonfield_filter(lookup_expr, filter_class):
    """
    create JSONField filter parameter
    :param lookup_expr: get（exact, icontains...）
    :return: filter parameter
    """
    return {
        JSONField: {
            'filter_class': filter_class,
            'extra': lambda f: {
                'lookup_expr': lookup_expr
            },
        }
    }

JSONFIELD_FILTER_OVERRIDE = {
    # String filters
    **generate_jsonfield_filter('exact', CharFilter),
    **generate_jsonfield_filter('iexact', CharFilter),
    **generate_jsonfield_filter('contains', CharFilter),
    **generate_jsonfield_filter('icontains', CharFilter),
    # Number filters (support integers and floats)
    **generate_jsonfield_filter('exact', NumberFilter),  # exact match for numbers (int/float)
    **generate_jsonfield_filter('lt', NumberFilter),  # less than
    **generate_jsonfield_filter('lte', NumberFilter),  # less than or equal
    **generate_jsonfield_filter('gt', NumberFilter),  # greater than
    **generate_jsonfield_filter('gte', NumberFilter),  # greater than or equal
    # Boolean filters
    **generate_jsonfield_filter('exact', BooleanFilter),  # exact match for boolean values
    # Date filters
    **generate_jsonfield_filter('exact', DateFilter),  # exact match for dates
    **generate_jsonfield_filter('lt', DateFilter),  # less than
    **generate_jsonfield_filter('lte', DateFilter),  # less than or equal
    **generate_jsonfield_filter('gt', DateFilter),  # greater than
    **generate_jsonfield_filter('gte', DateFilter),  # greater than or equal
    # DateTime filters
    **generate_jsonfield_filter('exact', DateTimeFilter),  # exact match for datetime
    **generate_jsonfield_filter('lt', DateTimeFilter),  # less than
    **generate_jsonfield_filter('lte', DateTimeFilter),  # less than or equal
    **generate_jsonfield_filter('gt', DateTimeFilter),  # greater than
    **generate_jsonfield_filter('gte', DateTimeFilter),  # greater than or equal
    # Range filters
    **generate_jsonfield_filter('range', RangeFilter),  # range filter for numbers, dates, etc.
}

class UserFilter(FilterSet):
    """
    User filter
    """
    class Meta:
        model = models.User
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class PermissionFilter(FilterSet):
    """
    Permission filter
    """
    class Meta:
        model = models.Permission
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class FileFilter(FilterSet):
    """
    File filter
    """
    class Meta:
        model = models.Files
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class TeamFilter(FilterSet):
    """
    Team filter
    """
    class Meta:
        model = models.Team
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class DepartmentFilter(FilterSet):
    """
    Team filter
    """
    class Meta:
        model = models.Department
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class APIFilter(FilterSet):
    """
    API filter
    """
    class Meta:
        model = models.API
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class ExampleFilter(FilterSet):
    """
    Example filter
    """
    class Meta:
        model = models.Example
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class PidsFilter(FilterSet):
    """
    Pids filter
    """
    class Meta:
        model = models.Pids
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class PyPiFilter(FilterSet):
    """
    Pids filter
    """
    class Meta:
        model = models.PyPi
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class CPUFilter(FilterSet):
    """
    CPU filter
    """
    class Meta:
        model = models.CPU
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class MemoryFilter(FilterSet):
    """
    Memory filter
    """
    class Meta:
        model = models.Memory
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class DiskFilter(FilterSet):
    """
    Disk filter
    """
    class Meta:
        model = models.Disk
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE



class NetworkFilter(FilterSet):
    """
    Network filter
    """
    class Meta:
        model = models.Network
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class GoodsFilter(FilterSet):
    """
    Goods filter
    """
    class Meta:
        model = models.Goods
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class BinFilter(FilterSet):
    """
    Bin filter
    """
    class Meta:
        model = models.Bin
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class StockFilter(FilterSet):
    """
    Stock filter
    """
    class Meta:
        model = models.Stock
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class CapitalFilter(FilterSet):
    """
    Capital filter
    """
    class Meta:
        model = models.Capital
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class SupplierFilter(FilterSet):
    """
    Supplier filter
    """
    class Meta:
        model = models.Supplier
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class CustomerFilter(FilterSet):
    """
    Customer filter
    """
    class Meta:
        model = models.Customer
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class ASNFilter(FilterSet):
    """
    ASN filter
    """
    class Meta:
        model = models.ASN
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class DNFilter(FilterSet):
    """
    DN filter
    """
    class Meta:
        model = models.DN
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class PurchaseFilter(FilterSet):
    """
    Purchase filter
    """
    class Meta:
        model = models.Purchase
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class BarFilter(FilterSet):
    """
    Bar filter
    """
    class Meta:
        model = models.Bar
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class FeeFilter(FilterSet):
    """
    Fee filter
    """
    class Meta:
        model = models.Fee
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE


class DriverFilter(FilterSet):
    """
    Driver filter
    """
    class Meta:
        model = models.Driver
        fields = '__all__'
        filter_overrides = JSONFIELD_FILTER_OVERRIDE