from django.contrib import admin
from .models import Tutor, Mascota, Veterinario, Cita, FichaMedica, Recordatorio


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido', 'telefono', 'email')
    search_fields = ('nombre', 'apellido', 'rut')


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'tutor', 'edad')
    list_filter = ('especie', 'sexo')
    search_fields = ('nombre', 'tutor__nombre', 'tutor__apellido')


@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'especialidad', 'telefono')


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'veterinario', 'fecha_hora', 'estado')
    list_filter = ('estado', 'fecha_hora', 'veterinario')
    search_fields = ('mascota__nombre', 'veterinario__user__first_name')


@admin.register(FichaMedica)
class FichaMedicaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'veterinario', 'fecha')
    search_fields = ('mascota__nombre', 'diagnostico')


@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'tipo', 'fecha_programada', 'completado')
    list_filter = ('tipo', 'completado')