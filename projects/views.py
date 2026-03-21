from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True            
        return request.user.is_admin
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin

class ProjectViewSet(viewsets.ModelViewSet):
    
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    
    def get_queryset(self):
        if self.request.user.is_admin:
            return Project.objects.all()
        
        return Project.objects.filter(tasks__assigned_to=self.request.user).distinct()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)