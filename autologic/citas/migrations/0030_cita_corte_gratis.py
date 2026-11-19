from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0029_servicio_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='corte_gratis',
            field=models.BooleanField(default=False),
        ),
    ]
