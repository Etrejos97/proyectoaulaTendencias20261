from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Task, Tag, Comment, TaskHistory
from .serializers import TaskSerializer, TagSerializer, CommentSerializer, TaskHistorySerializer
from projects.models import ProjectMembership
from projects.permissions import IsProjectMember, IsProjectEditorOrOwner, IsCommentAuthorOrAdmin


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectMember, IsProjectEditorOrOwner]
    filterset_fields = ['project', 'status', 'priority', 'assigned_to', 'is_active', 'tags__name']
    search_fields = ['title', 'description', 'tags__name']
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        member_projects = ProjectMembership.objects.filter(
            user=user
        ).values_list('project_id', flat=True)
        return Task.objects.filter(project__in=member_projects)

    def perform_update(self, serializer):
        
        serializer.instance._changed_by = self.request.user
        serializer.save()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        task_id = self.request.query_params.get('task')
        if user.is_admin:
            qs = Comment.objects.all()
        else:
            member_projects = ProjectMembership.objects.filter(
                user=user
            ).values_list('project_id', flat=True)
            qs = Comment.objects.filter(task__project__in=member_projects)
        if task_id:
            qs = qs.filter(task_id=task_id)
        return qs

    def perform_create(self, serializer):
        task_id = self.request.data.get('task')
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise PermissionDenied("La tarea no existe.")
        if not self.request.user.is_admin:
            is_member = ProjectMembership.objects.filter(
                user=self.request.user,
                project=task.project
            ).exists()
            if not is_member:
                raise PermissionDenied("No eres miembro de este proyecto.")
        serializer.save(author=self.request.user)


class TaskHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['task', 'field_changed']   
    ordering_fields = ['changed_at']               

    def get_queryset(self):
        user = self.request.user
        task_id = self.request.query_params.get('task')
        if user.is_admin:
            qs = TaskHistory.objects.all()
        else:
            member_projects = ProjectMembership.objects.filter(
                user=user
            ).values_list('project_id', flat=True)
            qs = TaskHistory.objects.filter(task__project__in=member_projects)
        if task_id:
            qs = qs.filter(task_id=task_id)
        return qs