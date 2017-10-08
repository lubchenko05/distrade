from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, PermissionsMixin
from django.db.models.signals import post_save

"""
TODO:

    0. [Done] Modify models:
       Add ImageField, where it's needed.

    1. [Done] modify user model, need to add.
        - Profile photo.
        - Address.
        - Phone.

    2. [Done] Create User role. something like shop manager.
       Create permission for this role.

    3. Create views for clients.

    4. Create views for managing data.

"""


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True, null=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ,
    )
    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=16, blank=True)
    image = models.ImageField(upload_to='Images/Users', default='Images/None/NoUser.jpg', blank=True)
    address = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)

    def __str__(self):
          return "%s's profile" % self.user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, blank='True')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='Images/Categories', default='Images/None/NoCategory.jpg')

    def __str__(self):
        return self.name


class Criterion(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='Images/Providers', default='Images/None/NoProvider.jpg')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True,)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, related_name='products')

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(upload_to='Images/Products', default='Images/None/NoProduct.jpg')

    def __str__(self):
        return '%s-%s' % (self.product.name, str(self.pk))


class Characteristic(models.Model):
    product = models.ForeignKey(Product, related_name='characteristics')
    criterion = models.ForeignKey(Criterion, related_name='values')
    value = models.CharField(max_length=255)

    def __str__(self):
        return '%s - %s' % (self.product.name, self.criterion.name)


class Feedback(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='feedbacks', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feedbacks')
    disadvantage = models.CharField(max_length=255, blank=True)
    message = models.TextField(blank=True)
    mark = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)], default=10)

    def __str__(self):
        return '%s - %s' % (self.owner.username, self.product.name)


class Order(models.Model):
    STATUS = (
        ('NEW', 'Created'),
        ('RUN', 'Confirmed'),
        ('DEL', 'Canceled'),
        ('OK', 'Delivered'),
    )

    customer = models.ForeignKey(get_user_model())
    products = models.ManyToManyField(Product)
    date = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=255, choices=STATUS, default='NEW')

    def __str__(self):
        return '%s - %s' % (self.customer.username, str(self.date))


class Message(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='messages')
    title = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now)
    text = models.TextField()

    def __str__(self):
        return '%s - %s' % (self.owner.username, self.title)