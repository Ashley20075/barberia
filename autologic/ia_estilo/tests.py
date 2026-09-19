from django.test import SimpleTestCase


class IaEstiloSmokeTest(SimpleTestCase):
    def test_url_exists(self):
        response = self.client.get('/ia-estilo/')
        self.assertEqual(response.status_code, 200)
