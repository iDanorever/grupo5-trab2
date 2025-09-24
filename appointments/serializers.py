from rest_framework import serializers
from .models import Cita
import os

class CitaSerializer(serializers.ModelSerializer):
    # 👇 Esto es solo un campo de entrada, no se guarda en la DB
    calendar_id = serializers.CharField(
        required=False,  # ya no es obligatorio
        write_only=True  # no se devuelve en la respuesta
    )

    class Meta:
        model = Cita
        fields = ["id", "paciente", "fecha", "duracion", "ghl_event_id", "calendar_id"]

    def validate_calendar_id(self, value):
        """
        Si no se pasa calendar_id en la request, usar el del .env
        """
        if not value:
            value = os.getenv("CALENDAR_ID")
        return value