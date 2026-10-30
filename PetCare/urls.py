from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tutores', views.TutorViewSet)
router.register(r'mascotas', views.MascotaViewSet)
router.register(r'veterinarios', views.VeterinarioViewSet)
router.register(r'citas', views.CitaViewSet)
router.register(r'fichas', views.FichaMedicaViewSet)
router.register(r'recordatorios', views.RecordatorioViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('tutores-mascotas/', views.tutores_mascotas, name='tutores_mascotas'),
    path('calendario/', views.calendario, name='calendario'),
    path('fichas-medicas/', views.fichas_medicas, name='fichas_medicas'),
    path('recordatorios/', views.recordatorios, name='recordatorios'),
    path('api/', include(router.urls)),
]
