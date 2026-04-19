from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TagViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]