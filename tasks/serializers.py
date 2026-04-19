from rest_framework import serializers
from .models import Task, Tag
from projects.serializers import ProjectSerializer
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_by', 'created_by_username', 'created_at']
        read_only_fields = ['created_by', 'created_at']

    def validate_name(self, value):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        qs = Tag.objects.filter(name__iexact=value.strip(), created_by=user)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "Ya tienes una etiqueta con este nombre."
            )
        return value.strip().lower()


class TagSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            tag = Tag.objects.filter(name__iexact=data.strip()).first()
            if not tag:
                request = self.context.get('request')
                user = request.user if request and request.user.is_authenticated else None
                tag = Tag.objects.create(name=data.strip().lower(), created_by=user)
            return tag
        except (TypeError, ValueError):
            self.fail('invalid')


class TaskSerializer(serializers.ModelSerializer):

    project_info = ProjectSerializer(source='project', read_only=True)
    assigned_to_info = UserSerializer(source='assigned_to', read_only=True)
    tags = TagSlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all(),
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'priority', 'status',
            'due_date', 'completed_at', 'is_active', 'project', 'project_info',
            'assigned_to', 'assigned_to_info', 'tags', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'completed_at', 'created_at', 'updated_at']

    def validate(self, attrs):
        project = attrs.get('project')

        if project and project.status != 'active':
            raise serializers.ValidationError(
                {"project": "Prohibido: No se pueden agregar ni asignar tareas a un proyecto archivado o inactivo."}
            )

        return attrs