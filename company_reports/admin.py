from django.contrib import admin
from company_reports.models.company import CompanyData

@admin.register(CompanyData)
class CompanyDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'company_logo', 'created_at', 'updated_at')
    search_fields = ('company_name',)
    ordering = ('company_name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información de la Empresa', {
            'fields': ('company_name', 'company_logo')
        }),
        ('Información del Sistema', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

