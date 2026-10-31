from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


# Proxy Model para filtrar y gestionar Secretarios en Django Admin
class Secretario(User):
    class Meta:
        proxy = True
        verbose_name = 'Secretario(a)'
        verbose_name_plural = 'Secretarios(as)'


class Tutor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, default='')
    rut = models.CharField(max_length=12)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.CharField(max_length=200, blank=True, default='Sin Registrar')

    def __str__(self):
        return f"{self.nombre} (RUT: {self.rut})"


class Mascota(models.Model):
    ESPECIES = [
        ('PERRO', 'Perro'),
        ('GATO', 'Gato'),
        ('OTRO', 'Otro'),
    ]
    ESTADOS = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]
    SEXOS = [
        ('MACHO', 'Macho'),
        ('HEMBRA', 'Hembra'),
    ]

    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=10, choices=ESPECIES, default='PERRO')
    raza = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(default=1)
    peso = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    sexo = models.CharField(max_length=10, choices=SEXOS, default='MACHO')
    estado = models.CharField(max_length=10, choices=ESTADOS, default='ACTIVO')

    def __str__(self):
        return f"{self.nombre} ({self.tutor.nombre})"


class Veterinario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100, blank=True, null=True) # En caso de no vincular a User
    especialidad = models.CharField(max_length=100, default='General')
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        # 1. Si tiene el campo nombre directo lleno (Ej: Frambuesa)
        if self.nombre and self.nombre.strip():
            return f"Dr(a). {self.nombre} ({self.especialidad})"
        
        # 2. Si está vinculado a un usuario de Django con nombre/apellido
        if self.user and (self.user.first_name or self.user.last_name):
            nombre_completo = f"{self.user.first_name} {self.user.last_name}".strip()
            return f"Dr(a). {nombre_completo} ({self.especialidad})"
        
        # 3. Si sólo tiene username en User
        if self.user and self.user.username:
            return f"Dr(a). {self.user.username} ({self.especialidad})"

        # 4. Alternativa por defecto en caso de no tener nombre asignado
        return f"Dr(a). Veterinario #{self.id} ({self.especialidad})"

class Cita(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.CASCADE, related_name='citas')
    fecha_hora = models.DateTimeField()
    motivo = models.CharField(max_length=255, blank=True)
    estado = models.CharField(max_length=20, default='PENDIENTE')

    def __str__(self):
        return f"Cita: {self.mascota.nombre} con {self.veterinario} ({self.fecha_hora})"


class FichaMedica(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='fichas_medicas')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    receta_medica = models.TextField(blank=True, null=True)
    examenes = models.FileField(upload_to='examenes/', blank=True, null=True)

    def __str__(self):
        return f"Ficha {self.mascota.nombre} - {self.fecha.strftime('%d/%m/%Y')}"


class Recordatorio(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='recordatorios', null=True, blank=True)
    tipo = models.CharField(max_length=100)
    fecha_programada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50, default='PENDIENTE')

    def __str__(self):
        return f"Recordatorio: {self.tipo} - {self.mascota}"