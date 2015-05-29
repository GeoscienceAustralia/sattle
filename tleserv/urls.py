from rest_framework.routers import DefaultRouter

from . import views


router2 = DefaultRouter()
router2.register(r'satellites', views.SatelliteViewSet)
router2.register(r'tles', views.TleViewSet)
#router.register(r'users', views.UserViewSet)
