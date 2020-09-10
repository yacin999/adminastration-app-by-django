from django.contrib import admin
from .models import StaffPermission, Staff

# Register your models here.


class StaffPermissionAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['pk' ,'name']
    search_fields = ['name']



class StaffAdmin(admin.ModelAdmin):
    list_filter = ['user', 'permissions']
    list_display = ['user']
    search_fields = ['user', 'permissions']


admin.site.register(StaffPermission, StaffPermissionAdmin)
admin.site.register(Staff, StaffAdmin)
