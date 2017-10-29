import os

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from api.paginations import StandardResultsSetPagination
from root.models import Category, Provider, Product, Order, Criterion, Like, Check
from root.permissions import IsSelf, IsOrderCustomer, IsOrderCustomer, IsManager
from .serializers import (
    UserSerializer,
    CategorySerializer,
    CategoryDetailSerializer,
    ProviderSerializer,
    ProductSerializer, OrderSerializer, OrderDetailSerializer, OrderCreateSerializer, CheckSerializer)

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
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategoryDetailSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'pk'


@api_view(['POST'])
@permission_classes([IsManager, ])  # In prod change to IsManager or IsAdmin
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
@permission_classes([IsManager, ])  # In prod change to IsManager or IsAdmin
def update_category(request, pk):
    if not Category.objects.filter(pk=pk).exists():
        return Response(data={"error": 'Category with name %s was not found' % pk},
                        status=status.HTTP_404_NOT_FOUND)
    category = Category.objects.get(pk=pk)
    if 'description' in request.data:
        category.description = request.data['description']
    if 'image' in request.data:
        category.image = request.data['image']
    return Response(data=CategoryDetailSerializer(category).data)


@api_view(['POST'])
@permission_classes([IsManager, ])  # In prod change to IsManager or IsAdmin
def update_category__add_criterion(request, pk):
    if not Category.objects.filter(pk=pk).exists():
        return Response(data={"error": 'Category with pk %s was not found' % pk},
                        status=status.HTTP_404_NOT_FOUND)
    category = Category.objects.get(pk=pk)
    if 'criterion' in request.data:
        criterion = request.data['criterion']
    else:
        return Response(data={"error": "List of criterion required that named 'criterion'"})
    for c in criterion:
        Criterion.objects.create(category=category, name=c)
    return Response(data=CategoryDetailSerializer(category).data)


@api_view(['POST'])
@permission_classes([IsManager, ])  # In prod change to IsManager or IsAdmin
def update_category__remove_criterion(request, pk):
    if not Category.objects.filter(pk=pk).exists():
        return Response(data={"error": 'Category with name %s was not found' % pk},
                        status=status.HTTP_404_NOT_FOUND)
    category = Category.objects.get(pk=pk)
    if 'criterion' in request.data:
        criterion = request.data['criterion']
    else:
        return Response(data={"error": "List of criterion required that named 'criterion'"})
    obj_criterion = Criterion.objects.filter(category=category)
    for i in obj_criterion:
        if i.name in criterion:
            i.delete()
    return Response(data=CategoryDetailSerializer(category).data)


class ListProductView(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination


class DetailProviderView(RetrieveAPIView):
    queryset = Provider.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProviderSerializer


class DetailProductView(RetrieveAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def update_product__add_like(request, pk):
    if not Product.objects.filter(pk=pk).exists():
        return Response(data={"error": 'Product with name %s was not found' % pk},
                        status=status.HTTP_404_NOT_FOUND)
    product = Product.objects.get(pk=pk)
    like = Like.objects.get_or_create(product=product)[0]
    if request.user not in like.users.all():
        like.users.add(request.user)
        like.save()
        return Response(data={'ok': 'Like was added'})
    else:
        return Response(data={'error': 'Like was already added'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def update_product__remove_like(request, pk):
    if not Product.objects.filter(pk=pk).exists():
        return Response(data={"error": 'Product with name %s was not found' % pk},
                        status=status.HTTP_404_NOT_FOUND)
    product = Product.objects.get(pk=pk)
    like = Like.objects.get_or_create(product=product)[0]
    if request.user in like.users.all():
        like.users.remove(request.user)
        like.save()
        return Response(data={'ok': 'Like was removed'})
    else:
        return Response(data={'error': 'User was not liked this product before'}, status=status.HTTP_400_BAD_REQUEST)


class OrderListView(ListAPIView):
    permission_classes([IsAuthenticated, ])
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-date')


class DetailOrderView(RetrieveAPIView):
    queryset = Order.objects.all()
    permission_classes([IsAuthenticated, IsOrderCustomer])
    serializer_class = OrderDetailSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_check(request, pk):
        orders = Order.objects.filter(pk=pk)
        if orders.exists():
            if request.user == orders[0].customer or request.user.is_staff:
                if not orders[0].get_check:
                    return HttpResponse('<h1>Not Found(404)</h1>')
                return HttpResponse(orders[0].get_check.get().get_pdf(), content_type='application/report')
            else:
                return HttpResponse('<html><body>Access error</body></html>')
        else:
            return HttpResponse('<html><body><h1>Not Found(404)</h1></body></html>')


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def create_order(request):
    serializer = OrderCreateSerializer(data=request.data, context={'user': request.user})
    if serializer.is_valid():
        serializer.save()
        data = OrderDetailSerializer(serializer.instance)
        return Response(data.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderView(UpdateAPIView):
    queryset = Order.objects.all()
    permission_classes([IsAuthenticated, IsOrderCustomer])
    serializer_class = OrderCreateSerializer


class CheckListView(ListAPIView):
    queryset = Check.objects.all()
    permission_classes([IsAuthenticated, ])
    serializer_class = CheckSerializer

    def get_queryset(self):
        return Check.objects.filter(customer=self.request.user)


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
    try:
        os.system('sh /usr/src/app/update.sh')
        return Response(data={"ok": "Deploy was complete!"})
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'deploy error'})