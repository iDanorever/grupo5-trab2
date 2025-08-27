from django.contrib import admin
from therapists.models import Therapist

@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ("id","first_name","last_name_paternal","document_number","region_fk","province_fk","district_fk","is_active")
    list_filter = ("is_active","region_fk","province_fk","district_fk")
    search_fields = ("first_name","last_name_paternal","last_name_maternal","document_number")
