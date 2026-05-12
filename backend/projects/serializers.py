from rest_framework import serializers
from .models import Project, ProjectMembership
from users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):

    owner_info = UserSerializer(source='owner', read_only=True)
    my_role = serializers.SerializerMethodField()

    def get_my_role(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            membership = ProjectMembership.objects.filter(
                project=obj,
                user=request.user
            ).first()
            return membership.role if membership else None
        return None

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'status', 'start_date', 'due_date',
            'owner', 'owner_info', 'my_role', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'my_role', 'created_at', 'updated_at']

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


class ProjectMembershipSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = ProjectMembership
        fields = ['id', 'project', 'project_name', 'user', 'username', 'role', 'joined_at']
        read_only_fields = ['id', 'joined_at', 'username', 'project_name']