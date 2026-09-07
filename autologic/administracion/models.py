from django.db import models


class Sitio(models.Model):
    """Contenido editable de la página de inicio. Se utiliza como singleton."""

    nombre_marca = models.CharField(max_length=100, default="BarberSpringfield")
    eslogan = models.CharField(max_length=200, default="✂️ CORTES CON PERSONALIDAD")
    hero_titulo = models.CharField(max_length=200, default="Estilo & Elegancia Para Caballeros")
    hero_descripcion = models.TextField(default="Vive la experiencia de una barbería tradicional con técnicas modernas. Atención personalizada, ambiente único y los mejores acabados.")
    hero_imagen_1 = models.URLField(blank=True, default="https://images.unsplash.com/photo-1622286342621-4bd786c2447c?q=80&w=1200&auto=format&fit=crop")
    hero_imagen_2 = models.URLField(blank=True, default="https://images.unsplash.com/photo-1599351431202-1e0f0137899a?q=80&w=1200&auto=format&fit=crop")
    hero_imagen_3 = models.URLField(blank=True, default="https://images.unsplash.com/photo-1517832606299-7ae9b720a186?q=80&w=1200&auto=format&fit=crop")

    servicios_titulo = models.CharField(max_length=150, default="Servicios Populares")
    servicios_subtitulo = models.CharField(max_length=255, default="Cada corte, cada arreglo, hecho con precisión y dedicación")

    barberos_titulo = models.CharField(max_length=150, default="Nuestros Barberos")
    barberos_subtitulo = models.CharField(max_length=255, default="Profesionales apasionados por su arte")

    nosotros_titulo = models.CharField(max_length=200, default="Más que una barbería, un legado")
    nosotros_parrafo_1 = models.TextField(default="Desde 2012, BarberSpringfield es el punto de encuentro para los hombres que valoran la estética, la tradición y la buena conversación.")
    nosotros_parrafo_2 = models.TextField(default="Con un ambiente que fusiona lo vintage con lo moderno, cada visita es una experiencia sensorial.")
    nosotros_punto_1 = models.CharField(max_length=150, default="Profesionales certificados")
    nosotros_punto_2 = models.CharField(max_length=150, default="Productos premium importados")
    nosotros_punto_3 = models.CharField(max_length=150, default="Higiene y esterilización garantizada")
    nosotros_imagen = models.URLField(blank=True, default="https://www.peluker.com/blog/wp-content/uploads/2024/11/Image04Inspiracion-en-mobiliario-de-barberia-vintage-para-un-look-clasico.jpg")

    testimonios_titulo = models.CharField(max_length=150, default="Lo que dicen nuestros clientes")
    testimonios_subtitulo = models.CharField(max_length=255, default="Más de 500 reseñas nos respaldan")
    testimonio_1 = models.TextField(default="Excelente servicio, el barbero entendió exactamente lo que quería.")
    testimonio_1_autor = models.CharField(max_length=100, default="Javier M.")
    testimonio_2 = models.TextField(default="Llevo años buscando un lugar así. El corte Fade perfecto. 100% recomendado.")
    testimonio_2_autor = models.CharField(max_length=100, default="Andrés L.")
    testimonio_3 = models.TextField(default="La mejor barbería de la zona. Precios justos y te dan una cerveza mientras esperas.")
    testimonio_3_autor = models.CharField(max_length=100, default="Camila R.")

    cta_titulo = models.CharField(max_length=200, default="¿Listo para un cambio de look?")
    cta_descripcion = models.TextField(default="Reserva tu cita ahora y obtén un 15% de descuento en tu primer corte.")
    cta_boton = models.CharField(max_length=80, default="Reservar mi espacio")

    footer_descripcion = models.TextField(default="Cortes modernos, atención personalizada y calidad garantizada.")
    horario = models.TextField(default="Lun - Vie: 9:00 AM - 8:00 PM\nSábados: 10:00 AM - 6:00 PM\nDomingos: Cerrado")
    direccion = models.CharField(max_length=255, default="Calle 36B Sur # 5-50")
    telefono = models.CharField(max_length=50, default="+57 301 234 5678")
    email = models.EmailField(default="barberspringfield@gmail.com")
    noticias_titulo = models.CharField(max_length=100, default="Noticias")
    noticias_descripcion = models.TextField(default="Promociones y tips de cuidado masculino.")
    copyright_texto = models.CharField(max_length=255, default="© 2025 BarberSpringfield | Estilo & Elegancia - Todos los derechos reservados")

    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contenido de inicio"
        verbose_name_plural = "Contenido de inicio"

    def __str__(self):
        return self.nombre_marca

    @classmethod
    def obtener(cls):
        sitio = cls.objects.first()
        if sitio is None:
            sitio = cls.objects.create()
        return sitio
