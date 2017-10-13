from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.paginations import StandardResultsSetPagination
from root.models import Category, Provider, Product, Order
from root.permissions import IsSelf
from .serializers import (
    UserSerializer,
    CategorySerializer,
    CategoryDetailSerializer,
    ProviderSerializer,
    ProductSerializer, OrderSerializer)

UserModel = get_user_model()


class CreateUserView(CreateAPIView):
    model = UserModel
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UpdateUserView(UpdateAPIView):
    queryset = UserModel
    permission_classes = (IsAuthenticated, IsSelf)
    serializer_class = UserSerializer


class ListCategoryView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination


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


class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    permission_classes(AllowAny,)
    serializer_class = OrderSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_user_detail(request, pk):
    user = UserModel.objects.get(pk=pk)
    if user.exist():
        data = UserSerializer(user, context={'request': request})
        return Response(data=data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_self_user(request):
    data = request.user
    if data:
        return Response(data=UserSerializer(data, context={'request': request}).data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def deploy(request):
    #  TODO: Run deploy script
    return Response(data={"ok": "Deploy was complete!"})
