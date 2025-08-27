from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TherapistViewSet,
    index
)

router = DefaultRouter()
router.register(r'therapists', TherapistViewSet, basename='therapist')

urlpatterns = [
    path('', index, name='therapists_index'),  # Página principal en /
    path('', include(router.urls)),  # APIs disponibles en la raíz
]