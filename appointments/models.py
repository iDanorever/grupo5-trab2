from django.db import models

class Cita(models.Model):
    paciente = models.CharField(max_length=255)
    fecha = models.DateTimeField()
    duracion = models.IntegerField(default=30)  # minutos
    calendar_id = models.CharField(max_length=255)  # ID del calendario GHL
    ghl_event_id = models.CharField(max_length=255, blank=True, null=True)  # ID en GHL si existe
    creado_en = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Cita de {self.paciente} - {self.fecha}"