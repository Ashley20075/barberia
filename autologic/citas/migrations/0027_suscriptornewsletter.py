import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0026_cita_analisis_ia'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuscriptorNewsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('creado', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Suscriptor al newsletter',
                'verbose_name_plural': 'Suscriptores al newsletter',
                'ordering': ['-creado'],
            },
        ),
    ]
