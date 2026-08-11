
crea un entorno virtual
python -m venv venv

Activar entorno virtual
venv\Scripts\activate

instalar django
pip install django

pip install django-extensions

Configurar la db
python manage.py makemigrations
python manage.py migrate

Crear un admin
python manage.py createsuperuser

iniciar servidor
python manage.py runserver


set PATH=C:\Users\aprendiz\Desktop\windows_10_cmake_Release_Graphviz-15.0.0-win32\Graphviz-15.0.0-win32\bin;%PATH%

py manage.py makemigrations
py manage.py migrate
py manage.py graph_models -a -o modelo_barberia.png

libreria para pdf
pip install reportlab


MAC

python3 -m venv venv
pip install django django-extensions reportlab
pip install requests
pip install twilio
pip install python-dotenv
cd django
python manage.py makemigrations
python manage.py migrate
python manage.py runserver