Secretarios:

- Fer
holachao123

Para guardar y aplicar los cambios realizados en el código dentro de tu instancia de **AWS EC2**, debes ejecutar una serie de comandos en la consola terminal de tu servidor (conectada vía SSH o Session Manager).

A continuación tienes la secuencia ordenada de pasos a ejecutar:

---

### Pasos para Guardar y Aplicar Cambios en EC2

1. **Acceder a la carpeta del proyecto**
```bash
cd ~/EVA3_BACKEND

```


*(Asegúrate de colocar la ruta exacta donde clonaste o ubicaste tu repositorio en el servidor EC2).*
2. **Activar el entorno virtual de Python**
```bash
source env/bin/activate

```


3. **Traer los últimos cambios (Si subiste el código a Git)**
```bash
git pull origin main

```


*(Si modificaste los archivos directamente en el servidor usando `nano` o `vim`, puedes saltarte este paso).*
4. **Aplicar migraciones de la base de datos (Si agregaste o modificaste modelos/campos)**
```bash
python manage.py makemigrations
python manage.py migrate

```


5. **Recolectar archivos estáticos (CSS, JS, imágenes)**
```bash
python manage.py collectstatic --noinput

```
