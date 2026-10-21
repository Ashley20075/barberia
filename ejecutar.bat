@echo off
echo === 1. Entrando a la carpeta del proyecto ===
cd /d "%~dp0autologic"

echo === 2. Creando entorno virtual (si no existe) ===
if not exist venv (
    python -m venv venv
)

echo === 3. Activando entorno e instalando librerias ===
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo === 4. Aplicando migraciones de base de datos ===
python manage.py makemigrations
python manage.py migrate

echo === 5. Iniciando servidor ===
python manage.py runserver