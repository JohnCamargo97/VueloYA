import django_filters
from .models import Vuelo, aerolinea

class vueloFilter(django_filters.FilterSet):
    AEROLINEAS = Vuelo.objects.all().values_list('id_aerolinea', 'id_aerolinea')
    id_aerolinea = django_filters.MultipleChoiceFilter(choices=AEROLINEAS)
    #price = django_filters.RangeFilter()
    class Meta:
        model = Vuelo
        fields = {
            'precio': ['lt'],
            'id_aerolinea': ['exact'],
        }