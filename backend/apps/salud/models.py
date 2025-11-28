from django.db import models
from apps.poblacion.models.personas import Persona

# Modelo para historial médico
class HistorialMedico(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='historial_medico')
    antecedentes_familiares = models.TextField(blank=True, null=True, help_text="Antecedentes familiares relevantes")
    alergias = models.TextField(blank=True, null=True, help_text="Alergias conocidas")
    medicamentos_actuales = models.TextField(blank=True, null=True, help_text="Medicamentos que toma actualmente")
    condiciones_cronicas = models.TextField(blank=True, null=True, help_text="Condiciones médicas crónicas")
    cirugias_previas = models.TextField(blank=True, null=True, help_text="Cirugías o procedimientos previos")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Historial médico de {self.persona}"

    class Meta:
        verbose_name = "Historial Médico"
        verbose_name_plural = "Historiales Médicos"

# Modelo para vacunas
class Vacuna(models.Model):
    TIPO_VACUNA_CHOICES = [
        ('rutinaria', 'Rutinaria'),
        ('campana', 'Campaña'),
        ('especial', 'Especial'),
    ]

    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='vacunas')
    nombre_vacuna = models.CharField(max_length=200, help_text="Nombre de la vacuna")
    tipo_vacuna = models.CharField(max_length=20, choices=TIPO_VACUNA_CHOICES, default='rutinaria')
    fecha_aplicacion = models.DateField()
    dosis = models.CharField(max_length=50, blank=True, null=True, help_text="Número de dosis o descripción")
    lote = models.CharField(max_length=100, blank=True, null=True, help_text="Lote de la vacuna")
    profesional_salud = models.CharField(max_length=200, blank=True, null=True, help_text="Profesional que aplicó la vacuna")
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_vacuna} - {self.persona} ({self.fecha_aplicacion})"

    class Meta:
        verbose_name = "Vacuna"
        verbose_name_plural = "Vacunas"
        ordering = ['-fecha_aplicacion']

# Modelo para medicamentos
class Medicamento(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='medicamentos')
    nombre_medicamento = models.CharField(max_length=200, help_text="Nombre del medicamento")
    dosis = models.CharField(max_length=100, help_text="Dosis prescrita")
    frecuencia = models.CharField(max_length=100, help_text="Frecuencia de administración")
    duracion = models.CharField(max_length=100, blank=True, null=True, help_text="Duración del tratamiento")
    indicacion = models.TextField(help_text="Indicación médica")
    fecha_prescripcion = models.DateField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    profesional_salud = models.CharField(max_length=200, blank=True, null=True, help_text="Profesional que prescribió")
    observaciones = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True, help_text="Si el medicamento está activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_medicamento} - {self.persona}"

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"
        ordering = ['-fecha_prescripcion']

# Modelo para exámenes médicos
class ExamenMedico(models.Model):
    TIPO_EXAMEN_CHOICES = [
        ('laboratorio', 'Laboratorio'),
        ('imagen', 'Imagenología'),
        ('funcional', 'Funcional'),
        ('endoscopia', 'Endoscopía'),
        ('otros', 'Otros'),
    ]

    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='examenes_medicos')
    tipo_examen = models.CharField(max_length=20, choices=TIPO_EXAMEN_CHOICES)
    nombre_examen = models.CharField(max_length=200, help_text="Nombre específico del examen")
    fecha_solicitud = models.DateField()
    fecha_realizacion = models.DateField(blank=True, null=True)
    resultado = models.TextField(blank=True, null=True)
    interpretacion = models.TextField(blank=True, null=True, help_text="Interpretación médica del resultado")
    profesional_solicitante = models.CharField(max_length=200, blank=True, null=True)
    profesional_interpretador = models.CharField(max_length=200, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_examen} - {self.persona} ({self.fecha_solicitud})"

    class Meta:
        verbose_name = "Examen Médico"
        verbose_name_plural = "Exámenes Médicos"
        ordering = ['-fecha_solicitud']

# Modelo para registros de salud
class RegistroSalud(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='registros_salud')
    fecha_registro = models.DateField()
    tipo_registro = models.CharField(max_length=100, help_text="Tipo de registro (ej: consulta, vacunación)")
    descripcion = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Registro de {self.persona} - {self.tipo_registro} ({self.fecha_registro})"

    class Meta:
        verbose_name = "Registro de Salud"
        verbose_name_plural = "Registros de Salud"
        ordering = ['-fecha_registro']

# Modelo para alertas de salud
class AlertaSalud(models.Model):
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]

    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='alertas_salud')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    fecha_alerta = models.DateField(auto_now_add=True)
    resuelta = models.BooleanField(default=False)
    fecha_resolucion = models.DateField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Alerta para {self.persona} - {self.titulo} ({self.prioridad})"

    class Meta:
        verbose_name = "Alerta de Salud"
        verbose_name_plural = "Alertas de Salud"
        ordering = ['-fecha_alerta']

# Modelo para controles de salud
class ControlSalud(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='controles_salud')
    tipo_control = models.CharField(max_length=100, help_text="Tipo de control (ej: vacunación, chequeo)")
    fecha_programada = models.DateField()
    fecha_realizada = models.DateField(blank=True, null=True)
    realizado = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Control de {self.persona} - {self.tipo_control} ({self.fecha_programada})"

    class Meta:
        verbose_name = "Control de Salud"
        verbose_name_plural = "Controles de Salud"
        ordering = ['fecha_programada']
