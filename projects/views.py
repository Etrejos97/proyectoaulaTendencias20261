from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer


class IsOwnerOrAdmin(permissions.BasePermission):

     
    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
            
        
        return getattr(request.user, 'is_admin', False)

class ProjectViewSet(viewsets.ModelViewSet):
    
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    
    def get_queryset(self):
        
        return Project.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)