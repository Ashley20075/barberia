
crea un entorno virtual

python -m venv venv

Activar entorno virtual

venv\Scripts\activate

pip install django django-extensions reportlab

Configurar la db

cd django
python manage.py makemigrations
python manage.py migrate

Crear un admin
python manage.py createsuperuser

iniciar servidor
python manage.py runserver

python manage.py enviar_recordatorios


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


python manage.py enviar_recordatorios