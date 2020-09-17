from django.contrib import admin
from .models import Niveau, Module, Enseignant, Salle, Periode, EmploiTemps, Material, Order, ChargeHoraire, Science

# Register your models here.


class ModuleAdmin(admin.ModelAdmin):
    list_filter = ['designation']
    list_display = ['pk' ,'designation', 'code', 'coeff', 'credit', 'semestre', 'cours', 'tp', 'td']
    search_fields = ['designation', 'code']

class EnseignantAdmin(admin.ModelAdmin):
    list_filter = ['nom', 'prenom']
    list_display = ['pk', 'nom', 'prenom', 'grade', 'email']
    search_fields = ['nom', 'prenom']

class SalleAdmin(admin.ModelAdmin):
    list_filter = ['design', 'bloc']
    list_display = ['bloc', 'design', 'type_of', 'is_available']
    search_fields = ['design', 'bloc', 'type_of']

class EmploiTempsAdmin(admin.ModelAdmin):
    list_filter = ['slug']
    list_display = ['slug']
    search_fields = ['slug']


class PeriodeAdmin(admin.ModelAdmin):
    list_display = ['module', 'enseignant', 'salle', 'groupe', 'groupe_type', 'peride_one', 'perides_two', 'perides_three', 'perides_twelve']
    search_fields = ['id']




class MaterialAdmin(admin.ModelAdmin):
    list_filter = ['name', 'is_available']
    list_display = ['id', 'name', 'is_available']
    search_fields = ['name', 'is_available']

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['item']
    list_display = ['id', 'item']
    search_fields = ['item']


class ChargeHoraireAdmin(admin.ModelAdmin):
    list_filter = ['semestre']
    list_display = ['id', 'semestre']
    search_fields = ['semestre']


class ScienceAdmin(admin.ModelAdmin):
    list_filter = ['nature']
    list_display = ['id', 'nature', 'groupe', 'occupe']
    search_fields = ['nature', 'groupe', 'occupe']



admin.site.register(Module, ModuleAdmin)
admin.site.register(Niveau)
admin.site.register(Enseignant, EnseignantAdmin)
admin.site.register(Salle, SalleAdmin)
admin.site.register(Periode, PeriodeAdmin)
admin.site.register(EmploiTemps, EmploiTempsAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ChargeHoraire, ChargeHoraireAdmin)
admin.site.register(Science, ScienceAdmin)







