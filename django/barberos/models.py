from django.db import models

class Barbero(models.Model):
    DIAS_SEMANA = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]
    
    nombre = models.CharField(max_length=200)
    cedula = models.CharField(max_length=20, unique=True)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    # ===== NUEVOS CAMPOS DE HORARIO =====
    jornada_inicio = models.TimeField(default='08:00')
    jornada_fin = models.TimeField(default='18:00')
    duracion_cita = models.IntegerField(default=30)
    dias_laborales = models.CharField(max_length=50, default='LUN,MAR,MIE,JUE,VIE,SAB')
    dia_descanso = models.CharField(max_length=3, choices=DIAS_SEMANA, default='DOM')
    tiempo_entre_citas = models.IntegerField(default=15)
    
    def __str__(self):
        return self.nombre
    
    def get_dias_laborales_list(self):
        return self.dias_laborales.split(',') if self.dias_laborales else []
    
    def es_dia_laboral(self, fecha):
        from datetime import datetime
        dias = {0: 'LUN', 1: 'MAR', 2: 'MIE', 3: 'JUE', 4: 'VIE', 5: 'SAB', 6: 'DOM'}
        dia_semana = dias[fecha.weekday()]
        return dia_semana in self.get_dias_laborales_list()
    
    def es_dia_descanso(self, fecha):
        from datetime import datetime
        dias = {0: 'LUN', 1: 'MAR', 2: 'MIE', 3: 'JUE', 4: 'VIE', 5: 'SAB', 6: 'DOM'}
        dia_semana = dias[fecha.weekday()]
        return dia_semana == self.dia_descanso
    
    def horarios_disponibles(self, fecha, duracion=35):
        import datetime
        from citas.models import Cita

        if not self.es_dia_laboral(fecha) or self.es_dia_descanso(fecha):
            return []

        inicio = datetime.datetime.combine(fecha, self.jornada_inicio)
        fin = datetime.datetime.combine(fecha, self.jornada_fin)

        citas = Cita.objects.filter(
            barbero=self,
            fecha=fecha,
            estado__in=["Pendiente", "Confirmada"]
        )

        horarios = []

        while inicio + datetime.timedelta(minutes=duracion) <= fin:

            hora_fin = inicio + datetime.timedelta(minutes=duracion)

            ocupado = False

            for cita in citas:

                cita_inicio = datetime.datetime.combine(
                    fecha,
                    datetime.datetime.strptime(cita.hora, "%I:%M %p").time()
                )

                cita_fin = cita_inicio + datetime.timedelta(
                    minutes=cita.duracion_total + self.tiempo_entre_citas
                )

                if inicio < cita_fin and hora_fin > cita_inicio:
                    ocupado = True
                    break

            if not ocupado:
                horarios.append(inicio.strftime("%I:%M %p"))

            inicio += datetime.timedelta(minutes=15)

        return horarios
    
    class Meta:
        verbose_name = 'Barbero'
        verbose_name_plural = 'Barberos'
        ordering = ['nombre']