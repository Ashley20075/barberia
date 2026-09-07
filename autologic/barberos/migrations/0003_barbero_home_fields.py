from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("barberos", "0002_barbero_dia_descanso_barbero_dias_laborales_and_more")]
    operations = [
        migrations.AddField(model_name="barbero", name="imagen_url", field=models.URLField(blank=True, default="")),
        migrations.AddField(model_name="barbero", name="calificacion", field=models.DecimalField(decimal_places=1, default=5.0, max_digits=2)),
        migrations.AddField(model_name="barbero", name="numero_resenas", field=models.PositiveIntegerField(default=0)),
        migrations.AddField(model_name="barbero", name="instagram", field=models.URLField(blank=True, default="")),
        migrations.AddField(model_name="barbero", name="facebook", field=models.URLField(blank=True, default="")),
        migrations.AddField(model_name="barbero", name="whatsapp", field=models.URLField(blank=True, default="")),
    ]
