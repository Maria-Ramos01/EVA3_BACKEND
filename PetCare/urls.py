from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'tutores', views.TutorViewSet)
router.register(r'mascotas', views.MascotaViewSet)
router.register(r'veterinarios', views.VeterinarioViewSet)
router.register(r'citas', views.CitaViewSet)
router.register(r'fichas', views.FichaMedicaViewSet)
router.register(r'recordatorios', views.RecordatorioViewSet)

urlpatterns = [
    # Endpoints de Autenticación JWT
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),

    # Rutas Web (HTML) y API
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Ruta Web -> Devuelve la plantilla HTML
    path('tutor-mascotas/', views.tutores_mascotas_view, name='tutores_mascotas'),
    path('api/tutores/<int:pk>/', views.editar_tutor_api, name='editar_tutor_api'),
    path('api/agendar-cita/', views.agendar_cita_api, name='agendar_cita_api'),
    path('api/citas/<int:pk>/estado/', views.cambiar_estado_cita_api, name='cambiar_estado_cita_api'),
    # Ruta API -> Procesa los datos enviados por la petición AJAX / fetch
    path('api/registrar-tutor-mascotas/', views.registrar_tutor_mascotas_api, name='api_registrar_tutor_mascotas'),
    path('fichas-medicas/', views.fichas_medicas, name='fichas_medicas'),
    path('api/recordatorios/', views.crear_recordatorio_api, name='crear_recordatorio_api'),
    path('api/', include(router.urls)),
]
