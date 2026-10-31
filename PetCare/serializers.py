from rest_framework import serializers
from .models import Tutor, Mascota, Veterinario, Cita, FichaMedica, Recordatorio
from django.db import transaction

# 1. Definir primero MascotaSerializer para evitar el NameError
class MascotaSerializer(serializers.ModelSerializer):
    tutor_nombre = serializers.ReadOnlyField(source='tutor.__str__')

    class Meta:
        model = Mascota
        fields = '__all__'


# 2. TutorSerializer con soporte anidado opcional
class TutorSerializer(serializers.ModelSerializer):
    mascotas = MascotaSerializer(many=True, required=False)

    class Meta:
        model = Tutor
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        mascotas_data = validated_data.pop('mascotas', [])
        tutor = Tutor.objects.create(**validated_data)
        for m_data in mascotas_data:
            Mascota.objects.create(tutor=tutor, **m_data)
        return tutor


class VeterinarioSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField(source='user.get_full_name')

    class Meta:
        model = Veterinario
        fields = '__all__'


class CitaSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.ReadOnlyField(source='mascota.nombre')
    veterinario_nombre = serializers.ReadOnlyField(source='veterinario.__str__')

    class Meta:
        model = Cita
        fields = '__all__'


class FichaMedicaSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.ReadOnlyField(source='mascota.nombre')

    class Meta:
        model = FichaMedica
        fields = '__all__'


class RecordatorioSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.ReadOnlyField(source='mascota.nombre')

    class Meta:
        model = Recordatorio
        fields = '__all__'