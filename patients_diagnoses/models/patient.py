from django.db import models
from django.utils import timezone

class Patient(models.Model):
    # Información personal
    document_number = models.CharField(max_length=20, unique=True)
    paternal_lastname = models.CharField(max_length=100)
    maternal_lastname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    personal_reference = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField()
    sex = models.CharField(max_length=10, choices=[
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    ])

    # Información de contacto
    primary_phone = models.CharField(max_length=15)
    secondary_phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Información adicional
    ocupation = models.CharField(max_length=100, blank=True, null=True)
    health_condition = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)

    # Relaciones con otras apps
    # (Ahora referenciadas explícitamente a la app ubi_geo para evitar E300/E307)
    region = models.ForeignKey('ubi_geo.Region', on_delete=models.PROTECT, related_name='medical_patients')
    province = models.ForeignKey('ubi_geo.Province', on_delete=models.PROTECT, related_name='medical_patients')
    district = models.ForeignKey('ubi_geo.District', on_delete=models.PROTECT, related_name='medical_patients')

    # Usando el modelo de DocumentType de histories_configurations
    document_type = models.ForeignKey(
        'histories_configurations.DocumentType',
        on_delete=models.PROTECT,
        related_name='medical_patients'
    )

    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'patients'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-created_at']

    def soft_delete(self):
        """Soft delete del paciente."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def restore(self):
        """Restaura un paciente eliminado."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])

    def get_full_name(self):
        """Obtiene el nombre completo del paciente."""
        return f"{self.name} {self.paternal_lastname} {self.maternal_lastname}"

    def __str__(self):
        return self.get_full_name()
