from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from barberos.models import Barbero
from citas.models import Cita, Resena, Servicio
from clientes.models import Cliente
from notificaciones.models import Notificacion


class CalificarServicioTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("ana", "ana@example.com", "clave12345")
        self.cliente = Cliente.objects.create(user=self.user, nombre="Ana", email="ana@example.com")
        self.user_barbero = User.objects.create_user("beto", "beto@example.com", "clave12345")
        self.barbero = Barbero.objects.create(
            nombre="Beto", cedula="123", especialidad="Fade", telefono="1",
            email="beto@example.com", calificacion=Decimal("4.0"), numero_resenas=1,
        )
        self.servicio = Servicio.objects.create(nombre="Corte", descripcion="x", precio=20000, duracion=30)
        self.cita = self._cita("Finalizada")
        self.client.force_login(self.user)

    def _cita(self, estado, hora="09:00 AM", cliente=None):
        return Cita.objects.create(
            cliente=cliente or self.cliente, servicio=self.servicio, barbero=self.barbero,
            fecha=date(2030, 1, 7), hora=hora, estado=estado,
        )

    def url(self, cita=None):
        return reverse("calificar_cita", args=[(cita or self.cita).id])

    def test_panel_ofrece_calificar_una_cita_finalizada(self):
        r = self.client.get(reverse("panel_cliente"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'id="avisoCalificar"')
        self.assertContains(r, self.url())

    def test_calificar_guarda_resena_actualiza_barbero_y_notifica(self):
        r = self.client.post(self.url(), {"puntuacion": "5", "comentario": "  Excelente corte  "})
        self.assertRedirects(r, reverse("panel_cliente"))
        resena = Resena.objects.get(cita=self.cita)
        self.assertEqual((resena.puntuacion, resena.comentario), (5, "Excelente corte"))
        self.barbero.refresh_from_db()
        self.assertEqual(self.barbero.numero_resenas, 2)
        self.assertEqual(self.barbero.calificacion, Decimal("4.5"))
        n = Notificacion.objects.get(usuario=self.user_barbero)
        self.assertIn("5/5", n.mensaje)
        self.assertIn("Excelente corte", n.mensaje)

    def test_el_comentario_es_opcional(self):
        self.client.post(self.url(), {"puntuacion": "3"})
        self.assertEqual(Resena.objects.get(cita=self.cita).comentario, "")

    def test_el_panel_muestra_estrellas_y_comentario_despues_de_calificar(self):
        self.client.post(self.url(), {"puntuacion": "4", "comentario": "Muy bien"})
        r = self.client.get(reverse("panel_cliente"))
        self.assertContains(r, "Muy bien")
        self.assertNotContains(r, 'id="avisoCalificar"')

    def test_no_se_puede_calificar_dos_veces(self):
        self.client.post(self.url(), {"puntuacion": "5"})
        self.client.post(self.url(), {"puntuacion": "1"})
        self.assertEqual(Resena.objects.filter(cita=self.cita).count(), 1)
        self.assertEqual(Resena.objects.get(cita=self.cita).puntuacion, 5)
        self.barbero.refresh_from_db()
        self.assertEqual(self.barbero.numero_resenas, 2)

    def test_puntuacion_invalida_no_guarda(self):
        for valor in ["", "0", "6", "abc", "-1"]:
            self.client.post(self.url(), {"puntuacion": valor})
        self.assertFalse(Resena.objects.exists())

    def test_solo_citas_finalizadas(self):
        for estado, hora in [("Pendiente", "10:00 AM"), ("Confirmada", "11:00 AM"), ("Cancelada", "12:00 PM")]:
            self.client.post(self.url(self._cita(estado, hora)), {"puntuacion": "5"})
        self.assertFalse(Resena.objects.exists())

    def test_no_se_puede_calificar_la_cita_de_otro_cliente(self):
        otro = Cliente.objects.create(nombre="Otro")
        ajena = self._cita("Finalizada", "01:00 PM", cliente=otro)
        r = self.client.post(self.url(ajena), {"puntuacion": "5"})
        self.assertEqual(r.status_code, 404)
        self.assertFalse(Resena.objects.exists())

    def test_get_no_califica(self):
        self.client.get(self.url())
        self.assertFalse(Resena.objects.exists())

    def test_requiere_iniciar_sesion(self):
        self.client.logout()
        r = self.client.post(self.url(), {"puntuacion": "5"})
        self.assertEqual(r.status_code, 302)
        self.assertIn("login", r.url)
        self.assertFalse(Resena.objects.exists())
