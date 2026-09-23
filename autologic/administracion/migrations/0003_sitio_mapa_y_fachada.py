# Generado manualmente para agregar mapa embebido e imagen de fachada.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0002_rename_hero_imagen_1_sitio_hero_imagen_1_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitio',
            name='mapa_embed_url',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='sitio',
            name='fachada_imagen_url',
            field=models.URLField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='sitio',
            name='fachada_imagen_archivo',
            field=models.ImageField(blank=True, null=True, upload_to='home/'),
        ),
        migrations.AddField(
            model_name='sitio',
            name='fachada_imagen_fuente',
            field=models.CharField(choices=[('url', 'URL'), ('archivo', 'Archivo del dispositivo')], default='url', max_length=10),
        ),
    ]
