import uuid
from django.db import models
from django.conf import settings

class Project(models.Model):
    

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Activo'
        ARCHIVED = 'archived', 'Archivado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='projects_owned'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ProjectMembership(models.Model):
    class Role(models.TextChoices):
        OWNER    = 'owner',    'Propietario'
        EDITOR   = 'editor',   'Editor'
        OBSERVER = 'observer', 'Observador'

    id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project   = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    user      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )
    role      = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.OBSERVER,
        verbose_name='Rol en el proyecto'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')
        verbose_name = 'Membresía de Proyecto'
        verbose_name_plural = 'Membresías de Proyecto'
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.user} → {self.project} ({self.role})"