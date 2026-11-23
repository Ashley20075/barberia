from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from barberos.models import Barbero
from citas.asistencia import InasistenciaInvalida, marcar_no_asistio
from citas.models import Cita, Servicio
from clientes.models import Cliente
from notificaciones.models import Notificacion, SuscripcionTurno


class BaseCitas(TestCase):
    def setUp(self):
        self.hoy = timezone.localdate()
        self.admin = User.objects.create_superuser("admin", "admin@example.com", "clave12345")
        self.u_cliente = User.objects.create_user("ana", "ana@example.com", "clave12345")
        self.cliente = Cliente.objects.create(user=self.u_cliente, nombre="Ana", email="ana@example.com")
        self.u_barbero = User.objects.create_user("beto", "beto@example.com", "clave12345")
        self.barbero = Barbero.objects.create(
            nombre="Beto", cedula="1", especialidad="Fade", telefono="1",
            email="beto@example.com", dia_descanso="DOM",
        )
        self.servicio = Servicio.objects.create(nombre="Corte", descripcion="x", precio=20000, duracion=30)

    def cita(self, dias, hora="10:00 AM", estado="Confirmada", cliente=None, **kw):
        return Cita.objects.create(
            cliente=cliente or self.cliente, servicio=self.servicio, barbero=self.barbero,
            fecha=self.hoy + timedelta(days=dias), hora=hora, estado=estado, duracion_total=40, **kw,
        )

    def dia_laboral(self, desde):
        d = desde
        while not self.barbero.es_dia_laboral(self.hoy + timedelta(days=d)):
            d += 1
        return d


class CancelacionConAntelacionTests(BaseCitas):
    def test_no_se_puede_cancelar_con_menos_de_24_horas(self):
        cita = self.cita(0, hora="11:59 PM")
        self.client.force_login(self.u_cliente)
        self.client.get(reverse("cancelar_cita_cliente", args=[cita.id]))
        cita.refresh_from_db()
        self.assertEqual(cita.estado, "Confirmada")

    def test_se_puede_cancelar_con_dos_dias(self):
        cita = self.cita(self.dia_laboral(3))
        self.client.force_login(self.u_cliente)
        self.client.get(reverse("cancelar_cita_cliente", args=[cita.id]))
        cita.refresh_from_db()
        self.assertEqual(cita.estado, "Cancelada")


class InasistenciaTests(BaseCitas):
    def test_no_se_puede_marcar_antes_de_la_hora(self):
        cita = self.cita(5)
        with self.assertRaises(InasistenciaInvalida):
            marcar_no_asistio(cita, "cliente")

    def test_primera_falta_es_advertencia_y_segunda_bloquea(self):
        c1 = self.cita(-3)
        marcar_no_asistio(c1, "cliente")
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.inasistencias, 1)
        self.assertFalse(self.cliente.penalizado)
        self.assertEqual(c1.estado, "NoAsistio")

        c2 = self.cita(-2)
        marcar_no_asistio(c2, "cliente")
        self.cliente.refresh_from_db()
        self.assertTrue(self.cliente.penalizado)
        self.assertEqual(self.cliente.penalizado_hasta, self.hoy + timedelta(days=7))

    def test_cliente_penalizado_no_puede_agendar(self):
        self.cliente.penalizado_hasta = self.hoy + timedelta(days=3)
        self.cliente.save()
        self.client.force_login(self.u_cliente)
        d = self.dia_laboral(2)
        self.client.post(reverse("agendar_cita"), {
            "servicio": self.servicio.id, "barbero": self.barbero.id,
            "fecha": (self.hoy + timedelta(days=d)).isoformat(), "hora": "10:00 AM", "duracion_total": 40,
        })
        self.assertFalse(Cita.objects.filter(estado="Pendiente").exists())

    def test_falta_del_barbero_compensa_con_cupon_y_avisa_al_admin(self):
        cita = self.cita(-1)
        marcar_no_asistio(cita, "barbero")
        self.cliente.refresh_from_db()
        self.barbero.refresh_from_db()
        self.assertEqual(self.cliente.recompensas_disponibles, 1)
        self.assertEqual(self.barbero.inasistencias, 1)
        self.assertEqual(self.cliente.inasistencias, 0)
        self.assertTrue(Notificacion.objects.filter(usuario=self.admin).exists())

    def test_barbero_marca_desde_su_panel(self):
        cita = self.cita(-1)
        self.client.force_login(self.u_barbero)
        self.client.get(reverse("barberos:cliente_no_asistio", args=[cita.id]))
        cita.refresh_from_db()
        self.assertEqual((cita.estado, cita.falta_de), ("NoAsistio", "cliente"))

    def test_admin_marca_desde_su_panel(self):
        cita = self.cita(-1)
        self.client.force_login(self.admin)
        self.client.get(reverse("administracion:marcar_inasistencia", args=[cita.id, "barbero"]))
        cita.refresh_from_db()
        self.assertEqual((cita.estado, cita.falta_de), ("NoAsistio", "barbero"))

    def test_paneles_cargan_con_citas_no_asistidas(self):
        marcar_no_asistio(self.cita(-1), "cliente")
        for user, url in [(self.u_cliente, "panel_cliente"), (self.u_barbero, "barberos:panel_barbero"),
                          (self.admin, "administracion:panel_admin")]:
            self.client.force_login(user)
            self.assertEqual(self.client.get(reverse(url)).status_code, 200)


