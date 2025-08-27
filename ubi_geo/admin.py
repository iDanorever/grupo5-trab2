from django.contrib import admin
from ubi_geo.models import Region, Province, District

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id","ubigeo_code","name")
    search_fields = ("ubigeo_code","name")

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("id","ubigeo_code","name","region")
    list_filter = ("region",)
    search_fields = ("ubigeo_code","name","region__name")

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id","ubigeo_code","name","province")
    list_filter = ("province__region","province")
    search_fields = ("ubigeo_code","name","province__name","province__region__name")