import django_filters
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):  # defines what query params are allowed for filtering employees

    designation = django_filters.CharFilter(
        field_name='designation',
        lookup_expr='iexact'  # case-insensitive EXACT match (e.g. "manager" matches "Manager", but not "managers")
    )

    emp_name = django_filters.CharFilter(field_name='emp_name', lookup_expr='icontains')  # case-insensitive PARTIAL match (e.g. "raj" matches "Rajesh")

    # id = django_filters.RangeFilter(field_name='id')  # commented out - built-in way to do range filtering, but custom version used below instead

    # custom filtering
    id_min = django_filters.CharFilter(method='filter_by_id_range', label='From EMP ID')  # ?id_min=5 -> calls filter_by_id_range below
    id_max = django_filters.CharFilter(method='filter_by_id_range', label='To EMP ID')  # ?id_max=10 -> calls filter_by_id_range below

    def filter_by_id_range(self, queryset, name, value):  # custom method - runs whenever id_min or id_max is used
        if name == "id_min":
            return queryset.filter(emp_id__gte=value)  # emp_id >= value (greater than or equal)

        if name == "id_max":
            return queryset.filter(emp_id__lte=value)  # emp_id <= value (less than or equal)

        return queryset  # fallback - return unfiltered queryset if neither matched