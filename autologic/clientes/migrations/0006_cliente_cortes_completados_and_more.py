from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0005_cliente_correo_confirmado'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='cortes_completados',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cortes_para_recompensa',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cliente',
            name='recompensas_disponibles',
            field=models.PositiveIntegerField(default=0),
        ),
    ]