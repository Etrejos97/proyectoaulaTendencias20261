from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    """
    Gestiona todas las operaciones CRUD para el modelo Project.
    Requiere que el usuario esté logueado (autenticado mediante token).
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Cuando se crea un proyecto, agarramos al usuario que está logueado
    def get_queryset(self):
        # Solo devuelve proyectos donde el usuario es el owner
        return Project.objects.filter(owner=self.request.user)
    # y lo asignamos automáticamente como el dueño (owner) del proyecto
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)