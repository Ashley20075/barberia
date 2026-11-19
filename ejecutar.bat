@echo off
setlocal EnableExtensions
title Barberia - Iniciando sistema
chcp 65001 >nul

REM Ir a la carpeta del proyecto (soporta espacios en la ruta)
cd /d "%~dp0autologic" || (
    echo [ERROR] No se encontro la carpeta "autologic" junto a este archivo.
    goto :fin
)

REM 1) Buscar Python (launcher "py" o "python")
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (
    where python >nul 2>nul && set "PY=python"
)
if not defined PY (
    echo [ERROR] No se encontro Python. Instala Python 3.10+ desde https://www.python.org/downloads/
    echo         y marca la casilla "Add Python to PATH" durante la instalacion.
    goto :fin
)
echo Usando: %PY%

REM 2) Crear entorno virtual si no existe
if not exist ".venv\Scripts\python.exe" (
    echo Creando entorno virtual...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual.
        goto :fin
    )
)

REM 3) Usar siempre el python del venv (sin depender de "activate")
set "VPY=%CD%\.venv\Scripts\python.exe"

echo Instalando dependencias (puede tardar la primera vez)...
"%VPY%" -m pip install --upgrade pip >nul 2>nul
"%VPY%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Fallo la instalacion de dependencias. Revisa tu conexion a internet.
    echo         Si el error menciona "mysql-connector-python", ejecuta de nuevo; si persiste,
    echo         copia el mensaje completo para revisarlo.
    goto :fin
)

echo Aplicando migraciones...
"%VPY%" manage.py migrate
if errorlevel 1 (
    echo [ERROR] Fallo "manage.py migrate".
    goto :fin
)

echo.
echo Abriendo el navegador en http://127.0.0.1:8000/ ...
start "" "http://127.0.0.1:8000/"

echo Servidor iniciado. Para detenerlo presiona CTRL+C.
"%VPY%" manage.py runserver 127.0.0.1:8000

:fin
echo.
pause
endlocal
