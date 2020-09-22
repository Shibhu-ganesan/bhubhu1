import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
    start = DateFilter(field_name = 'date', lookup_expr = 'gte')
    end = DateFilter(field_name = 'date', lookup_expr = 'lte')
    note = CharFilter(field_name='note', lookup_expr='icontains')
    class Meta:
        model = Status
        fields = '__all__'
        exclude = ['customer','date']

