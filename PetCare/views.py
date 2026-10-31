from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Tutor, Mascota, Veterinario, Cita, FichaMedica, Recordatorio
from .serializers import (
    TutorSerializer, MascotaSerializer, VeterinarioSerializer,
    CitaSerializer, FichaMedicaSerializer, RecordatorioSerializer
)


# --- VISTAS TEMPLATES HTML ---

def index(request):
    if request.method == 'POST':
        user_input = request.POST.get('username')
        pass_input = request.POST.get('password')
        user = authenticate(request, username=user_input, password=pass_input)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'petcare/index.html', {'error': 'Credenciales inválidas'})

    mascotas = Mascota.objects.select_related('tutor').all()
    veterinarios = Veterinario.objects.select_related('user').all()
    tutores = Tutor.objects.prefetch_related('mascotas').all()

    return render(request, 'petcare/index.html', {
        'mascotas': mascotas,
        'veterinarios': veterinarios,
        'tutores': tutores
    })
    
    return render(request, 'petcare/index.html')


def login_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('username')
        pass_input = request.POST.get('password')
        user = authenticate(request, username=user_input, password=pass_input)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'petcare/login.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'petcare/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'petcare/dashboard.html')


@login_required(login_url='login')
def tutores_mascotas_view(request):
    # Carga todos los tutores con sus mascotas para la plantilla HTML
    tutores = Tutor.objects.prefetch_related('mascotas').all()
    return render(request, 'petcare/tutores_mascotas.html', {'tutores': tutores})


@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_tutor_mascotas_api(request):
    data = request.data
    try:
        with transaction.atomic():
            # 1. Guardar en la base de datos PostgreSQL
            tutor = Tutor.objects.create(
                nombre=data.get('nombre', ''),
                rut=data.get('rut', ''),
                email=data.get('email', ''),
                telefono=data.get('telefono', '')
            )

            mapa_especies = {'PERRO': 'PERRO', 'GATO': 'GATO', 'OTRO': 'OTRO'}
            mascotas_data = data.get('mascotas', [])
            mascotas_creadas = []

            for m in mascotas_data:
                esp_raw = str(m.get('especie', '')).upper()
                esp_val = mapa_especies.get(esp_raw, 'OTRO')

                mascota = Mascota.objects.create(
                    tutor=tutor,
                    nombre=m.get('nombre', ''),
                    especie=esp_val,
                    raza=m.get('raza', 'Mestizo')
                )
                mascotas_creadas.append({
                    'nombre': mascota.nombre,
                    'especie': mascota.get_especie_display(),
                    'raza': mascota.raza
                })

            # 2. Devolver la estructura completa en la respuesta
            return Response({
                'message': 'Guardado correctamente',
                'tutor': {
                    'nombre': tutor.nombre,
                    'rut': tutor.rut,
                    'email': tutor.email,
                    'telefono': tutor.telefono,
                    'mascotas': mascotas_creadas
                }
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def editar_tutor_api(request, pk):
    try:
        tutor = Tutor.objects.get(pk=pk)
        tutor.nombre = request.data.get('nombre', tutor.nombre)
        tutor.rut = request.data.get('rut', tutor.rut)
        tutor.email = request.data.get('email', tutor.email)
        tutor.telefono = request.data.get('telefono', tutor.telefono)
        tutor.save()
        return Response({'message': 'Tutor actualizado con éxito'})
    except Tutor.DoesNotExist:
        return Response({'error': 'Tutor no encontrado'}, status=404)

@login_required(login_url='login')
def calendario_view(request):
    mascotas = Mascota.objects.select_related('tutor').all()
    veterinarios = Veterinario.objects.select_related('user').all()
    citas = Cita.objects.select_related('mascota', 'veterinario', 'mascota__tutor').all()
    
    return render(request, 'petcare/calendario.html', {
        'mascotas': mascotas,
        'veterinarios': veterinarios,
        'citas': citas
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def agendar_cita_api(request):
    data = request.data
    try:
        with transaction.atomic():
            veterinario = Veterinario.objects.get(id=data.get('veterinario_id'))

            if data.get('tipo_paciente') == 'NUEVO':
                # Crear Tutor y Mascota para el paciente nuevo
                t_data = data.get('tutor', {})
                tutor = Tutor.objects.create(
                    nombre=t_data.get('nombre'),
                    rut=t_data.get('rut'),
                    telefono=t_data.get('telefono'),
                    email=t_data.get('email')
                )
                m_data = data.get('mascota', {})
                mascota = Mascota.objects.create(
                    tutor=tutor,
                    nombre=m_data.get('nombre'),
                    especie=m_data.get('especie', 'PERRO'),
                    raza=m_data.get('raza', 'Mestizo')
                )
            else:
                # Obtener mascota existente
                mascota = Mascota.objects.get(id=data.get('mascota_id'))

            # Crear la Cita Médica
            cita = Cita.objects.create(
                mascota=mascota,
                veterinario=veterinario,
                fecha_hora=data.get('fecha_hora'),
                motivo=data.get('motivo', 'Consulta general'),
                estado='CONFIRMADA'
            )

            return Response({'message': 'Cita agendada correctamente'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='login')
def fichas_medicas(request):
    return render(request, 'petcare/fichas_medicas.html')


@login_required(login_url='login')
def recordatorios(request):
    return render(request, 'petcare/recordatorios.html')


# --- API VIEWSETS (DRF) ---

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer

    # Sobrescribimos create para reusar tutores existentes por RUT
    def create(self, request, *args, **kwargs):
        rut = request.data.get('rut')
        
        if rut:
            tutor_existente = Tutor.objects.filter(rut=rut).first()
            if tutor_existente:
                serializer = self.get_serializer(tutor_existente)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
        return super().create(request, *args, **kwargs)


class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer


class VeterinarioViewSet(viewsets.ModelViewSet):
    queryset = Veterinario.objects.all()
    serializer_class = VeterinarioSerializer


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer


class FichaMedicaViewSet(viewsets.ModelViewSet):
    queryset = FichaMedica.objects.all()
    serializer_class = FichaMedicaSerializer


class RecordatorioViewSet(viewsets.ModelViewSet):
    queryset = Recordatorio.objects.all()
    serializer_class = RecordatorioSerializer