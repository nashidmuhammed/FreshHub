from onlinefoods.models import product
import django_filters


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = product
        fields = ['pname',]