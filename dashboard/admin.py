from django.contrib import admin
from .models import Niveau, Module, Enseignant, Salle, Periode, EmploiTemps, CanvasTimeTable

# Register your models here.


class ModuleAdmin(admin.ModelAdmin):
    list_filter = ['designation']
    list_display = ['pk' ,'designation', 'code', 'coeff', 'credit']
    search_fields = ['designation', 'code']

class EnseignantAdmin(admin.ModelAdmin):
    list_filter = ['nom', 'prenom']
    list_display = ['pk', 'nom', 'prenom', 'grade', 'email']
    search_fields = ['nom', 'prenom']

class SalleAdmin(admin.ModelAdmin):
    list_filter = ['design', 'bloc']
    list_display = ['bloc', 'design', 'type']
    search_fields = ['design', 'bloc', 'type']

class EmploiTempsAdmin(admin.ModelAdmin):
    list_filter = ['slug']
    list_display = ['slug']
    search_fields = ['slug']

class CanvasAdmin(admin.ModelAdmin):
    list_filter = ['niveau']
    list_display = ['slug', 'semestre', 'modules', 'niveau', 'tp', 'td', 'cours']
    search_fields = ['niveau']


admin.site.register(Module, ModuleAdmin)
admin.site.register(Niveau)
admin.site.register(Enseignant, EnseignantAdmin)
admin.site.register(Salle, SalleAdmin)
admin.site.register(Periode)
admin.site.register(EmploiTemps, EmploiTempsAdmin)
admin.site.register(CanvasTimeTable, CanvasAdmin)








