import django_filters

from django.contrib.auth import get_user_model

#from .models import Satellite, Tle
from .models import Satellite, Tle


User = get_user_model()


class NullFilter(django_filters.BooleanFilter):
    """Filter on a field set as null or not."""
    
    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{'%s__isnull' % self.name: value})
        return qs
        
        
class SatelliteFilter(django_filters.FilterSet):
    
    #end_min = django_filters.DateFilter(name='end', lookup_type='gte')
    #end_max = django_filters.DateFilter(name='end', lookup_type='lte')
    
    class Meta:
        model = Satellite
        #fields = ('isactive', 'satname', )
        fields = ('isactive',)


class TleFilter(django_filters.FilterSet):
    
    #norad_number = django_filters.NumberFilter(lookup_type='eq')
    
    class Meta:
        model = Tle
        fields = ('norad_number',  )
        
    def __init__(self, *args, **kwargs):
        #FEI super().__init__(*args, **kwargs)
        super(TleFilter, self).__init__(*args, **kwargs)
        #self.filters['assigned'].extra.update( {'to_field_name': User.USERNAME_FIELD})
