@echo off
setlocal EnableExtensions
title Barberia - Iniciando sistema
chcp 65001 >nul

REM === 1. Entrar a la carpeta del proyecto (soporta espacios en la ruta) ===
cd /d "%~dp0autologic" || (
    echo [ERROR] No se encontro la carpeta "autologic" junto a este archivo.
    goto :fin
)

REM === 2. Buscar Python (launcher "py" o "python") ===
echo === 1. Buscando Python instalado ===
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (
    where python >nul 2>nul && set "PY=python"
)
if not defined PY (
    echo.
    echo [ERROR] No se encontro Python instalado o no esta agregado al PATH.
    echo         Instala Python 3.12 o superior desde https://www.python.org/downloads/
    echo         y marca la casilla "Add python.exe to PATH" durante la instalacion.
    goto :fin
)
echo Usando: %PY%

REM === 3. Entorno virtual: usa "venv" o ".venv" si ya existe, si no crea "venv" ===
echo === 2. Preparando entorno virtual ===
set "VENV=venv"
if exist ".venv\Scripts\python.exe" set "VENV=.venv"

if not exist "%VENV%\Scripts\python.exe" (
    echo Creando entorno virtual "%VENV%"...
    %PY% -m venv "%VENV%"
)
if not exist "%VENV%\Scripts\python.exe" (
    echo.
    echo [ERROR] No se pudo crear el entorno virtual "%VENV%".
    goto :fin
)

REM Usar siempre el python del entorno virtual (sin depender de "activate")
set "VPY=%CD%\%VENV%\Scripts\python.exe"

REM === 4. Instalar librerias ===
echo === 3. Instalando librerias (puede tardar la primera vez) ===
"%VPY%" -m pip install --upgrade pip --disable-pip-version-check >nul 2>nul
"%VPY%" -m pip install -r requirements.txt --disable-pip-version-check
if errorlevel 1 (
    echo.
    echo [ERROR] Fallo la instalacion de librerias. Revisa tu conexion a internet.
    echo         Si el problema continua, copia el mensaje completo para revisarlo.
    goto :fin
)

REM === 5. Migraciones de base de datos ===
echo === 4. Aplicando migraciones de base de datos ===
"%VPY%" manage.py migrate
if errorlevel 1 (
    echo.
    echo [ERROR] Fallo "manage.py migrate".
    goto :fin
)

REM === 6. Abrir el navegador unos segundos despues y arrancar el servidor ===
echo.
echo === 5. Iniciando servidor en http://127.0.0.1:8000/ ===
echo El navegador se abrira solo. Para detener el servidor presiona CTRL+C.
start "" /min cmd /c "ping -n 6 127.0.0.1 >nul & start http://127.0.0.1:8000/"
"%VPY%" manage.py runserver 127.0.0.1:8000

:fin
echo.
pause
endlocal