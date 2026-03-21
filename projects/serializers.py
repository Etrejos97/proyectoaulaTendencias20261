from rest_framework import serializers
from .models import Project
from users.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    # Retornamos los detalles del owner al consultar un proyecto
    owner_info = UserSerializer(source='owner', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status', 'start_date', 'due_date', 
            'owner', 'owner_info', 'created_at', 'updated_at'
        ]
        # Estos campos los manejará automáticamente la API, no el usuario final
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']