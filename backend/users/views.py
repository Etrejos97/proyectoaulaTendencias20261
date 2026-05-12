from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from tasks.models import Task
from .models import User
from .serializers import UserSerializer


class IsAdminOrSelf(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if view.action in ['list', 'destroy'] and not request.user.is_admin:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj == request.user

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAdminOrSelf()]

    def get_queryset(self):
        if self.request.user.is_admin:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)

    @action(detail=False, methods=['get'], url_path='profile')
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Se requiere el refresh token.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': 'Sesión cerrada correctamente.'},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {'error': 'Token inválido o ya expirado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'], url_path='metrics')
    def metrics(self, request, pk=None):
        user = self.get_object()

        if not request.user.is_admin and request.user != user:
            raise PermissionDenied("No tienes permiso para ver las métricas de este usuario.")

        tasks = Task.objects.filter(assigned_to=user)

        total = tasks.count()
        completed = tasks.filter(status='completed').count()
        cancelled = tasks.filter(status='cancelled').count()
        overdue = tasks.filter(
            due_date__lt=timezone.now()
        ).exclude(status__in=['completed', 'cancelled']).count()
        in_progress = tasks.filter(status='in_progress').count()
        pending = tasks.filter(status='pending').count()

        base = total - cancelled
        fulfillment_rate = round((completed / base) * 100, 1) if base > 0 else 0.0

        return Response({
            'user_id': str(user.id),
            'username': user.username,
            'total_assigned': total,
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'cancelled': cancelled,
            'overdue': overdue,
            'fulfillment_rate_percent': fulfillment_rate,
        })