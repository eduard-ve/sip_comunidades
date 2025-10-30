from django.db import models
from .personas import Persona
from .catalogos import TipoRelacion

# Modelo de Relaciones Familiares entre Personas
class RelacionFamiliar(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='relaciones')
    familiar = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='familiares')
    tipo_relacion = models.ForeignKey(TipoRelacion, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.persona} - {self.tipo_relacion} - {self.familiar}"
    
    class Meta:
        verbose_name = "Relación Familiar"
        verbose_name_plural = "Relaciones Familiares"
        constraints = [
            models.CheckConstraint(check=~models.Q(persona=models.F('familiar')), name='no_auto_relacion')
 ]
