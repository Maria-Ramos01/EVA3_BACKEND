from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Tutor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Mascota(models.Model):
    ESPECIES = [
        ('CANINO', 'Canino'),
        ('FELINO', 'Felino'),
        ('EXOTICO', 'Exótico'),
    ]
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=10, choices=ESPECIES)
    raza = models.CharField(max_length=100)
    edad = models.PositiveIntegerField(help_text="Edad en años")
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso en kg")
    sexo = models.CharField(max_length=10, choices=[('MACHO', 'Macho'), ('HEMBRA', 'Hembra')])

    def __str__(self):
        return f"{self.nombre} ({self.tutor.nombre} {self.tutor.apellido})"


class Veterinario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=100, default='Medicina General')
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"Dr(a). {self.user.first_name} {self.user.last_name} - {self.especialidad}"


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
    motivo = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default='PENDIENTE')

    def clean(self):
        # Validación de solapamiento de horas por veterinario
        if self.fecha_hora:
            inicio_cita = self.fecha_hora
            fin_cita = self.fecha_hora + timezone.timedelta(minutes=30)
            
            citas_traslapadas = Cita.objects.filter(
                veterinario=self.veterinario,
                fecha_hora__gte=inicio_cita,
                fecha_hora__lt=fin_cita
            ).exclude(id=self.id)

            if citas_traslapadas.exists():
                raise ValidationError("El profesional ya tiene una cita agendada en ese horario.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cita {self.mascota.nombre} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"


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
    TIPOS = [
        ('VACUNA', 'Vacunación'),
        ('CONTROL', 'Control Periódico'),
        ('DESPARASITACION', 'Desparasitación'),
    ]
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='recordatorios')
    tipo = models.CharField(max_length=15, choices=TIPOS)
    fecha_programada = models.DateField()
    descripcion = models.CharField(max_length=200)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.mascota.nombre} ({self.fecha_programada})"