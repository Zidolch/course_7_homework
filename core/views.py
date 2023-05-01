from typing import Any

from django.contrib.auth import login, logout
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response

from core.models import User
from core.serializers import UserCreateSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer


class SignUpView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: LoginSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request=request, user=serializer.save())
        return Response(serializer.data)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = ProfileSerializer
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)

    def get_object(self) -> User:
        return self.request.user

    def perform_destroy(self, instance: User) -> None:
        logout(self.request)


class UpdatePasswordView(generics.UpdateAPIView):
    permission_classes: tuple[BasePermission, ...] = (IsAuthenticated,)
    serializer_class = UpdatePasswordSerializer

    def get_object(self) -> User:
        return self.request.user
