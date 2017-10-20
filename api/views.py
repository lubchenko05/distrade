from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.paginations import StandardResultsSetPagination
from root.models import Category, Provider, Product, Order, Criterion
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


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])  # In prod change to IsManager or IsAdmin
def create_category(request):
    if 'name' in request.data:
        if Category.objects.filter(name=request.data['name']).exists():
            return Response(data={"error": 'Category with name %s already exist!' % request.data['name']},
                            status=status.HTTP_400_BAD_REQUEST)

        category = Category.objects.create(name=request.data['name'],
                                           description=request.data['description'] if 'description' in request.data else '',
                                           image=request.data['image'] if 'image' in request.data else None, )
        criterion = request.data['criterion'] if 'criterion' in request.data else None
        if criterion:
            if type(criterion) == list:
                for item in criterion:
                    Criterion.objects.create(name=item, category=category)
            else:
                Criterion.objects.create(name=criterion, category=Category)
        return Response(data=CategoryDetailSerializer(category).data)
    else:
        return Response(data={"error": "Name was required"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])  # In prod change to IsManager or IsAdmin
def update_category(request, name):
    if not Category.objects.filter(name=name).exists():
        return Response(data={"error": 'Category with name %s was not found' % name},
                        status=status.HTTP_404_NOT_FOUND)
    category = Category.objects.get(name=name)
    if 'description' in request.data:
        category.description = request.data['description']
    if 'image' in request.data:
        category.image = request.data['image']
    if 'criterion' in request.data:
        criterion = request.data['criterion']
        if type(criterion) == list:
            pass
        else:
            pass
    return Response(data=CategoryDetailSerializer(category).data)


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
    try:
        user = UserModel.objects.get(pk=pk)
    except:
        user = None
    if user:
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

"""
TODO:
0. Add liked for user and likes for product. [Done]
1. View for add category. [Done]
2. View for add product.
3. View for edit category.
4. View for edit product.
5. View for add order.
6. View for edit order.
7. View for generate check.
8. View for paying with LiqPay
"""