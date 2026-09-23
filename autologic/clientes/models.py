from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    # user puede quedar vacío: son los clientes que el administrador
    # registra a mano cuando alguien llega a la barbería sin cuenta en
    # la página. Así queda un registro de esa persona y de su cita,
    # sin obligarla a crear una cuenta que no va a usar.
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='cliente',
        null=True, blank=True,
    )
    nombre = models.CharField(max_length=200)
    cedula = models.CharField(max_length=20, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, default='')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    # Las cuentas creadas desde la web o por el administrador nacen con
    # el correo pendiente. Las cuentas existentes se consideran confirmadas
    # mediante el valor por defecto de la migración.
    correo_confirmado = models.BooleanField(default=True)

    # Programa de fidelidad: cada 10 cortes finalizados, el siguiente
    # queda gratis.
    cortes_completados = models.PositiveIntegerField(default=0)
    cortes_para_recompensa = models.PositiveIntegerField(default=0)
    recompensas_disponibles = models.PositiveIntegerField(default=0)

    @property
    def registrado(self):
        """True si el cliente tiene cuenta propia en la página."""
        return self.user_id is not None

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']