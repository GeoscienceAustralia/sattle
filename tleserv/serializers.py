from datetime import date

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Satellite, Tle


User = get_user_model()


class SatelliteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Satellite
        fields = ('url', 'norad_number', 'satname', 'isactive', )
            

class TleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tle
        fields = ('url', 'tleid', 'line1', 'line2', 'norad_number', 'epochsec', 'tle_dt_utc', 'inp_dt_utc', 'status')

