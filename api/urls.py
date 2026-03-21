"""
Router principal que agrupa todas las APIs de apps
"""
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from users.urls import router as users_router
from projects.urls import router as projects_router  
from tasks.urls import router as tasks_router

# Combina TODOS los routers
main_router = DefaultRouter()

# Incluye routers de cada app
main_router.registry.extend(users_router.registry)
main_router.registry.extend(projects_router.registry)
main_router.registry.extend(tasks_router.registry)

urlpatterns = [
    path('', include(main_router.urls)),
]
