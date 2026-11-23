from django.db import migrations


def corregir_limites(apps, schema_editor):
    Producto = apps.get_model("inventario", "Producto")
    Producto.objects.filter(stock_maximo=0).update(stock_maximo=20)
    for p in Producto.objects.all():
        if p.stock_minimo > p.stock_maximo:
            p.stock_minimo = min(5, p.stock_maximo)
            p.save(update_fields=["stock_minimo"])


class Migration(migrations.Migration):

    dependencies = [
        ("inventario", "0013_producto_stock_maximo"),
    ]

    operations = [
        migrations.RunPython(corregir_limites, migrations.RunPython.noop),
    ]
