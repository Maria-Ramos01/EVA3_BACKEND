from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
import json
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Tutor, Mascota, Veterinario, Cita, FichaMedica, Recordatorio
from .serializers import (
    TutorSerializer, MascotaSerializer, VeterinarioSerializer,
    CitaSerializer, FichaMedicaSerializer, RecordatorioSerializer
)

def es_admin(user):
    return user.is_staff or user.is_superuser

# --- VISTAS TEMPLATES HTML ---
@login_required(login_url='login')
def index(request):
    mascotas_activas = Mascota.objects.filter(estado__iexact='ACTIVO')
    veterinarios = Veterinario.objects.all()
    citas = Cita.objects.select_related('mascota', 'veterinario', 'mascota__tutor').all().order_by('-fecha_hora')
    recordatorios = Recordatorio.objects.select_related('mascota').all().order_by('-id')

    return render(request, 'petcare/index.html', {
        'mascotas': mascotas_activas,
        'veterinarios': veterinarios,
        'citas': citas,
        'recordatorios': recordatorios
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username_req = request.POST.get('username')
        password_req = request.POST.get('password')
        user = authenticate(request, username=username_req, password=password_req)
        
        if user.is_active:  # Verificar que esté activo
                login(request, user)
                return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'petcare/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'petcare/dashboard.html')


@login_required(login_url='login')
def tutores_mascotas(request, tutor_id=None):
    tutor_obj = Tutor.objects.prefetch_related('mascotas').filter(id=tutor_id).first() if tutor_id else None

    if request.method == 'POST':
        nombre_tutor = request.POST.get('nombre_tutor')
        rut = request.POST.get('rut')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')

        if tutor_obj:
            tutor_obj.nombre = nombre_tutor
            tutor_obj.rut = rut
            tutor_obj.email = email
            tutor_obj.telefono = telefono
            tutor_obj.save()
            mensaje = "Tutor y mascotas actualizados correctamente."
        else:
            tutor_obj = Tutor.objects.create(
                nombre=nombre_tutor, rut=rut, email=email, telefono=telefono
            )
            mensaje = "Tutor y mascotas registrados correctamente."

        mascota_ids = request.POST.getlist('mascota_id[]')
        nombres_mascota = request.POST.getlist('nombre_mascota[]')
        especies = request.POST.getlist('especie[]')
        razas = request.POST.getlist('raza[]')
        estados = request.POST.getlist('estado_val[]')

        for i in range(len(nombres_mascota)):
            if nombres_mascota[i].strip():
                m_id = mascota_ids[i] if i < len(mascota_ids) and mascota_ids[i] else None
                val_recibido = estados[i] if i < len(estados) else 'ACTIVO'
                m_estado = 'ACTIVO' if str(val_recibido).upper() in ['ACTIVO', 'TRUE'] else 'INACTIVO'    
                            
                if m_id:
                    mascota = Mascota.objects.filter(id=m_id, tutor=tutor_obj).first()
                    if mascota:
                        mascota.nombre = nombres_mascota[i]
                        mascota.especie = especies[i]
                        mascota.raza = razas[i]
                        mascota.estado = m_estado
                        mascota.save()
                else:
                    Mascota.objects.create(
                        tutor=tutor_obj,
                        nombre=nombres_mascota[i],
                        especie=especies[i],
                        raza=razas[i],
                        estado=m_estado
                    )

        messages.success(request, mensaje)
        return redirect('tutores_mascotas')

    tutores = Tutor.objects.prefetch_related('mascotas').all().order_by('-id')
    
    return render(request, 'petcare/tutores_mascotas.html', {
        'tutores': tutores,
        'tutor_editar': tutor_obj
    })
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

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import transaction

@api_view(['POST'])
@permission_classes([AllowAny])
def agendar_cita_api(request):
    data = request.data
    try:
        with transaction.atomic():
            veterinario = Veterinario.objects.get(id=data.get('veterinario_id'))
            fecha_hora = data.get('fecha_hora')
            motivo = data.get('motivo', 'Consulta Médica')

            # 1. Validar solapamiento ANTES de crear la cita (Usando 'veterinario' y 'fecha_hora')
            existe_solapamiento = Cita.objects.filter(
                veterinario=veterinario,
                fecha_hora=fecha_hora
            ).exclude(estado='CANCELADA').exists()

            if existe_solapamiento:
                return Response(
                    {'error': 'La hora seleccionada ya fue reservada por otro paciente.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Obtener o crear Mascota
            if data.get('tipo_paciente') == 'NUEVO':
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
                mascota = Mascota.objects.get(id=data.get('mascota_id'))

            # 3. Crear Cita
            cita = Cita.objects.create(
                mascota=mascota,
                veterinario=veterinario,
                fecha_hora=fecha_hora,
                motivo=motivo,
                estado='PENDIENTE'
            )

            # 4. Crear Recordatorio
            recordatorio_kwargs = {}
            if hasattr(Recordatorio, 'paciente'):
                recordatorio_kwargs['paciente'] = mascota
            elif hasattr(Recordatorio, 'mascota'):
                recordatorio_kwargs['mascota'] = mascota

            if hasattr(Recordatorio, 'tipo'):
                recordatorio_kwargs['tipo'] = f"Cita con {veterinario} - {motivo}"

            if hasattr(Recordatorio, 'fecha_programada'):
                recordatorio_kwargs['fecha_programada'] = fecha_hora
            elif hasattr(Recordatorio, 'fecha'):
                recordatorio_kwargs['fecha'] = fecha_hora

            if hasattr(Recordatorio, 'estado_notificacion'):
                recordatorio_kwargs['estado_notificacion'] = 'Programado'
            elif hasattr(Recordatorio, 'estado'):
                recordatorio_kwargs['estado'] = 'PENDIENTE'

            Recordatorio.objects.create(**recordatorio_kwargs)

            return Response({'message': 'Cita y recordatorio agendados con éxito'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def cambiar_estado_cita_api(request, pk):
    try:
        cita = Cita.objects.get(pk=pk)
        nuevo_estado = request.data.get('estado')
        if nuevo_estado in ['PENDIENTE', 'CONFIRMADA', 'CANCELADA']:
            cita.estado = nuevo_estado
            cita.save()
            return Response({'message': f'Estado actualizado a {nuevo_estado}'}, status=status.HTTP_200_OK)
        return Response({'error': 'Estado no válido'}, status=status.HTTP_400_BAD_REQUEST)
    except Cita.DoesNotExist:
        return Response({'error': 'Cita no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    

@login_required
def fichas_medicas(request):
    fichas = FichaMedica.objects.all().select_related('mascota', 'mascota__tutor').order_by('-fecha_creacion')
    
    return render(request, 'petcare/fichas_medicas.html', {'fichas': fichas})

@login_required(login_url='login')
@csrf_exempt
def crear_recordatorio_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mascota_id = data.get('mascota_id')
            tipo = data.get('tipo')
            fecha = data.get('fecha')

            if not mascota_id or not fecha:
                return JsonResponse({'status': 'error', 'message': 'Faltan campos obligatorios (Mascota o Fecha)'}, status=400)

            mascota = Mascota.objects.get(id=mascota_id)
            
            # Crear recordatorio con los campos mínimos requeridos
            recordatorio = Recordatorio.objects.create(
                mascota=mascota,
                tipo=tipo,
                fecha_programada=fecha
            )

            # Si el modelo incluye algún campo para el estado de notificación, lo asignamos de forma segura
            estado_texto = "PENDIENTE"
            if hasattr(recordatorio, 'estado_notificacion'):
                recordatorio.estado_notificacion = "PENDIENTE"
                recordatorio.save()
                estado_texto = recordatorio.estado_notificacion
            elif hasattr(recordatorio, 'estado'):
                recordatorio.estado = "PENDIENTE"
                recordatorio.save()
                estado_texto = recordatorio.estado

            return JsonResponse({
                'status': 'success',
                'recordatorio': {
                    'id': recordatorio.id,
                    'mascota_nombre': mascota.nombre,
                    'tipo': recordatorio.tipo,
                    'fecha': str(recordatorio.fecha_programada),
                    'estado': estado_texto
                }
            })
        except Mascota.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'La mascota seleccionada no existe'}, status=404)
        except Exception as e:
            # Devuelve el mensaje exacto de error en lugar de la alerta genérica
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def eliminar_recordatorio_api(request, rec_id):
    if request.method in ['DELETE', 'POST']:
        try:
            recordatorio = Recordatorio.objects.get(id=rec_id)
            recordatorio.delete()
            return JsonResponse({'status': 'success'})
        except Recordatorio.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'El recordatorio no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def editar_recordatorio_api(request, rec_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            recordatorio = Recordatorio.objects.get(id=rec_id)
            
            if 'tipo' in data:
                recordatorio.tipo = data['tipo']
            if 'fecha' in data:
                recordatorio.fecha_programada = data['fecha']
                
            recordatorio.save()
            return JsonResponse({
                'status': 'success',
                'recordatorio': {
                    'id': recordatorio.id,
                    'tipo': recordatorio.tipo,
                    'fecha': str(recordatorio.fecha_programada)
                }
            })
        except Recordatorio.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Recordatorio no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_disponibilidad_veterinario(request, vet_id):
    try:
        vet = Veterinario.objects.get(id=vet_id, activo=True)
        return Response({
            'hora_inicio': vet.hora_inicio.strftime('%H:%M'),
            'hora_fin': vet.hora_fin.strftime('%H:%M'),
            'dias_permitidos': [int(d) for d in vet.dias_atencion.split(',') if d.isdigit()]
        })
    except Veterinario.DoesNotExist:
        return Response({'error': 'Veterinario no disponible'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_horas_ocupadas(request):
    vet_id = request.GET.get('vet_id')
    fecha_str = request.GET.get('fecha')  # Formato YYYY-MM-DD

    if not vet_id or not fecha_str:
        return Response({'error': 'Faltan parámetros'}, status=400)

    try:
        vet = Veterinario.objects.get(id=vet_id)
        
        # Obtener horas de citas activas/confirmadas para ese vet en esa fecha
        citas = Cita.objects.filter(
            veterinario_id=vet_id,
            fecha_hora__date=fecha_str
        ).exclude(estado='Cancelada')

        # Extraer las horas ocupadas (ejemplo: ["14:30", "15:00"])
        horas_ocupadas = [cita.fecha_hora.strftime('%H:%M') for cita in citas]

        return Response({
            'hora_inicio': vet.hora_inicio.strftime('%H:%M'),
            'hora_fin': vet.hora_fin.strftime('%H:%M'),
            'dias_permitidos': [int(d) for d in vet.dias_atencion.split(',') if d.isdigit()],
            'horas_ocupadas': horas_ocupadas
        })
    except Veterinario.DoesNotExist:
        return Response({'error': 'Veterinario no encontrado'}, status=404)

@login_required(login_url='login')
def lista_veterinarios(request):
    veterinarios = Veterinario.objects.all()
    return render(request, 'petcare/veterinarios.html', {
        'veterinarios': veterinarios
    })

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