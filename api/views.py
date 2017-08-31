from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from api.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
