from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0006_cliente_cortes_completados_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='foto_perfil',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='clientes/perfil/',
                help_text='Foto de perfil que el cliente sube desde "Editar Perfil".',
            ),
        ),
    ]