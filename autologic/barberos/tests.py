from datetime import date
from django.test import SimpleTestCase

from .models import Barbero


class JornadaBarberoTests(SimpleTestCase):
    def setUp(self):
        self.barbero = Barbero(
            nombre="Barbero de prueba",
            cedula="TEST-001",
            especialidad="Corte",
            telefono="3000000000",
            email="barbero@example.com",
            dias_laborales="LUN,MAR,MIE,JUE,VIE,SAB",
            dia_descanso="MIE",
        )

    def test_dia_descanso_no_es_laboral_aunque_aparezca_en_lista(self):
        self.assertTrue(self.barbero.es_dia_descanso(date(2026, 11, 11)))
        self.assertFalse(self.barbero.es_dia_laboral(date(2026, 11, 11)))

    def test_dia_laboral_se_reconoce(self):
        self.assertTrue(self.barbero.es_dia_laboral(date(2026, 11, 10)))

    def test_los_otros_seis_dias_son_laborales_aunque_la_lista_antigua_no_los_tenga(self):
        self.barbero.dias_laborales = "MIE"
        self.assertTrue(self.barbero.es_dia_laboral(date(2026, 11, 9)))
        self.assertTrue(self.barbero.es_dia_laboral(date(2026, 11, 12)))

    def test_cambiar_el_descanso_actualiza_los_seis_dias(self):
        self.barbero.dia_descanso = "LUN"
        self.assertFalse(self.barbero.es_dia_laboral(date(2026, 11, 9)))
        self.assertTrue(self.barbero.es_dia_laboral(date(2026, 11, 11)))
        self.assertEqual(len(self.barbero.get_dias_laborales_list()), 6)

    def test_si_el_descanso_cambia_a_jueves_el_miercoles_vuelve_a_ser_laboral(self):
        self.barbero.dia_descanso = "JUE"
        self.assertTrue(self.barbero.es_dia_laboral(date(2026, 11, 11)))
        self.assertFalse(self.barbero.es_dia_laboral(date(2026, 11, 12)))
        self.assertEqual(len(self.barbero.get_dias_laborales_list()), 6)
