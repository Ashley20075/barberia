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
        # Al editar, el stock NO se cambia aquí: se usa un Ajuste (queda en el historial).
        if self.instance and self.instance.pk:
            self.fields['stock_actual'].disabled = True
            self.fields['stock_actual'].required = False
            self.fields['stock_actual'].help_text = 'Para cambiar el stock usa "Ajustar stock".'

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

    def clean(self):
        data = super().clean()
        tipo = data.get('tipo')
        if tipo != 'ENTRADA':
            data['proveedor'] = None
        if tipo == 'AJUSTE' and not (data.get('nota') or '').strip():
            self.add_error('nota', 'El ajuste requiere un motivo (conteo físico, producto dañado o perdido).')
        return data