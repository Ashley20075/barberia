Documentación del proyecto
https://docs.google.com/document/d/1ytgUJAQ0TiwKj8696dOookmV89ZgS-Jd/edit?usp=drive_link&ouid=106568756738730459176&rtpof=true&sd=true

Comandos habituales (desde `autologic`):
- Crear administrador: `python manage.py createsuperuser`
- Aplicar migraciones: `python manage.py migrate`
- Enviar recordatorios: `python manage.py enviar_recordatorios`
- Iniciar el servidor: `python manage.py runserver`

En Windows, abre `ejecutar.bat`. En macOS o Linux, desde la carpeta principal ejecuta `chmod +x ejecutar.sh` una sola vez y después `./ejecutar.sh`. Los dos scripts instalan las dependencias, aplican las migraciones e inician el servidor.

Esta actualización incluye los ajustes de AutoAI en plata, mejoras para móviles y tabletas, correcciones de modales y una edición más sencilla de los días laborales y de descanso de los barberos.

Para instalarlo manualmente, entra en `autologic`, crea un entorno virtual, instala `requirements.txt` y ejecuta `python manage.py migrate`. Copia `.env.example` como `.env` y completa las claves que uses (Google, Gemini, correo y Django). Conserva tu `.env`, tu base de datos y tus archivos privados; no los reemplaces con archivos de ejemplo. Para uso local, el proyecto arranca con la configuración predeterminada. Las integraciones de Google, Gemini y correo necesitan sus propias credenciales en `.env`; en producción debes usar una clave secreta propia y `DJANGO_DEBUG=False`.
