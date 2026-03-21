from rest_framework import serializers
from .models import Task
from projects.serializers import ProjectSerializer
from users.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
  
    project_info = ProjectSerializer(source='project', read_only=True)
    assigned_to_info = UserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'priority', 'status', 
            'due_date', 'completed_at', 'is_active', 'project', 'project_info',
            'assigned_to', 'assigned_to_info', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'completed_at', 'created_at', 'updated_at']
        
    def validate(self, attrs):
      
        project = attrs.get('project')
        
        
        if project and project.status != 'active':
            from rest_framework import serializers
            raise serializers.ValidationError(
                {"project": "Prohibido: No se pueden agregar ni asignar tareas a un proyecto archivado o inactivo."}
            )
            
        return attrs