class ListaDeEsperaTests(BaseCitas):
    def setUp(self):
        super().setUp()
        self.u2 = User.objects.create_user("carla", "carla@example.com", "clave12345")
        self.cliente2 = Cliente.objects.create(user=self.u2, nombre="Carla", email="carla@example.com")
        self.u3 = User.objects.create_user("dani", "dani@example.com", "clave12345")
        self.cliente3 = Cliente.objects.create(user=self.u3, nombre="Dani", email="dani@example.com")
        self.d = self.dia_laboral(4)
        self.cita_ocupada = self.cita(self.d)

    def esperar(self, user):
        return SuscripcionTurno.objects.create(
            usuario=user, barbero=self.barbero, fecha=self.cita_ocupada.fecha, hora="10:00 AM",
            servicio=self.servicio, duracion_total=40,
        )

    def test_el_primero_de_la_fila_queda_agendado_automaticamente(self):
        self.esperar(self.u2)
        self.esperar(self.u3)
        self.cita_ocupada.estado = "Cancelada"
        self.cita_ocupada.save()
        nueva = Cita.objects.get(cliente=self.cliente2, estado="Pendiente")
        self.assertEqual((nueva.hora, nueva.barbero), ("10:00 AM", self.barbero))
        self.assertFalse(Cita.objects.filter(cliente=self.cliente3, estado="Pendiente").exists())
        # el segundo sigue esperando
        self.assertTrue(SuscripcionTurno.objects.filter(usuario=self.u3).exists())
        self.assertFalse(SuscripcionTurno.objects.filter(usuario=self.u2).exists())

    def test_se_salta_al_penalizado(self):
        self.cliente2.penalizado_hasta = self.hoy + timedelta(days=5)
        self.cliente2.save()
        self.esperar(self.u2)
        self.esperar(self.u3)
        self.cita_ocupada.estado = "Cancelada"
        self.cita_ocupada.save()
        self.assertTrue(Cita.objects.filter(cliente=self.cliente3, estado="Pendiente").exists())
        self.assertFalse(Cita.objects.filter(cliente=self.cliente2, estado="Pendiente").exists())

    def test_endpoint_guarda_servicio_en_la_lista(self):
        self.client.force_login(self.u2)
        r = self.client.post(reverse("notificaciones:suscribirse_turno"), {
            "barbero": self.barbero.id, "fecha": self.cita_ocupada.fecha.isoformat(), "hora": "10:00 AM",
            "duracion_total": 40, "servicio": self.servicio.id, "suscrito": "true",
        })
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(SuscripcionTurno.objects.get(usuario=self.u2).servicio, self.servicio)
