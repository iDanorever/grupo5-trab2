# users_profiles/models/user.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import FileExtensionValidator

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    # Desactivar campos de AbstractUser que NO existen en tu tabla
    username   = None
    first_name = None
    last_name  = None

    # Login por email
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")

    # last_login se maneja automáticamente por Django

    # Campos básicos para funcionamiento
    document_number = models.CharField(max_length=20, unique=True, verbose_name="Número de documento")
    user_name = models.CharField(max_length=50, unique=True, verbose_name="Nombre de usuario")
    name = models.CharField(max_length=100, verbose_name="Nombres")
    paternal_lastname = models.CharField(max_length=100, verbose_name="Apellido paterno")
    maternal_lastname = models.CharField(max_length=100, verbose_name="Apellido materno")

    # document_type = models.ForeignKey('histories_configurations.DocumentType',
    #                                   on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tipo de documento")
    # country = models.ForeignKey('ubi_geo.Country',
    #                             on_delete=models.SET_NULL, null=True, blank=True, verbose_name="País")

    # Campos de timestamp básicos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")

    objects = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['user_name', 'document_number']

    class Meta:
        db_table = 'users'
        managed = True  # Django gestiona la tabla
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.name} {self.paternal_lastname} - {self.document_number}"

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])

    def get_full_name(self):
        return f"{self.name} {self.paternal_lastname} {self.maternal_lastname}"

    def verify_email(self):
        self.email_verified_at = timezone.now()
        self.save(update_fields=['email_verified_at'])
