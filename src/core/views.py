from django.contrib.auth import authenticate, login, logout

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, \
    UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User
import core.serializers as core_serializers


class UserCreateView(CreateAPIView):
    serializer_class = core_serializers.UserCreateSerializer


class UserLoginView(CreateAPIView):
    serializer_class = core_serializers.UserLoginSerializer

    def perform_create(self, serializer):
        login(request=self.request, user=serializer.save())


class RetrieveUpdateUser(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = core_serializers.UserRetrieveUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = core_serializers.UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

