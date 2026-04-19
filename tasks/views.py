from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Task
from .serializers import TaskSerializer
from projects.models import ProjectMembership
from projects.permissions import IsProjectMember, IsProjectEditorOrOwner


class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember, IsProjectEditorOrOwner]

    filterset_fields = ['project', 'status', 'priority', 'assigned_to', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        # Solo tareas de proyectos donde el usuario es miembro
        member_projects = ProjectMembership.objects.filter(
            user=user
        ).values_list('project_id', flat=True)
        return Task.objects.filter(project__in=member_projects)