from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetViewSet

app_name = 'pets'

router = DefaultRouter()
router.register(r'pets', PetViewSet, basename='pet')

urlpatterns = [
    path('', include(router.urls)),
]
