from django.db import models
from django.conf import settings
from django.utils import timezone

class UserVerificationCode(models.Model):
    """
    Modelo para códigos de verificación de usuarios
    Relacionado con la tabla user_verification_codes de la BD
    """
    
    # Relación con el usuario
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='verification_codes',
        verbose_name='Usuario'
    )
    
    # Código de verificación
    code = models.CharField(max_length=6, verbose_name='Código de verificación')
    
    # Fecha de expiración
    expires_at = models.DateTimeField(verbose_name='Expira en')
    
    # Intentos fallidos
    failed_attempts = models.PositiveIntegerField(
        default=0,
        verbose_name='Intentos fallidos'
    )
    
    # Bloqueo temporal
    locked_until = models.DateTimeField(
        blank=True, null=True,
        verbose_name='Bloqueado hasta'
    )
    
    # Campos de control
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')
    
    class Meta:
        db_table = 'user_verification_codes'  # Nombre exacto de tu tabla
        verbose_name = 'Código de verificación de usuario'
        verbose_name_plural = 'Códigos de verificación de usuarios'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Código {self.code} para {self.user.user_name}"
    
    def is_expired(self):
        """Verifica si el código ha expirado"""
        return timezone.now() > self.expires_at
    
    def is_locked(self):
        """Verifica si el código está temporalmente bloqueado"""
        return self.locked_until and timezone.now() < self.locked_until
    
    def increment_failed_attempts(self):
        """Incrementa los intentos fallidos"""
        self.failed_attempts += 1
        self.save(update_fields=['failed_attempts', 'updated_at'])
    
    def lock_temporarily(self, minutes=15):
        """Bloquea el código temporalmente"""
        self.locked_until = timezone.now() + timezone.timedelta(minutes=minutes)
        self.save(update_fields=['locked_until', 'updated_at'])
    
    def unlock(self):
        """Desbloquea el código"""
        self.locked_until = None
        self.failed_attempts = 0
        self.save(update_fields=['locked_until', 'failed_attempts', 'updated_at'])
    
    def is_valid(self):
        """Verifica si el código es válido para usar"""
        return not self.is_expired() and not self.is_locked()
    
    @classmethod
    def create_code(cls, user, code_length=6, expiration_minutes=15):
        """Crea un nuevo código de verificación"""
        import random
        import string
        
        # Generar código aleatorio
        code = ''.join(random.choices(string.digits, k=code_length))
        
        # Invalidar códigos anteriores del usuario
        cls.objects.filter(user=user, expires_at__gt=timezone.now()).update(
            expires_at=timezone.now()
        )
        
        # Crear nuevo código
        return cls.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timezone.timedelta(minutes=expiration_minutes)
        )