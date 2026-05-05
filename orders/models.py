from django.db import models
from django.contrib.auth.models import User


class WorkOrder(models.Model):
    """Modelo principal de Orden de Trabajo."""

    class Status(models.TextChoices):
        PENDING   = 'PENDIENTE',  'Pendiente'
        IN_PROGRESS = 'EN_PROCESO', 'En Proceso'
        COMPLETED = 'COMPLETADA', 'Completada'
        CANCELLED = 'CANCELADA',  'Cancelada'

    class Priority(models.TextChoices):
        LOW    = 'BAJA',   'Baja'
        MEDIUM = 'MEDIA',  'Media'
        HIGH   = 'ALTA',   'Alta'

    # Identificación
    code         = models.CharField(max_length=20, unique=True, editable=False)
    title        = models.CharField(max_length=200, verbose_name='Título')
    description  = models.TextField(verbose_name='Descripción')

    # Clasificación
    status   = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name='Estado')
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM, verbose_name='Prioridad')

    # Asignación
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_orders', verbose_name='Asignado a')
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='created_orders', verbose_name='Creado por')

    # Fechas
    due_date   = models.DateField(null=True, blank=True, verbose_name='Fecha límite')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Orden de Trabajo'
        verbose_name_plural = 'Órdenes de Trabajo'

    def __str__(self):
        return f"{self.code} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.code:
            last = WorkOrder.objects.order_by('id').last()
            next_id = (last.id + 1) if last else 1
            self.code = f"OT-{next_id:04d}"
        super().save(*args, **kwargs)

    @property
    def status_badge(self):
        badges = {
            'PENDIENTE':  'warning',
            'EN_PROCESO': 'info',
            'COMPLETADA': 'success',
            'CANCELADA':  'secondary',
        }
        return badges.get(self.status, 'light')

    @property
    def priority_badge(self):
        badges = {
            'BAJA':  'success',
            'MEDIA': 'warning',
            'ALTA':  'danger',
        }
        return badges.get(self.priority, 'light')
