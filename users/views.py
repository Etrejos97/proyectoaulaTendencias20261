from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    Gestiona las operaciones CRUD para los Usuarios.
    Permite registrarse (AllowAny en POST) pero requiere estar
    autenticado para ver la lista de usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Permite crear un usuario (registrarse) a cualquier persona, sin estar logueado
        if self.action == 'create':
            return [permissions.AllowAny()]
        # Las demás peticiones (listar, actualizar, borrar) exigen estar autenticado
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='profile')
    def profile(self, request):
        """
        GET /api/users/profile/
        Devuelve los datos del usuario actualmente autenticado.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        """
        POST /api/users/logout/
        Invalida el refresh token del usuario (blacklist).
        Requiere enviar: { "refresh": "<token>" }
        """
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