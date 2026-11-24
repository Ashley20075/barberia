from django import forms
from .models import Producto, MovimientoInventario

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'stock_actual', 'stock_minimo', 'stock_maximo', 'precio_unitario']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control bg-dark-input'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control bg-dark-input'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control bg-dark-input'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control bg-dark-input'}),
            'stock_maximo': forms.NumberInput(attrs={'class': 'form-control bg-dark-input'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control bg-dark-input', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Valores por defecto: mínimo 5 y máximo 20 (si se dejan vacíos o en 0).
        for campo in ('stock_minimo', 'stock_maximo'):
            self.fields[campo].required = False
        if not (self.instance and self.instance.pk):
            self.fields['stock_minimo'].initial = 5
            self.fields['stock_maximo'].initial = 20
        # Al editar, el stock NO se cambia aquí: se usa un Ajuste (queda en el historial).
        if self.instance and self.instance.pk:
            self.fields['stock_actual'].disabled = True
            self.fields['stock_actual'].required = False
            self.fields['stock_actual'].help_text = 'Para cambiar el stock registra una entrada o una salida..'

    def clean_stock_minimo(self):
        valor = self.cleaned_data.get('stock_minimo')
        return 5 if valor is None else valor

    def clean_stock_maximo(self):
        valor = self.cleaned_data.get('stock_maximo')
        return 20 if not valor else valor

# Cada entrada de stock debe ser de minimo 5 y maximo 20 unidades.
ENTRADA_MINIMA = 5
ENTRADA_MAXIMA = 20

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['tipo', 'cantidad', 'proveedor', 'fecha', 'nota']  # <-- Agregar proveedor y fecha
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select bg-dark-input'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control bg-dark-input', 'min': 0}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control bg-dark-input', 'placeholder': 'Nombre del proveedor'}),
            'fecha': forms.DateTimeInput(attrs={'class': 'form-control bg-dark-input', 'type': 'datetime-local'}),
            'nota': forms.Textarea(attrs={'class': 'form-control bg-dark-input', 'rows': 2, 'placeholder': 'Observaciones del movimiento'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # El ajuste de stock ya no se ofrece aquí: solo entradas y salidas.
            self.fields['tipo'].choices = [c for c in self.fields['tipo'].choices if c[0] != 'AJUSTE']
    
    def clean(self):
        data = super().clean()
        tipo = data.get('tipo')
        if tipo != 'ENTRADA':
            data['proveedor'] = None
        cantidad = data.get('cantidad')
        if tipo == 'ENTRADA' and cantidad is not None and not (ENTRADA_MINIMA <= cantidad <= ENTRADA_MAXIMA):
            self.add_error(
                'cantidad',
                f'Una entrada debe ser de mínimo {ENTRADA_MINIMA} y máximo {ENTRADA_MAXIMA} unidades.'
            )
        if tipo == 'AJUSTE' and not (data.get('nota') or '').strip():
            self.add_error('nota', 'El ajuste requiere un motivo (conteo físico, producto dañado o perdido).')
        return data