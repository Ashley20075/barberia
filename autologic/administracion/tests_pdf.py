from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from barberos.models import Barbero


class PdfsTests(TestCase):
    def setUp(self):
        User.objects.create_user('admin', password='x', is_superuser=True, is_staff=True)
        self.client.login(username='admin', password='x')

    def test_cierre_caja_pdf_sin_datos(self):
        r = self.client.get(reverse('administracion:cierre_caja_pdf'))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.content.startswith(b'%PDF'))

    def test_cierre_caja_pdf_rango(self):
        r = self.client.get(reverse('administracion:cierre_caja_pdf'),
                            {'fecha_inicio': '2026-01-01', 'fecha_fin': '2026-01-31'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.content.startswith(b'%PDF'))

    def test_certificado_barbero_pdf(self):
        b = Barbero.objects.create(nombre='Luis', cedula='123', especialidad='Fade',
                                   telefono='300', email='luis@x.com')
        r = self.client.get(reverse('administracion:certificado_barbero_admin', args=[b.id]))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.content.startswith(b'%PDF'))
