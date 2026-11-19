from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import MovimientoForm, ProductoForm
from .models import MovimientoInventario, Producto
from .utils import registrar_movimiento


class MovimientosTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', password='x', is_superuser=True)
        self.p = Producto.objects.create(
            nombre='Cera', stock_actual=10, stock_minimo=3, stock_maximo=15, precio_unitario=5000)

    def test_entrada_actualiza_stock_y_guarda_proveedor(self):
        m = registrar_movimiento(self.p, 'ENTRADA', 3, usuario=self.user, proveedor='ACME')
        self.p.refresh_from_db()
        self.assertEqual(self.p.stock_actual, 13)
        self.assertEqual((m.stock_anterior, m.stock_nuevo, m.proveedor), (10, 13, 'ACME'))

    def test_entrada_no_supera_maximo(self):
        with self.assertRaises(ValueError):
            registrar_movimiento(self.p, 'ENTRADA', 6)
        self.p.refresh_from_db()
        self.assertEqual(self.p.stock_actual, 10)
        self.assertEqual(MovimientoInventario.objects.count(), 0)

    def test_salida_sin_proveedor_y_puede_llegar_a_cero(self):
        m = registrar_movimiento(self.p, 'SALIDA', 10, proveedor='NO-DEBE-GUARDARSE')
        self.p.refresh_from_db()
        self.assertEqual(self.p.stock_actual, 0)
        self.assertIsNone(m.proveedor)

    def test_salida_no_supera_stock(self):
        with self.assertRaises(ValueError):
            registrar_movimiento(self.p, 'SALIDA', 11)

    def test_ajuste_requiere_motivo_y_respeta_maximo(self):
        with self.assertRaises(ValueError):
            registrar_movimiento(self.p, 'AJUSTE', 8)
        with self.assertRaises(ValueError):
            registrar_movimiento(self.p, 'AJUSTE', 16, nota='conteo')
        m = registrar_movimiento(self.p, 'AJUSTE', 8, nota='conteo físico', proveedor='X')
        self.p.refresh_from_db()
        self.assertEqual((self.p.stock_actual, m.stock_anterior, m.stock_nuevo), (8, 10, 8))
        self.assertIsNone(m.proveedor)

    def test_devolucion_puede_omitir_validacion_de_maximo(self):
        registrar_movimiento(self.p, 'ENTRADA', 20, validar_maximo=False)
        self.p.refresh_from_db()
        self.assertEqual(self.p.stock_actual, 30)


class ValidacionProductoTests(TestCase):
    def test_minimo_no_mayor_que_maximo(self):
        f = ProductoForm({'nombre': 'A', 'stock_actual': 1, 'stock_minimo': 9,
                          'stock_maximo': 5, 'precio_unitario': 1})
        self.assertFalse(f.is_valid())

    def test_stock_no_mayor_que_maximo(self):
        f = ProductoForm({'nombre': 'A', 'stock_actual': 9, 'stock_minimo': 1,
                          'stock_maximo': 5, 'precio_unitario': 1})
        self.assertFalse(f.is_valid())

    def test_formulario_ajuste_exige_motivo(self):
        f = MovimientoForm({'tipo': 'AJUSTE', 'cantidad': 4, 'fecha': '2026-01-01T10:00'})
        self.assertFalse(f.is_valid())
        self.assertIn('nota', f.errors)


class VistasInventarioTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', password='x', is_superuser=True)
        self.client.login(username='admin', password='x')

    def test_crear_producto_con_stock_inicial_queda_en_historial(self):
        self.client.post(reverse('inventario:agregar'), {
            'nombre': 'Gel', 'descripcion': '', 'stock_actual': 7, 'stock_minimo': 2,
            'stock_maximo': 12, 'precio_unitario': '3000'})
        p = Producto.objects.get(nombre='Gel')
        self.assertEqual(p.stock_actual, 7)
        mov = p.movimientos.get()
        self.assertEqual((mov.tipo, mov.cantidad, mov.stock_nuevo), ('ENTRADA', 7, 7))

    def test_editar_no_cambia_stock(self):
        p = Producto.objects.create(nombre='Gel', stock_actual=5, stock_minimo=1, stock_maximo=10)
        self.client.post(reverse('inventario:editar', args=[p.id]), {
            'nombre': 'Gel2', 'descripcion': '', 'stock_actual': 9, 'stock_minimo': 2,
            'stock_maximo': 11, 'precio_unitario': '1'})
        p.refresh_from_db()
        self.assertEqual((p.nombre, p.stock_actual, p.stock_maximo), ('Gel2', 5, 11))

    def test_movimiento_via_vista_entrada_salida_ajuste(self):
        p = Producto.objects.create(nombre='Gel', stock_actual=5, stock_minimo=1, stock_maximo=10)
        url = reverse('inventario:movimiento', args=[p.id])
        base = {'fecha': '2026-01-01T10:00'}
        self.client.post(url, dict(base, tipo='ENTRADA', cantidad=3, proveedor='P'))
        self.client.post(url, dict(base, tipo='SALIDA', cantidad=2, proveedor='P'))
        self.client.post(url, dict(base, tipo='AJUSTE', cantidad=4, nota='conteo'))
        p.refresh_from_db()
        self.assertEqual(p.stock_actual, 4)
        self.assertEqual(p.movimientos.count(), 3)
        self.assertEqual(p.movimientos.filter(proveedor__isnull=False).count(), 1)

    def test_pdf_se_genera(self):
        Producto.objects.create(nombre='Gel', stock_actual=5, stock_minimo=1, stock_maximo=10)
        r = self.client.get(reverse('inventario:reporte_pdf'))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.content.startswith(b'%PDF'))
