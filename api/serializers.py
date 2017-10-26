import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from root.models import Profile, Category, Product, ProductImages, Provider, Order, Criterion, Characteristic, Like, \
    OrderProduct, Check


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ('name', 'address', 'description', 'image')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone', 'email', 'image', 'address')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    password = serializers.CharField(write_only=True)
    likes = serializers.HyperlinkedIdentityField(view_name='product-detail',
                                                 lookup_field='pk', many=True,
                                                 read_only=True,)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        phone = ''
        image = None
        address = ''
        email = ''
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
        # create profile
            if 'phone' in profile_data:
                phone = profile_data['phone']
            if 'email' in profile_data:
                email = profile_data['email']
            if 'image' in profile_data:
                image = profile_data['image']
            if 'address' in profile_data:
                address = profile_data['address']
        profile = Profile.objects.create(
            user=user,
            phone=phone,
            image=image,
            address=address,
            email=email,
        )

        user.save()
        return user

    def update(self, instance, validated_data):
        profile = Profile.objects.get(user=instance)
        if 'phone' in validated_data:
            profile.phone = validated_data['phone']
        if 'email' in validated_data:
            profile.email = validated_data['email']
        if 'image' in validated_data:
            profile.image = validated_data['image']
        if 'address' in validated_data:
            profile.address = validated_data['address']
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        profile.save()
        instance.save()
        return instance

    class Meta:
        model = get_user_model()
        fields = ('url', 'username', 'password', 'profile', 'likes')


class CriterionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Criterion
        fields = ('name',)


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ('name', 'value',)


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ('image',)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('users', )


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True, read_only=True)
    characteristics = CharacteristicSerializer(many=True, read_only=True)
    provider = ProviderSerializer(read_only=True)
    category = serializers.HyperlinkedRelatedField(view_name='category-detail', read_only=True, lookup_field='pk')
    liked = LikeSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'characteristics', 'images', 'category', 'provider', 'liked',
                  'likes_count')


class CategoryDetailSerializer(serializers.ModelSerializer):
    # products = serializers.HyperlinkedRelatedField(
    #    many=True,
    #    view_name='product-detail',
    #    read_only=True,
    #    lookup_field='name')
    products = ProductSerializer(many=True, read_only=True)
    criterion = CriterionSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'description', 'criterion', 'image', 'products']


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category-detail', lookup_field='pk')

    class Meta:
        model = Category
        fields = ['id', 'url', 'name', 'description', 'image']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['customer', 'products', 'date', 'status', 'typeof_delivery',
                  'typeof_payment']


class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['customer', 'products', 'date', 'status', 'typeof_delivery',
                  'typeof_payment', 'name', 'surname', 'address', 'email']


class OrderCreateSerializer(serializers.ModelSerializer):
    status = serializers.CharField(allow_blank=True, allow_null=True)
    products = serializers.ListField(allow_blank=True)


    class Meta:
        model = Order
        fields = ['status', 'products', 'typeof_delivery',
                  'typeof_payment', 'name', 'surname', 'address', 'email']

    def create(self, validated_data):
        customer = self.context['request.user']
        typeof_delivery = validated_data['typeof_delivery'] if 'typeof_delivery' in validated_data else ''
        typeof_payment = validated_data['typeof_payment'] if 'typeof_payment' in validated_data else ''
        name = validated_data['name'] if 'name' in validated_data else ''
        surname = validated_data['surname'] if 'surname' in validated_data else ''
        address = validated_data['address'] if 'address' in validated_data else ''
        email = validated_data['email'] if 'email' in validated_data else ''

        if 'products' in validated_data:
            products = validated_data['products']
            for i in products:
                product = Product.objects.filter(pk=i[0])
                if product.exists():
                    OrderProduct.objects.create(order=self, product=product[0], count=i[1])

        order = Order.objects.create(customer=customer,
                                     typeof_delivery=typeof_delivery,
                                     typeof_payment=typeof_payment,
                                     name=name,
                                     surname=surname,
                                     address=address,
                                     email=email)
        order.save()
        return order

    def update(self, instance, validated_data):
        if 'status' in validated_data:
            if validated_data['status'] == "PAY":
                check = Check.objects.filter(order=instance)
                if not check.exists():
                    order = instance,
                    product = ', '.join(['"%s":{"price": "%s", "count":"%s"}'
                                         % (p.product.name, p.product.price, p.count) for p in instance.products])
                    customer = instance.customer
                    check = Check.objects.create(order=order, product=product[:-1] if product else '', customer=customer)
                    check.file = check.get_pdf()
                    check.save()
            instance.status = validated_data['status']  # TODO: CHECK PAYMENT
        if 'typeof_delivery' in validated_data:
            instance.typeof_delivery = validated_data['typeof_delivery']
        if 'typeof_payment' in validated_data:
            instance.typeof_payment = validated_data['typeof_payment']
        if 'name' in validated_data:
            instance.name = validated_data['name']
        if 'surname' in validated_data:
            instance.surname = validated_data['surname']
        if 'address' in validated_data:
            instance.address = validated_data['address']
        if 'email' in validated_data:
            instance.email = validated_data['email']
        instance.save()
        return instance


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ('file', )
