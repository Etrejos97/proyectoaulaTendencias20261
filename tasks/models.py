import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from projects.models import Project


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, verbose_name='Nombre de la Etiqueta')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tags_created',
        verbose_name='Creada por'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ['name']
        unique_together = ('name', 'created_by')

    def __str__(self):
        return self.name


class Task(models.Model):

    class Priority(models.TextChoices):
        LOW = 'low', 'Baja'
        MEDIUM = 'medium', 'Media'
        HIGH = 'high', 'Alta'
        CRITICAL = 'critical', 'Crítica'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        IN_PROGRESS = 'in_progress', 'En progreso'
        IN_REVIEW = 'in_review', 'En revisión'
        COMPLETED = 'completed', 'Completada'
        CANCELLED = 'cancelled', 'Cancelada'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(blank=True, verbose_name='Descripción')
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name='Prioridad'
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Estado'
    )
    due_date = models.DateTimeField(null=True, blank=True, verbose_name='Fecha límite')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha completada')
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Proyecto'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks_assigned',
        verbose_name='Asignada a'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tasks',
        blank=True,
        verbose_name='Etiquetas'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if self.status == self.Status.COMPLETED and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != self.Status.COMPLETED:
            self.completed_at = None
        super().save(*args, **kwargs)
        
class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Tarea'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Autor'
    )
    content = models.TextField(verbose_name='Contenido')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Meta:
    verbose_name = 'Comentario'
    verbose_name_plural = 'Comentarios'
    ordering = ['created_at']

def __str__(self):
    return f"Comentario de {self.author.username} en '{self.task.title}'"