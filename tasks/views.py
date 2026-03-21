from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD para Tareas. Soporta filtros avanzados, búsquedas de texto y ordenamiento.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Configuramos qué herramientas de búsqueda/filtro vamos a usar
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filtros exactos
    filterset_fields = ['project', 'status', 'priority', 'assigned_to', 'is_active']
    
    # Búsqueda por similitud de texto (ej. si contiene una palabra)
    search_fields = ['title', 'description']
    
    # Campos que el usuario puede usar para ordenar el listado (ascendente o descendente)
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']

    # Solo devuelve tareas de proyectos donde el usuario es owner
    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)
    
    
    