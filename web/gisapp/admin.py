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


class ServiceTypeAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name',)
    search_fields = ('name',)


class EquipmentTypeAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name',)
    search_fields = ('name',)


class EquipmentHospitalAdmin(admin.ModelAdmin):
    list_filter = ('equipment', 'hospital')
    list_display = ('equipment', 'hospital', 'quantity')
    search_fields = ()


class FundingSourceAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name',)
    search_fields = ('name',)


class FundingAdmin(admin.ModelAdmin):
    list_filter = ('funding_source', 'hospital')
    list_display = ('funding_source', 'hospital', 'amount')
    search_fields = ()


class ExpensesPurposeAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name',)
    search_fields = ('name',)


class ExpenseAdmin(admin.ModelAdmin):
    list_filter = ('expenses_purpose', 'hospital')
    list_display = ('expenses_purpose', 'hospital', 'amount')
    search_fields = ()


class MKBClassAdmin(admin.ModelAdmin):
    list_filter = ('level', 'parent')
    list_display = ('name', 'code', 'level', 'parent')
    search_fields = ('name', 'code')


class PatientStayAdmin(admin.ModelAdmin):
    list_filter = ('hospital', 'sex', 'citizenship', 'ethnicity', 'mkb', 'surgery', 'is_planned', 'is_urgent', 'stay_result', 'treatment_result')
    list_display = ('rpnID', 'hospital', 'age', 'sex', 'mkb', 'mkb_complication', 'days_spent', 'stay_result', 'treatment_result')
    search_fields = ('rpnID', )


class CitizenshipAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name',)
    search_fields = ('name',)


class EthnicityAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name',)
    search_fields = ('name',)


class SurgeryTypeAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


class StayProfileAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('name', )
    search_fields = ('name', )


admin.site.register(Region, RegionAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Town, TownAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(EquipmentType, EquipmentTypeAdmin)
admin.site.register(EquipmentHospital, EquipmentHospitalAdmin)
admin.site.register(FundingSource, FundingSourceAdmin)
admin.site.register(Funding, FundingAdmin)
admin.site.register(ExpensesPurpose, ExpensesPurposeAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(MKBClass, MKBClassAdmin)
admin.site.register(PatientStay, PatientStayAdmin)
admin.site.register(Citizenship, CitizenshipAdmin)
admin.site.register(Ethnicity, EthnicityAdmin)
admin.site.register(SurgeryType, SurgeryTypeAdmin)
admin.site.register(StayProfile, StayProfileAdmin)
