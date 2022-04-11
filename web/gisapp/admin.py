from django.contrib import admin

from django.contrib import admin

from .models import *


class RegionAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name', 'layer_name', 'lat', 'lon', 'zoom_level', )
    search_fields = ('name', 'layer_name', )


class DistrictAdmin(admin.ModelAdmin):
    list_filter = ('region', )
    list_display = ('name', 'region', 'layer_name', 'lat', 'lon', 'zoom_level', )
    search_fields = ('name', 'layer_name', )


class TownAdmin(admin.ModelAdmin):
    list_filter = ('district', )
    list_display = ('name', 'district', 'layer_name', 'lat', 'lon', 'zoom_level', )
    search_fields = ('name', 'layer_name', )


class HospitalAdmin(admin.ModelAdmin):
    list_filter = ('town', )
    list_display = ('name', 'town', 'layer_name', 'lat', 'lon', 'zoom_level', )
    search_fields = ('name', 'layer_name', )


admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Town, TownAdmin)
admin.site.register(Hospital, HospitalAdmin)
