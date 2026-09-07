from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Sitio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre_marca", models.CharField(default="BarberSpringfield", max_length=100)),
                ("eslogan", models.CharField(default="✂️ CORTES CON PERSONALIDAD", max_length=200)),
                ("hero_titulo", models.CharField(default="Estilo & Elegancia Para Caballeros", max_length=200)),
                ("hero_descripcion", models.TextField(default="Vive la experiencia de una barbería tradicional con técnicas modernas. Atención personalizada, ambiente único y los mejores acabados.")),
                ("hero_imagen_1", models.URLField(blank=True, default="https://images.unsplash.com/photo-1622286342621-4bd786c2447c?q=80&w=1200&auto=format&fit=crop")),
                ("hero_imagen_2", models.URLField(blank=True, default="https://images.unsplash.com/photo-1599351431202-1e0f0137899a?q=80&w=1200&auto=format&fit=crop")),
                ("hero_imagen_3", models.URLField(blank=True, default="https://images.unsplash.com/photo-1517832606299-7ae9b720a186?q=80&w=1200&auto=format&fit=crop")),
                ("servicios_titulo", models.CharField(default="Servicios Populares", max_length=150)),
                ("servicios_subtitulo", models.CharField(default="Cada corte, cada arreglo, hecho con precisión y dedicación", max_length=255)),
                ("barberos_titulo", models.CharField(default="Nuestros Barberos", max_length=150)),
                ("barberos_subtitulo", models.CharField(default="Profesionales apasionados por su arte", max_length=255)),
                ("nosotros_titulo", models.CharField(default="Más que una barbería, un legado", max_length=200)),
                ("nosotros_parrafo_1", models.TextField(default="Desde 2012, BarberSpringfield es el punto de encuentro para los hombres que valoran la estética, la tradición y la buena conversación.")),
                ("nosotros_parrafo_2", models.TextField(default="Con un ambiente que fusiona lo vintage con lo moderno, cada visita es una experiencia sensorial.")),
                ("nosotros_punto_1", models.CharField(default="Profesionales certificados", max_length=150)),
                ("nosotros_punto_2", models.CharField(default="Productos premium importados", max_length=150)),
                ("nosotros_punto_3", models.CharField(default="Higiene y esterilización garantizada", max_length=150)),
                ("nosotros_imagen", models.URLField(blank=True, default="https://www.peluker.com/blog/wp-content/uploads/2024/11/Image04Inspiracion-en-mobiliario-de-barberia-vintage-para-un-look-clasico.jpg")),
                ("testimonios_titulo", models.CharField(default="Lo que dicen nuestros clientes", max_length=150)),
                ("testimonios_subtitulo", models.CharField(default="Más de 500 reseñas nos respaldan", max_length=255)),
                ("testimonio_1", models.TextField(default="Excelente servicio, el barbero entendió exactamente lo que quería.")),
                ("testimonio_1_autor", models.CharField(default="Javier M.", max_length=100)),
                ("testimonio_2", models.TextField(default="Llevo años buscando un lugar así. El corte Fade perfecto. 100% recomendado.")),
                ("testimonio_2_autor", models.CharField(default="Andrés L.", max_length=100)),
                ("testimonio_3", models.TextField(default="La mejor barbería de la zona. Precios justos y te dan una cerveza mientras esperas.")),
                ("testimonio_3_autor", models.CharField(default="Camila R.", max_length=100)),
                ("cta_titulo", models.CharField(default="¿Listo para un cambio de look?", max_length=200)),
                ("cta_descripcion", models.TextField(default="Reserva tu cita ahora y obtén un 15% de descuento en tu primer corte.")),
                ("cta_boton", models.CharField(default="Reservar mi espacio", max_length=80)),
                ("footer_descripcion", models.TextField(default="Cortes modernos, atención personalizada y calidad garantizada.")),
                ("horario", models.TextField(default="Lun - Vie: 9:00 AM - 8:00 PM\nSábados: 10:00 AM - 6:00 PM\nDomingos: Cerrado")),
                ("direccion", models.CharField(default="Calle 36B Sur # 5-50", max_length=255)),
                ("telefono", models.CharField(default="+57 301 234 5678", max_length=50)),
                ("email", models.EmailField(default="barberspringfield@gmail.com", max_length=254)),
                ("noticias_titulo", models.CharField(default="Noticias", max_length=100)),
                ("noticias_descripcion", models.TextField(default="Promociones y tips de cuidado masculino.")),
                ("copyright_texto", models.CharField(default="© 2025 BarberSpringfield | Estilo & Elegancia - Todos los derechos reservados", max_length=255)),
                ("actualizado", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "Contenido de inicio", "verbose_name_plural": "Contenido de inicio"},
        ),
    ]
