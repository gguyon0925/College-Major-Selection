from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet

# Use router to automatically determine API URLs.
router = DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
