from .views import EventosViewSets
from rest_framework import routers
from django.urls import path, include

router = routers.DefaultRouter()
router.register('eventos',EventosViewSets)

urlpatterns = [
    path('', include(router.urls))
]
