from rest_framework import authentication, permissions, viewsets, filters

from .forms import SatelliteFilter, TleFilter
from .models import Satellite, Tle
from .serializers import SatelliteSerializer, TleSerializer


class DefaultsMixin(object):
    """Default settings for view authentication, permissions, filtering
     and pagination."""
    
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,    
    )
    permission_classes = (
        # permissions.IsAuthenticated,
        permissions.IsAuthenticatedOrReadOnly,
    )
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 10
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class SatelliteViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating Satellites."""
    
    queryset = Satellite.objects.order_by('norad_number')
    serializer_class = SatelliteSerializer
    #filter_class = SatelliteFilter
    search_fields = ('satname', )
    ordering_fields = ('norad_number', 'satname', )
    

class TleViewSet(DefaultsMixin, viewsets.ModelViewSet):
    """API endpoint for listing and creating TLEs."""
    
    queryset = Tle.objects.all()
    serializer_class = TleSerializer
    filter_class = TleFilter
    search_fields = ('norad_number',  )
    #OK ordering_fields = ('epochsec', 'tleid' , )
    ordering_fields = ('epochsec')
    # to get Latest TLE: http://127.0.0.1:8000/sattle/tleserv/tles/?format=json&norad_number=33591&ordering=-epochsec
    #http://127.0.0.1:8000/sattle/tleserv/tles/?norad_number=33591&ordering=epochsec&page=2
    
