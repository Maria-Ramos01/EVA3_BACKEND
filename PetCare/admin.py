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
    list_display = ('nombre', 'especialidad', 'hora_inicio', 'hora_fin', 'activo')
    list_editable = ('hora_inicio', 'hora_fin', 'activo')
    search_fields = ('nombre', 'especialidad')
    list_filter = ('activo', 'especialidad')

    def obtener_nombre(self, obj):
        # 1. Si se ingresó un nombre directamente en el formulario
        if obj.nombre:
            return f"Dr(a). {obj.nombre}"
        # 2. Si hay un usuario vinculado con nombre o apellido
        elif obj.user and (obj.user.first_name or obj.user.last_name):
            return f"Dr(a). {obj.user.first_name} {obj.user.last_name}"
        # 3. Si no hay nombre ni datos en User, usa el username del User si existe
        elif obj.user:
            return f"Dr(a). {obj.user.username}"
        return f"Dr(a). Veterinario #{obj.id}"

    obtener_nombre.short_description = 'Nombre Profesional'

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_hora', 'estado')
    list_filter = ('estado', 'fecha_hora')

@admin.register(FichaMedica)
class FichaMedicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'mascota', 'diagnostico_corto', 'fecha_creacion', 'tiene_adjunto')
    list_filter = ('fecha_creacion', 'mascota')
    search_fields = ('mascota__nombre', 'diagnostico', 'tratamiento', 'receta')
    fields = ('mascota', 'diagnostico', 'tratamiento', 'receta', 'adjunto', 'fecha_creacion')
    readonly_fields = ('fecha_creacion',)  # La fecha se genera automáticamente

    def diagnostico_corto(self, obj):
        return obj.diagnostico[:50] + "..." if len(obj.diagnostico) > 50 else obj.diagnostico
    diagnostico_corto.short_description = "Diagnóstico"

    def tiene_adjunto(self, obj):
        return bool(obj.adjunto)
    tiene_adjunto.boolean = True
    tiene_adjunto.short_description = "Adjunto"

@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    # Cambia 'estado_notificacion' por 'estado'
    list_display = ('mascota', 'tipo', 'fecha_programada', 'estado')
    list_filter = ('tipo', 'estado')
    search_fields = ('mascota__nombre', 'tipo')