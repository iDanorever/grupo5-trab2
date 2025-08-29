# users_profiles/admin.py

from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Q

# Import directo al archivo para evitar ambigüedades
from .models.user_verification_code import UserVerificationCode

User = get_user_model()

# -------------------------------------------------------------------
# Admin para el CustomUser (AUTH_USER_MODEL = 'users_profiles.User')
# -------------------------------------------------------------------

# Evita AlreadyRegistered si alguien ya lo registró
try:
    admin.site.unregister(User)
except NotRegistered:
    pass


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin del usuario personalizado.
    Solo usa campos que sabemos que existen en tu modelo.
    """

    list_display = (
        "user_name",
        "email",
        "name",
        "paternal_lastname",
        "maternal_lastname",
        "sex",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_display_links = ("user_name", "email")
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "sex",
        "date_joined",
    )
    search_fields = (
        "user_name",
        "email",
        "name",
        "paternal_lastname",
        "maternal_lastname",
    )
    ordering = ("-updated_at", "-date_joined")

    fieldsets = (
        ("Credenciales", {"fields": ("user_name", "email", "password")}),
        ("Información personal", {
            "fields": (
                "name",
                "paternal_lastname",
                "maternal_lastname",
                "sex",
                "photo_url",
                "phone",
            ),
        }),
        ("Permisos", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        ("Fechas", {
            "classes": ("collapse",),
            "fields": ("last_login", "date_joined", "updated_at", "deleted_at"),
        }),
        ("Identificación", {
            "classes": ("collapse",),
            "fields": ("document_type", "document_number"),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("user_name", "email", "password1", "password2"),
        }),
    )

    readonly_fields = ("last_login", "date_joined", "updated_at")


# -------------------------------------------------------------------
# Admin para UserVerificationCode (robusto ante variaciones de campos)
# Posibles nombres en proyectos distintos:
#   verification_type|type, target_email|email, is_used|used,
#   attempts|attempt_count, created_at, expires_at, max_attempts
# -------------------------------------------------------------------

def _get(obj, *names, default="—"):
    for n in names:
        if hasattr(obj, n):
            return getattr(obj, n)
    return default

@admin.display(description="Tipo verificación")
def col_verification_type(obj):
    return _get(obj, "verification_type", "type")

@admin.display(description="Email destino")
def col_target_email(obj):
    return _get(obj, "target_email", "email")

@admin.display(boolean=True, description="Usado")
def col_is_used(obj):
    return bool(_get(obj, "is_used", "used", default=False))

@admin.display(description="Intentos")
def col_attempts(obj):
    return _get(obj, "attempts", "attempt_count", default=0)

@admin.display(description="Máx. intentos")
def col_max_attempts(obj):
    return _get(obj, "max_attempts", default="—")

@admin.display(description="Creado")
def col_created_at(obj):
    return _get(obj, "created_at", default="—")

@admin.display(description="Expira")
def col_expires_at(obj):
    return _get(obj, "expires_at", default="—")


class UsedListFilter(admin.SimpleListFilter):
    title = "Estado (usado)"
    parameter_name = "used"

    def lookups(self, request, model_admin):
        return (("yes", "Usado"), ("no", "No usado"))

    def queryset(self, request, queryset):
        val = self.value()
        if val == "yes":
            return queryset.filter(Q(is_used=True) | Q(used=True))
        if val == "no":
            return queryset.filter(
                Q(is_used=False) | Q(used=False) | Q(is_used__isnull=True) | Q(used__isnull=True)
            )
        return queryset


class VerificationTypeListFilter(admin.SimpleListFilter):
    title = "Tipo de verificación"
    parameter_name = "vtype"

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        values = set(qs.values_list("verification_type", flat=True)) | set(qs.values_list("type", flat=True))
        values = sorted([v for v in values if v])
        return tuple((v, v) for v in values)

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        return queryset.filter(Q(verification_type=v) | Q(type=v))


@admin.register(UserVerificationCode)
class UserVerificationCodeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        col_verification_type,
        "code",
        col_target_email,
        col_is_used,
        col_attempts,
        col_max_attempts,
        col_created_at,
        col_expires_at,
    )
    list_filter = (VerificationTypeListFilter, UsedListFilter, "created_at", "expires_at")
    search_fields = ("user__user_name", "user__email", "code", "target_email", "email")
    ordering = ("-created_at",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        try:
            return qs.select_related("user")
        except Exception:
            return qs

    readonly_fields = ("created_at", "expires_at")
    fieldsets = (
        ("Información Básica", {
            "fields": ("user", "code"),
        }),
        ("Detalles", {
            "fields": ("verification_type", "target_email"),
            "description": "Si tu modelo usa otros nombres (p. ej. 'type' o 'email'), estos campos pueden mostrarse vacíos en admin pero el listado no fallará.",
        }),
        ("Estado", {
            "fields": ("is_used", "attempts", "max_attempts"),
        }),
        ("Fechas", {
            "classes": ("collapse",),
            "fields": ("created_at", "expires_at"),
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# Configuración del sitio admin
admin.site.site_header = "Administración de Usuarios"
admin.site.site_title = "Usuarios"
admin.site.index_title = "Panel de Administración"
