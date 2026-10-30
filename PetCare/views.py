from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Tutor, Mascota, Veterinario, Cita, FichaMedica, Recordatorio
from .serializers import (
    TutorSerializer, MascotaSerializer, VeterinarioSerializer,
    CitaSerializer, FichaMedicaSerializer, RecordatorioSerializer
)

# --- VISTAS TEMPLATES HTML ---

def index(request):
    return render(request, 'petcare/index.html')

def login_view(request):
    return render(request, 'petcare/login.html')

def tutores_mascotas(request):
    return render(request, 'petcare/tutores_mascotas.html')

def calendario(request):
    return render(request, 'petcare/calendario.html')

def fichas_medicas(request):
    return render(request, 'petcare/fichas_medicas.html')

def recordatorios(request):
    return render(request, 'petcare/recordatorios.html')


# --- API VIEWSETS (DRF) ---

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer


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