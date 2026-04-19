from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
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
        # Solo proyectos donde el usuario tiene membresía
        member_projects = ProjectMembership.objects.filter(
            user=user
        ).values_list('project_id', flat=True)
        return Project.objects.filter(id__in=member_projects)

    def perform_create(self, serializer):
        # Guarda el proyecto y automáticamente crea membresía owner
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
        # Verifica que el usuario sea miembro antes de retornar el objeto
        if not ProjectMembership.objects.filter(user=user, project=obj).exists():
            raise PermissionDenied("No eres miembro de este proyecto.")
        return obj


class ProjectMembershipViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return ProjectMembership.objects.all()
        # Solo membresías de proyectos donde el usuario participa
        member_projects = ProjectMembership.objects.filter(
            user=user
        ).values_list('project_id', flat=True)
        return ProjectMembership.objects.filter(project_id__in=member_projects)

    def perform_create(self, serializer):
        project = serializer.validated_data.get('project')
        user = self.request.user
        # Solo el owner del proyecto puede agregar miembros
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
        # Solo el owner puede cambiar roles
        membership = ProjectMembership.objects.filter(
            user=user,
            project=project,
            role=ProjectMembership.Role.OWNER
        ).first()
        if not membership and not user.is_admin:
            raise PermissionDenied("Solo el propietario puede modificar roles.")
        serializer.save()