from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("barberos", "0003_barbero_home_fields")]

    operations = [
        migrations.AddField(
            model_name="barbero",
            name="es_barbero",
            field=models.BooleanField(default=True),
        ),
    ]
