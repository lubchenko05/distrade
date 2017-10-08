from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.paginations import StandardResultsSetPagination
from .permissions import IsManager, IsSelf
from .models import Category, Provider, Product
from .serializers import (
    UserSerializer,
    CategorySerializer,
    CategoryDetailSerializer,
    ProviderSerializer,
    ProductSerializer)


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UpdateUserView(UpdateAPIView):
    queryset = get_user_model()
    permission_classes = (IsAuthenticated, IsSelf)
    serializer_class = UserSerializer


class ListCategoryView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer


class DetailCategoryView(RetrieveAPIView):
    lookup_field = 'name'
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategoryDetailSerializer
    pagination_class = StandardResultsSetPagination


class ListProductView(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer


class DetailProviderView(RetrieveAPIView):
    queryset = Provider.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProviderSerializer


class DetailProductView(RetrieveAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_user_detail(request, pk):
    data = UserSerializer(get_user_model().objects.get(pk))
    if data:
        return Response(data=data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
