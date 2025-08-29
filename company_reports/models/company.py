from django.db import models
from django.conf import settings

class CompanyData(models.Model):
    """
    Modelo para gestionar los datos de la empresa.
    Basado en la estructura de la tabla table_company_data de la BD.
    """
    
    company_name = models.CharField(max_length=266, verbose_name="Nombre de la empresa")
    company_logo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Logo de la empresa")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    def get_logo_url(self):
        """
        Retorna la URL del logo de la empresa o None si no tiene logo
        """
        if self.company_logo:
            return f"{settings.MEDIA_URL}{self.company_logo}"
        return None

    def has_logo(self):
        return bool(self.company_logo)

    def __str__(self):
        return self.company_name
    
    class Meta:
        db_table = 'table_company_data'
        verbose_name = "Datos de la Empresa"
        verbose_name_plural = "Datos de las Empresas"
        ordering = ['company_name'] 