from rest_framework import serializers
from .models import Tutor, Mascota, Veterinario, Cita, FichaMedica, Recordatorio


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'


class MascotaSerializer(serializers.ModelSerializer):
    tutor_nombre = serializers.ReadOnlyField(source='tutor.__str__')

    class Meta:
        model = Mascota
        fields = '__all__'


class VeterinarioSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField(source='user.get_full_name')

    class Meta:
        model = Veterinario
        fields = '__all__'


class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'


class FichaMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaMedica
        fields = '__all__'


class RecordatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recordatorio
        fields = '__all__'