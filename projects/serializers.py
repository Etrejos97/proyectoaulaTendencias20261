from rest_framework import serializers
from .models import Project
from users.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    
    owner_info = UserSerializer(source='owner', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status', 'start_date', 'due_date', 
            'owner', 'owner_info', 'created_at', 'updated_at'
        ]
        
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
        
    def validate_description(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError('La descripción debe tener al menos 10 caracteres.')
        return value

    def validate(self, data):
        start = data.get('start_date')
        due = data.get('due_date')
        if start and due and start > due:
            raise serializers.ValidationError({'due_date': 'La fecha límite debe ser posterior a la fecha de inicio.'})
        return data