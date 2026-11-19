from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0012_alter_producto_stock_actual'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='stock_maximo',
            field=models.PositiveIntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='producto',
            name='stock_actual',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
