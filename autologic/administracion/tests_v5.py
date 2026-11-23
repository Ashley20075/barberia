from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from clientes.models import Cliente


class PaginasAdminTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", "admin@example.com", "clave12345")
        self.client.force_login(self.admin)

    def test_agendar_admin_muestra_total_y_ninguno(self):
        r = self.client.get(reverse("administracion:agendar_cita_admin"))
        self.assertContains(r, 'id="totalPagar"')
        self.assertContains(r, "Ninguno")
        self.assertContains(r, "btn-volver-panel")

    def test_navbar_pide_confirmacion_para_cerrar_sesion(self):
        r = self.client.get(reverse("administracion:panel_admin"))
        self.assertContains(r, "Sí, cerrar sesión")

    def test_perdonar_penalizacion(self):
        u = User.objects.create_user("ana", "ana@example.com", "clave12345")
        c = Cliente.objects.create(user=u, nombre="Ana", email="ana@example.com",
                                   inasistencias=2, penalizado_hasta=timezone.localdate())
        self.client.get(reverse("administracion:perdonar_penalizacion", args=[c.id]))
        c.refresh_from_db()
        self.assertEqual((c.inasistencias, c.penalizado_hasta), (0, None))
        self.assertEqual(self.client.get(reverse("inventario:dashboard")).status_code, 200)
