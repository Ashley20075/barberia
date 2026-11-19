from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from barberos.models import Barbero
from notificaciones.models import Notificacion
from notificaciones.templatetags.notif_tags import notif_info


class ClasificacionTests(TestCase):
    def test_categorias(self):
        casos = {
            '🔔 El turno quedó disponible nuevamente. Lo estabas siguiendo para recibir un aviso.': 'espera',
            'Tu cita con Ana fue cancelada. Este turno quedó libre: 01/01/2026.': 'rechazo',
            'El turno del 01/01/2026 a las 9:00 AM quedó disponible nuevamente.': 'liberado',
            '🆕 Nueva cita: Ana el 01/01/2026.': 'nueva',
            '🎟️ Usaste tu cupón de corte gratis.': 'cupon',
            'Tu cita fue confirmada.': 'confirmada',
            'Hola': 'info',
        }
        for mensaje, esperado in casos.items():
            self.assertEqual(notif_info(mensaje)['clave'], esperado, mensaje)


class PaginaNotificacionesTests(TestCase):
    def _get(self, user):
        Notificacion.objects.create(usuario=user, mensaje='🆕 Nueva cita: Ana')
        self.client.force_login(user)
        return self.client.get(reverse('notificaciones:listar'))

    def test_cliente(self):
        r = self._get(User.objects.create_user('c', 'c@x.com', 'x'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'notif-nueva')
        self.assertContains(r, 'themeToggle')

    def test_admin(self):
        r = self._get(User.objects.create_user('a', 'a@x.com', 'x', is_superuser=True))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'tema-admin')

    def test_barbero(self):
        Barbero.objects.create(nombre='Luis', cedula='1', especialidad='Fade', telefono='3', email='b@x.com')
        r = self._get(User.objects.create_user('b', 'b@x.com', 'x'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'tema-barbero')
