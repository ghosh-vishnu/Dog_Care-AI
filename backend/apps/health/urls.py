from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VaccinationViewSet, HealthRecordViewSet

app_name = 'health'

router = DefaultRouter()
router.register(r'vaccinations', VaccinationViewSet, basename='vaccination')
router.register(r'health-records', HealthRecordViewSet, basename='health-record')

urlpatterns = [
    path('', include(router.urls)),
]
