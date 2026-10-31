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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100, default='Medicina General')
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"Dr(a). {self.user.first_name} {self.user.last_name}"


class Cita(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('REALIZADA', 'Realizada'),
    ]
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    veterinario = models.ForeignKey(Veterinario, on_delete=models.CASCADE, related_name='citas')
    fecha_hora = models.DateTimeField()
    motivo = models.TextField(default='Consulta general')
    estado = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE')

    def __str__(self):
        return f"Cita #{self.id} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"


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
    mascota_nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    fecha_programada = models.DateField()
    estado_notificacion = models.CharField(max_length=50, default='Programado (WhatsApp/Correo)')

    def __str__(self):
        return f"Recordatorio {self.mascota_nombre} - {self.tipo} ({self.fecha_programada})"