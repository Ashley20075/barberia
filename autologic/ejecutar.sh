#!/bin/bash
echo "=== 1. Creando entorno virtual (si no existe) ==="
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

echo "=== 2. Activando entorno e instalando librerias ==="
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "=== 3. Aplicando migraciones de base de datos ==="
python3 manage.py makemigrations
python3 manage.py migrate

echo "=== 4. Iniciando servidor ==="
python3 manage.py runserver