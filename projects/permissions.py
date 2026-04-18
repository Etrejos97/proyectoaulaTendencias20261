from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import ProjectMembership


class IsProjectMember(BasePermission):
    """
    Solo permite acceso a usuarios que sean miembros del proyecto.
    Se aplica en TaskViewSet y CommentViewSet.
    """
    message = "No eres miembro de este proyecto."

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        # obj puede ser una Task o un Comment — obtenemos el proyecto
        project = obj if hasattr(obj, 'memberships') else getattr(obj, 'project', None)
        if project is None:
            return False
        return ProjectMembership.objects.filter(
            user=request.user,
            project=project
        ).exists()


class IsProjectEditorOrOwner(BasePermission):
    """
    Solo permite crear/editar/eliminar a usuarios con rol owner o editor.
    Los observers solo pueden hacer GET.
    Se aplica en TaskViewSet.
    """
    message = "Necesitas rol de editor o propietario para esta acción."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_admin:
            return True
        project = getattr(obj, 'project', obj)
        role = ProjectMembership.objects.filter(
            user=request.user,
            project=project
        ).values_list('role', flat=True).first()
        return role in ('owner', 'editor')


class IsCommentAuthorOrAdmin(BasePermission):
    """
    Solo el autor del comentario o un admin global puede editarlo o eliminarlo.
    Cualquier miembro puede leer (GET).
    Se aplica en CommentViewSet (lo usará Persona 3).
    """
    message = "Solo el autor o un administrador puede modificar este comentario."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_admin