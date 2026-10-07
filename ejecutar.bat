@echo off
echo === 1. Entrando a la carpeta del proyecto ===
cd autologic

echo === 2. Creando entorno virtual (si no existe) ===
if not exist venv (
    py -m venv venv
)

echo === 3. Activando entorno e instalando librerias ===
call venv\Scripts\activate.bat
py -m pip install --upgrade pip
pip install -r requirements.txt

echo === 4. Aplicando migraciones de base de datos ===
py manage.py makemigrations
py manage.py migrate

echo === 5. Iniciando servidor ===
py manage.py runserver