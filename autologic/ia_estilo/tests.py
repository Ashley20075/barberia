from django.contrib.auth.models import User
from django.test import TestCase


class IaEstiloSmokeTest(TestCase):
    def test_url_exists(self):
        # La vista exige sesion: sin login redirige (302) al login.
        self.assertEqual(self.client.get('/ia-estilo/').status_code, 302)
        User.objects.create_user('u', password='x')
        self.client.login(username='u', password='x')
        self.assertEqual(self.client.get('/ia-estilo/').status_code, 200)
