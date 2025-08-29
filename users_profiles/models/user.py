from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    """
    Modelo de usuario personalizado.
    Basado en la estructura de la tabla users de la BD.
    """
    
    # Campos críticos de autenticación
    document_number = models.CharField(max_length=255, unique=True, verbose_name="Número de documento")
    photo_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="URL de foto")
    name = models.CharField(max_length=255, verbose_name="Nombres")
    paternal_lastname = models.CharField(max_length=255, verbose_name="Apellido paterno")
    maternal_lastname = models.CharField(max_length=255, verbose_name="Apellido materno")
    email = models.CharField(max_length=255, unique=True, verbose_name="Correo electrónico")
    sex = models.CharField(max_length=1, verbose_name="Sexo")
    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name="Teléfono")
    user_name = models.CharField(max_length=150, unique=True, verbose_name="Nombre de usuario")
    password = models.CharField(max_length=150, verbose_name="Contraseña")
    password_change = models.BooleanField(default=False, verbose_name="Requiere cambio de contraseña")
    last_session = models.DateTimeField(blank=True, null=True, verbose_name="Última sesión")
    account_statement = models.CharField(max_length=1, default='A', verbose_name="Estado de cuenta")
    email_verified_at = models.DateTimeField(blank=True, null=True, verbose_name="Email verificado en")
    document_type = models.ForeignKey(
        'histories_configurations.DocumentType',
        on_delete=models.CASCADE,
        verbose_name="Tipo de documento",
        null=True,
        blank=True
    )
    country = models.ForeignKey(
        'ubi_geo.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="País"
    )
    remember_token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Token de recordatorio")

    # Campos de control
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Eliminado en")
    
    # Configuración de autenticación
    USERNAME_FIELD = 'email'  # Se autentica por email
    REQUIRED_FIELDS = ['user_name', 'document_number']  # Campos requeridos para createsuperuser
    
    class Meta:
        db_table = 'users'  # Para mantener el nombre de tu tabla
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.name} {self.paternal_lastname} - {self.document_number}"
    
    def soft_delete(self):
        """Soft delete del usuario"""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
    
    def restore(self):
        """Restaurar usuario eliminado"""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])
    
    def get_full_name(self):
        """Nombre completo"""
        return f"{self.name} {self.paternal_lastname} {self.maternal_lastname}"
    
    def verify_email(self):
        """Marca el email como verificado"""
        self.email_verified_at = timezone.now()
        self.save(update_fields=['email_verified_at'])