@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

echo === 1. Entrando a la carpeta del proyecto ===
cd autologic

echo === 2. Buscando Python instalado ===
set PYCMD=
where py >nul 2>nul && set PYCMD=py
if "%PYCMD%"=="" (
    where python >nul 2>nul && set PYCMD=python
)
if "%PYCMD%"=="" (
    echo.
    echo ERROR: No se encontro Python instalado o no esta agregado al PATH.
    echo Instala Python desde https://www.python.org/downloads/
    echo Durante la instalacion, marca la casilla "Add python.exe to PATH".
    echo.
    pause
    exit /b 1
)

echo Usando el comando: %PYCMD%

echo === 3. Creando entorno virtual (si no existe) ===
if not exist "venv\Scripts\python.exe" (
    %PYCMD% -m venv venv
)

if not exist "venv\Scripts\python.exe" (
    echo.
    echo ERROR: No se pudo crear el entorno virtual "venv" correctamente.
    echo.
    pause
    exit /b 1
)

echo === 4. Instalando librerias dentro del entorno virtual ===
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt

echo === 5. Aplicando migraciones de base de datos ===
venv\Scripts\python.exe manage.py makemigrations
venv\Scripts\python.exe manage.py migrate

echo === 6. Iniciando servidor ===
venv\Scripts\python.exe manage.py runserver

pause