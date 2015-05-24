from django.contrib import admin

# Register your models here.


from .models import Satellite
from .models import Tle

admin.site.register(Satellite)

admin.site.register(Tle)