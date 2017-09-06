from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Category, Product, ProductImages, Provider


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = ('name', 'address', 'description', 'image')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone', 'image', 'address')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        profile_data = validated_data.pop('profile')
        # create profile
        profile = Profile.objects.create(
            user=user,
            phone=profile_data['phone'],
            image=profile_data['image'],
            address=profile_data['address'],
        )

        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('url', 'email', 'username', 'password', 'profile')


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ('image',)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer(many=True, read_only=True)
    provider = ProviderSerializer(read_only=True)
    category = serializers.HyperlinkedRelatedField(view_name='category-detail', read_only=True, lookup_field='name')

    class Meta:
        model = Product
        fields = ('name', 'description', 'images', 'category', 'provider')


class CategoryDetailSerializer(serializers.ModelSerializer):
    products = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='product-detail',
        read_only=True,
        lookup_field='name')

    class Meta:
        model = Category
        fields = ('name', 'description', 'image', 'products')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'description', 'image')
