from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Tutor, Mascota, Veterinario, Cita, FichaMedica, Recordatorio, Secretario

@admin.register(Secretario)
class SecretarioAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('username', 'first_name', 'last_name', 'email')

    def save_model(self, request, obj, form, change):
        # Asegurar que el usuario esté activo
        obj.is_active = True
        super().save_model(request, obj, form, change)

        # Crear o asignar el grupo 'Secretaria' con permisos estándar
        grupo_secretaria, _ = Group.objects.get_or_create(name='Secretaria')
        obj.groups.add(grupo_secretaria)

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'rut', 'nombre', 'apellido', 'telefono', 'email')
    search_fields = ('nombre', 'rut')

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    # 'estado' pertenece al modelo Mascota
    list_display = ('id', 'nombre', 'especie', 'raza', 'tutor', 'estado')
    list_filter = ('estado', 'especie')
    search_fields = ('nombre', 'raza')


@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'especialidad', 'telefono')

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_hora', 'estado')
    list_filter = ('estado', 'fecha_hora')

@admin.register(FichaMedica)
class FichaMedicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'diagnostico')

@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'fecha_programada', 'estado_notificacion')
    list_filter = ('tipo', 'estado_notificacion')