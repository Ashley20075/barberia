from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("notificaciones", "0001_initial"),
        ("barberos", "0003_barbero_home_fields"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SuscripcionTurno",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha", models.DateField()),
                ("hora", models.CharField(max_length=20)),
                ("creada", models.DateTimeField(auto_now_add=True)),
                ("barbero", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="suscripciones_turnos", to="barberos.barbero")),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="suscripciones_turnos", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Suscripción a turno",
                "verbose_name_plural": "Suscripciones a turnos",
                "ordering": ["fecha", "hora"],
            },
        ),
        migrations.AddConstraint(
            model_name="suscripcionturno",
            constraint=models.UniqueConstraint(fields=("usuario", "barbero", "fecha", "hora"), name="unique_suscripcion_turno_usuario"),
        ),
    ]
