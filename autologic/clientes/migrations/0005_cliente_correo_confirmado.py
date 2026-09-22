from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0004_cliente_user_nullable'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='correo_confirmado',
            field=models.BooleanField(default=True),
        ),
    ]
