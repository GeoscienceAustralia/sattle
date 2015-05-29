from django.contrib import admin

# Register your models here.


from .models import Satellite
from .models import Tle

# make/register the tables to appear in web UI
admin.site.register(Satellite)

admin.site.register(Tle)


