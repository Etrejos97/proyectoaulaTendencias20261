from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Task
from .serializers import TaskSerializer

class IsAdminOrAssigned(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if view.action in ['create', 'destroy'] and not request.user.is_admin:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.assigned_to == request.user
        return obj.assigned_to == request.user
    
class TaskViewSet(viewsets.ModelViewSet):
    
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAssigned]

    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    
    filterset_fields = ['project', 'status', 'priority', 'assigned_to', 'is_active']
    
    
    search_fields = ['title', 'description']
    
    
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']

    
    def get_queryset(self):
        
        if self.request.user.is_admin:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=self.request.user)
    
    
    