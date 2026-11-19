from types import SimpleNamespace
from unittest import mock

from django.test import TestCase

from clientes.fidelidad import aplicar_cupon, devolver_cupon, procesar_finalizacion
from clientes.models import Cliente


class CicloFidelidadTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nombre='Ana')
        for p in [
            mock.patch('clientes.fidelidad.notificar'),
            mock.patch('clientes.fidelidad.notificar_administradores'),
            mock.patch('clientes.fidelidad.usuario_de_barbero', return_value=None),
            mock.patch('citas.models.Cita.objects'),
        ]:
            p.start()
        self.addCleanup(mock.patch.stopall)

    def cita(self, gratis=False):
        return SimpleNamespace(pk=1, cliente_id=self.cliente.pk, barbero=None, corte_gratis=gratis)

    def recargar(self):
        self.cliente.refresh_from_db()
        return self.cliente

    def test_nueve_cortes_no_dan_cupon(self):
        for _ in range(9):
            self.assertEqual(procesar_finalizacion(self.cita()), 'normal')
        c = self.recargar()
        self.assertEqual((c.cortes_completados, c.cortes_para_recompensa, c.recompensas_disponibles), (9, 9, 0))

    def test_decimo_corte_otorga_cupon_y_reinicia_contador(self):
        for _ in range(9):
            procesar_finalizacion(self.cita())
        self.assertEqual(procesar_finalizacion(self.cita()), 'ganada')
        c = self.recargar()
        self.assertEqual((c.cortes_completados, c.cortes_para_recompensa, c.recompensas_disponibles), (10, 0, 1))

    def test_usar_cupon_descuenta_y_marca_cita(self):
        self.cliente.recompensas_disponibles = 1
        self.cliente.save()
        cita = self.cita()
        self.assertTrue(aplicar_cupon(cita))
        self.assertTrue(cita.corte_gratis)
        self.assertEqual(self.recargar().recompensas_disponibles, 0)

    def test_sin_cupon_no_se_aplica(self):
        cita = self.cita()
        self.assertFalse(aplicar_cupon(cita))
        self.assertFalse(cita.corte_gratis)

    def test_no_se_puede_usar_dos_veces_en_la_misma_cita(self):
        self.cliente.recompensas_disponibles = 2
        self.cliente.save()
        cita = self.cita()
        self.assertTrue(aplicar_cupon(cita))
        self.assertFalse(aplicar_cupon(cita))
        self.assertEqual(self.recargar().recompensas_disponibles, 1)

    def test_cita_con_cupon_no_suma_al_ciclo(self):
        self.assertEqual(procesar_finalizacion(self.cita(gratis=True)), 'cupon')
        c = self.recargar()
        self.assertEqual((c.cortes_completados, c.cortes_para_recompensa), (0, 0))

    def test_cancelar_devuelve_el_cupon(self):
        self.cliente.recompensas_disponibles = 1
        self.cliente.save()
        cita = self.cita()
        aplicar_cupon(cita)
        self.assertTrue(devolver_cupon(cita))
        self.assertEqual(self.recargar().recompensas_disponibles, 1)
        self.assertFalse(devolver_cupon(cita))   # ya no tiene cupón: no devuelve dos veces

    def test_ciclo_completo(self):
        for _ in range(10):
            procesar_finalizacion(self.cita())
        self.assertEqual(self.recargar().recompensas_disponibles, 1)
        cita = self.cita()
        aplicar_cupon(cita)
        self.assertEqual(procesar_finalizacion(cita), 'cupon')
        c = self.recargar()
        self.assertEqual((c.recompensas_disponibles, c.cortes_para_recompensa, c.cortes_completados), (0, 0, 10))
        procesar_finalizacion(self.cita())
        c = self.recargar()
        self.assertEqual((c.cortes_completados, c.cortes_para_recompensa), (11, 1))
