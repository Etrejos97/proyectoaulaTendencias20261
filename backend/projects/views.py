from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField
from .models import Project, ProjectMembership
from .serializers import ProjectSerializer, ProjectMembershipSerializer
from .permissions import IsProjectMember, IsProjectEditorOrOwner


class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectEditorOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Project.objects.all()
        member_projects = ProjectMembership.objects.filter(
            user=user
        ).values_list('project_id', flat=True)
        return Project.objects.filter(id__in=member_projects)

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMembership.objects.create(
            project=project,
            user=self.request.user,
            role=ProjectMembership.Role.OWNER
        )

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.is_admin:
            return obj
        if not ProjectMembership.objects.filter(user=user, project=obj).exists():
            raise PermissionDenied("No eres miembro de este proyecto.")
        return obj

    @action(detail=True, methods=['post'], url_path='archive')
    def archive(self, request, pk=None):
        project = self.get_object()
        user = request.user

        is_owner = ProjectMembership.objects.filter(
            user=user,
            project=project,
            role=ProjectMembership.Role.OWNER
        ).exists()

        if not is_owner and not user.is_admin:
            raise PermissionDenied("Solo el propietario puede archivar el proyecto.")

        if project.status == Project.Status.ARCHIVED:
            return Response(
                {'detail': 'El proyecto ya está archivado.'},
                status=400
            )

        project.status = Project.Status.ARCHIVED
        project.save()
        serializer = self.get_serializer(project)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='reactivate')
    def reactivate(self, request, pk=None):
        project = self.get_object()
        user = request.user

        is_owner = ProjectMembership.objects.filter(
            user=user,
            project=project,
            role=ProjectMembership.Role.OWNER
        ).exists()

        if not is_owner and not user.is_admin:
            raise PermissionDenied("Solo el propietario puede reactivar el proyecto.")

        if project.status == Project.Status.ACTIVE:
            return Response(
                {'detail': 'El proyecto ya está activo.'},
                status=400
            )

        project.status = Project.Status.ACTIVE
        project.save()
        serializer = self.get_serializer(project)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='metrics')
    def metrics(self, request, pk=None):
        project = self.get_object()
        tasks = project.tasks.all()

        total = tasks.count()
        by_status = tasks.values('status').annotate(total=Count('id'))
        completed = tasks.filter(status='completed').count()
        pending = tasks.filter(status='pending').count()
        in_progress = tasks.filter(status='in_progress').count()
        cancelled = tasks.filter(status='cancelled').count()
        overdue = tasks.filter(
            due_date__lt=timezone.now()
        ).exclude(status__in=['completed', 'cancelled']).count()

        completed_tasks = tasks.filter(
            status='completed',
            completed_at__isnull=False
        ).annotate(
            resolution_time=ExpressionWrapper(
                F('completed_at') - F('created_at'),
                output_field=DurationField()
            )
        )
        avg_seconds = completed_tasks.aggregate(avg=Avg('resolution_time'))['avg']
        avg_hours = round(avg_seconds.total_seconds() / 3600, 2) if avg_seconds else None

        return Response({
            'project_id': str(project.id),
            'project_name': project.name,
            'total_tasks': total,
            'by_status': {item['status']: item['total'] for item in by_status},
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress,
            'cancelled': cancelled,
            'overdue': overdue,
            'avg_resolution_hours': avg_hours,
        })


class ProjectMembershipViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return ProjectMembership.objects.all()
        member_projects = ProjectMembership.objects.filter(
            user=user
        ).values_list('project_id', flat=True)
        return ProjectMembership.objects.filter(project_id__in=member_projects)

    def perform_create(self, serializer):
        project = serializer.validated_data.get('project')
        user = self.request.user
        membership = ProjectMembership.objects.filter(
            user=user,
            project=project,
            role=ProjectMembership.Role.OWNER
        ).first()
        if not membership and not user.is_admin:
            raise PermissionDenied("Solo el propietario del proyecto puede agregar miembros.")
        serializer.save()

    def perform_update(self, serializer):
        project = serializer.instance.project
        user = self.request.user
        membership = ProjectMembership.objects.filter(
            user=user,
            project=project,
            role=ProjectMembership.Role.OWNER
        ).first()
        if not membership and not user.is_admin:
            raise PermissionDenied("Solo el propietario puede modificar roles.")
        serializer.save()