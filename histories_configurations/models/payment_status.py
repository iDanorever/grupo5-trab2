# histories_configurations/models/payment_status.py
from django.db import models

class PaymentStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'payment_status'   # <- coincide con tu tabla
        managed = False               # <- NO generar/alterar tabla vía migraciones
        verbose_name = "Estado de pago"
        verbose_name_plural = "Estados de pago"

    def __str__(self):
        return self.name
