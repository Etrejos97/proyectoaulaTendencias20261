from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    
    filterset_fields = ['project', 'status', 'priority', 'assigned_to', 'is_active']
    
    
    search_fields = ['title', 'description']
    
    
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']

    
    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)
    
    
    