from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from barberos.models import Barbero
from citas.models import Cita, Servicio
from clientes.models import Cliente

from .models import Notificacion, SuscripcionTurno


class NotificacionesCancelacionTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="testpass123"
        )
        self.cliente_user = User.objects.create_user(
            username="cliente", email="cliente@example.com", password="testpass123"
        )
        self.suscriptor_user = User.objects.create_user(
            username="suscriptor", email="suscriptor@example.com", password="testpass123"
        )
        self.barbero_user = User.objects.create_user(
            username="barbero", email="barbero@example.com", password="testpass123"
        )

        self.cliente = Cliente.objects.create(
            user=self.cliente_user,
            nombre="Cliente Prueba",
            cedula="100000001",
            telefono="3000000000",
            email="cliente@example.com",
        )
        self.suscriptor = Cliente.objects.create(
            user=self.suscriptor_user,
            nombre="Suscriptor Prueba",
            cedula="100000002",
            telefono="3000000001",
            email="suscriptor@example.com",
        )
        self.barbero = Barbero.objects.create(
            nombre="Barbero Prueba",
            cedula="200000001",
            especialidad="Corte",
            telefono="3000000002",
            email="barbero@example.com",
        )
        self.servicio = Servicio.objects.create(
            nombre="Corte clásico",
            descripcion="Corte de prueba",
            precio=20000,
            duracion=35,
        )

    def test_cancelacion_notifica_a_los_involucrados_y_suscriptores(self):
        cita = Cita.objects.create(
            cliente=self.cliente,
            servicio=self.servicio,
            barbero=self.barbero,
            fecha=date(2026, 10, 1),
            hora="10:00 AM",
            duracion_total=35,
            estado="Confirmada",
        )

        SuscripcionTurno.objects.create(
            usuario=self.suscriptor_user,
            barbero=self.barbero,
            fecha=cita.fecha,
            hora=cita.hora,
        )

        cita.estado = "Cancelada"
        cita.save()

        usuarios = {n.usuario.username for n in Notificacion.objects.filter(cita=cita)}
        self.assertEqual(usuarios, {"admin", "cliente", "barbero", "suscriptor"})

        aviso_barbero = Notificacion.objects.get(
            usuario=self.barbero_user,
            cita=cita,
        )
        self.assertIn("Tu cita con Cliente Prueba fue cancelada.", aviso_barbero.mensaje)
        self.assertIn("Este turno quedó libre: 01/10/2026 a las 10:00 AM", aviso_barbero.mensaje)
        self.assertIn("(Corte clásico)", aviso_barbero.mensaje)
        self.assertFalse(
            SuscripcionTurno.objects.filter(
                usuario=self.suscriptor_user,
                barbero=self.barbero,
                fecha=cita.fecha,
                hora=cita.hora,
            ).exists()
        )

    def test_guardar_cancelada_de_nuevo_no_duplica_notificaciones(self):
        cita = Cita.objects.create(
            cliente=self.cliente,
            servicio=self.servicio,
            barbero=self.barbero,
            fecha=date(2026, 10, 2),
            hora="11:00 AM",
            duracion_total=35,
            estado="Confirmada",
        )
        cita.estado = "Cancelada"
        cita.save()
        cantidad = Notificacion.objects.filter(cita=cita).count()

        cita.save()

        self.assertEqual(Notificacion.objects.filter(cita=cita).count(), cantidad)


    def test_usuario_puede_vaciar_sus_notificaciones(self):
        Notificacion.objects.create(
            usuario=self.cliente_user,
            mensaje="Aviso de prueba",
        )
        Notificacion.objects.create(
            usuario=self.barbero_user,
            mensaje="Aviso de otro usuario",
        )

        self.client.force_login(self.cliente_user)
        response = self.client.post(
            "/notificaciones/vaciar/",
            {"next": "/notificaciones/"},
        )

        self.assertRedirects(response, "/notificaciones/")
        self.assertFalse(
            Notificacion.objects.filter(usuario=self.cliente_user).exists()
        )
        self.assertTrue(
            Notificacion.objects.filter(usuario=self.barbero_user).exists()
        )
