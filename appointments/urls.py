from django.urls import path
from .views import crear_cita

urlpatterns = [
    path("crear/", crear_cita, name="crear_cita"),
]