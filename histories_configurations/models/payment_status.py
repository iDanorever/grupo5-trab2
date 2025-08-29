from django.db import models
from django.utils import timezone


class PaymentStatus(models.Model):
    """
    Modelo para estados de pago.
    Basado en la estructura de la tabla payment_status de la BD.
    """
    
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Eliminado en")
    
    class Meta:
        db_table = 'payment_status'
        verbose_name = 'Estado de pago'
        verbose_name_plural = 'Estados de pago'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def soft_delete(self):
        """Soft delete del estado de pago"""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
    
    def restore(self):
        """Restaurar estado de pago eliminado"""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])
