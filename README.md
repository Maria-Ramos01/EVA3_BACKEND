# EVA3_BACKEND
Maria Fernanda Ramos - 02.11.2026
# 🐾 PetCare Clinic - Sistema de Gestión Clínica Veterinaria

Sistema web desarrollado con **Django**, **Django REST Framework** y **PostgreSQL**, desplegado en una instancia de **AWS EC2**.

---

## 🌐 Acceso Público en Vivo

El sistema se encuentra desplegado y accesible públicamente en las siguientes direcciones:

* **Aplicación Principal:** [http://54.198.16.20:8000](http://54.198.16.20:8000)
* **Panel de Administración:** [http://54.198.16.20:8000/admin](http://54.198.16.20:8000/admin)

> **Nota sobre seguridad:** Al ingresar a través de la IP pública por protocolo HTTP (`http://`), el navegador mostrará una advertencia de "Conexión no segura". Esto es completamente normal en entornos de prueba. Haz clic en *Configuración avanzada* y luego en *Continuar al sitio*.

---

## 🛠️ Instrucciones de Ejecución en AWS EC2

Para iniciar o administrar el servidor manualmente desde la instancia remota:

### 1. Conexión SSH al servidor
Conéctate a la instancia desde la terminal de tu equipo local:
```bash
ssh -i "tu-clave.pem" ubuntu@54.198.16.20
