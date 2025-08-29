# users_profiles/models/user.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import FileExtensionValidator

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _ensure_defaults(self, extra_fields):
        """
        Completa valores por defecto para campos obligatorios que createsuperuser NO solicita.
        También garantiza un document_type por defecto buscando por name="General"
        (tu DocumentType no tiene campo 'code').
        """
        # Defaults para campos de texto obligatorios
        extra_fields.setdefault("name", "")
        extra_fields.setdefault("paternal_lastname", "")
        extra_fields.setdefault("maternal_lastname", "")
        extra_fields.setdefault("sex", "O")  # M/F/O

        # Asegurar document_type (FK requerida)
        if not extra_fields.get("document_type"):
            try:
                from histories_configurations.models import DocumentType

                # 1) intenta encontrar uno existente por nombre
                dt = DocumentType.objects.filter(name__iexact="General").first()

                # 2) si no existe, intenta crearlo con el mínimo posible
                if not dt:
                    try:
                        dt = DocumentType.objects.create(name="General")
                    except Exception:
                        # si tu modelo exige más campos (p. ej. description), intenta con descripción
                        dt = DocumentType.objects.create(
                            name="General",
                            description="Tipo por defecto"
                        )

                extra_fields["document_type"] = dt

            except Exception as e:
                # Mensaje claro si no se pudo resolver el DocumentType
                raise ValueError(
                    "No se pudo asignar un DocumentType por defecto. "
                    "Crea uno en histories_configurations.DocumentType con name='General' "
                    f"o pásalo explícitamente al crear el usuario. Detalle: {e}"
                )
        return extra_fields

    # NOTA: acepta user_name (NO username) porque REQUIRED_FIELDS pide user_name
    def create_user(self, email, user_name, document_number, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        if not user_name:
            raise ValueError("El nombre de usuario (user_name) es obligatorio")
        if not document_number:
            raise ValueError("El número de documento es obligatorio")

        email = self.normalize_email(email)

        # Sincroniza el 'username' heredado con tu 'user_name'
        username = extra_fields.pop("username", user_name)

        # Completa defaults para campos requeridos y document_type
        extra_fields = self._ensure_defaults(extra_fields)

        user = self.model(
            email=email,
            username=username,        # campo heredado de AbstractUser
            user_name=user_name,      # tu campo adicional
            document_number=document_number,
            **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, document_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(email, user_name, document_number, password, **extra_fields)


class User(AbstractUser):
    # Campos críticos de autenticación
    document_number = models.CharField(max_length=20, unique=True, verbose_name="Número de documento")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")

    # AbstractUser YA trae 'username'; además defines 'user_name'
    user_name = models.CharField(max_length=50, unique=True, verbose_name="Nombre de usuario")

    # Campos personales
    photo_url = models.ImageField(
        upload_to="users/photos/",  # Carpeta dentro de MEDIA_ROOT
        blank=True,
        null=True,
        verbose_name="Foto de perfil",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])]
    )
    name = models.CharField(max_length=100, verbose_name="Nombres")
    paternal_lastname = models.CharField(max_length=100, verbose_name="Apellido paterno")
    maternal_lastname = models.CharField(max_length=100, verbose_name="Apellido materno")
    sex = models.CharField(
        max_length=1,
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')],
        verbose_name="Sexo"
    )
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")

    # Seguridad / verificación
    password_change = models.BooleanField(default=False, verbose_name="Requiere cambio de contraseña")
    last_session = models.DateTimeField(blank=True, null=True, verbose_name="Última sesión")
    account_statement = models.CharField(max_length=20, default='active', verbose_name="Estado de cuenta")
    email_verified_at = models.DateTimeField(blank=True, null=True, verbose_name="Email verificado en")
    remember_token = models.CharField(max_length=100, blank=True, null=True, verbose_name="Token de recordatorio")

    # FK requerida
    document_type = models.ForeignKey(
        'histories_configurations.DocumentType',
        on_delete=models.PROTECT,
        verbose_name="Tipo de documento"
    )

    # Timestamps / soft delete
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Eliminado en")

    # Manager personalizado
    objects = UserManager()

    # Autenticación
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'document_number']

    class Meta:
        db_table = 'users'
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
