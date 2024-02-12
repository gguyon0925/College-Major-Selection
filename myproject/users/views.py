from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth.hashers import make_password

from .models import CustomUser
from .serializers import CustomUserSerializer


class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the request user is the object itself or an admin
        return request.user == obj or request.user.is_staff


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email']  # Specify fields to search against
    # Specify fields to allow ordering against
    ordering_fields = ['username', 'email']
    throttle_classes = [UserRateThrottle]

    # Define custom permission settings for different actions
    permission_classes_by_action = {
        'set_password': [IsSelfOrAdmin],
        'default': [IsAuthenticated]
    }

    def get_permissions(self):
        # Get the permission classes based on the action
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # Default to the 'default' permission classes if action is not specified
            return [permission() for permission in self.permission_classes_by_action['default']]

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        password = request.data.get('password')

        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Set and save the new password
        user.password = make_password(password)
        user.save()

        return Response({"status": "password set"}, status=status.HTTP_200_OK)
