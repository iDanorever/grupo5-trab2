from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models.user_verification_code import UserVerificationCode

User = get_user_model()


# Configuración personalizada para el modelo User
class CustomUserAdmin(BaseUserAdmin):
    """Administración personalizada para el modelo User"""
    
    list_display = [
        'user_name', 'name', 'paternal_lastname', 'maternal_lastname',
        'email', 'account_statement', 'is_active', 'date_joined'
    ]
    
    list_filter = [
        'account_statement', 'is_active', 'is_staff', 'is_superuser',
        'date_joined', 'last_login', 'deleted_at'
    ]
    
    search_fields = [
        'user_name', 'email', 'name', 'paternal_lastname', 'maternal_lastname',
        'document_number'
    ]
    
    ordering = ['-date_joined']
    
    fieldsets = (
        ('Información de Cuenta', {
            'fields': ('user_name', 'password', 'account_statement')
        }),
        ('Información Personal', {
            'fields': (
                'name', 'paternal_lastname', 'maternal_lastname',
                'sex', 'email', 'phone', 'photo_url'
            )
        }),
        ('Información de Documento', {
            'fields': ('document_number', 'document_type', 'country')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_name', 'name', 'paternal_lastname', 'maternal_lastname', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined', 'deleted_at']


# Registrar el admin personalizado
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, CustomUserAdmin)


@admin.register(UserVerificationCode)
class UserVerificationCodeAdmin(admin.ModelAdmin):
    """Administración para el modelo UserVerificationCode"""
    
    list_display = [
        'user', 'verification_type', 'code', 'target_email',
        'is_used', 'failed_attempts', 'created_at', 'expires_at'
    ]
    
    list_filter = [
        'verification_type', 'is_used', 'created_at', 'expires_at'
    ]
    
    search_fields = ['user__user_name', 'user__email', 'code', 'target_email']
    
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('user', 'verification_type', 'code', 'target_email')
        }),
        ('Estado', {
            'fields': ('is_used', 'failed_attempts', 'max_attempts')
        }),
        ('Fechas', {
            'fields': ('created_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'expires_at']
    
    def get_queryset(self, request):
        """Optimiza las consultas del admin"""
        return super().get_queryset(request).select_related('user')
    
    def has_add_permission(self, request):
        """No permite crear códigos manualmente"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Solo permite ver, no editar"""
        return False


# Configuración del sitio admin
admin.site.site_header = "Administración de Usuarios"
admin.site.site_title = "Usuarios"
admin.site.index_title = "Panel de Administración"
