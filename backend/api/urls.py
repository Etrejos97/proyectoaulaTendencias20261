from rest_framework.routers import DefaultRouter
from django.urls import path, include
from users.urls import router as users_router
from projects.urls import router as projects_router  
from tasks.urls import router as tasks_router

main_router = DefaultRouter()

main_router.registry.extend(users_router.registry)
main_router.registry.extend(projects_router.registry)
main_router.registry.extend(tasks_router.registry)

urlpatterns = [
    path('', include(main_router.urls)),
]
