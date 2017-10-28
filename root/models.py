from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from django.db.models.signals import post_save
from django.utils import timezone
from pdf_generator import generate_pdf


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
        'Unselect this instead of deleting accounts.',
    )
    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=16, blank=True)
    image = models.ImageField(upload_to='Images/Users', default='Images/None/NoUser.jpg', blank=True)
    address = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)

    def __str__(self):
          return "%s's profile" % self.user


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, blank='True')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='Images/Categories', default='Images/None/NoCategory.jpg')

    def __str__(self):
        return self.name


class Criterion(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, null=True, related_name='criterion')

    def __str__(self):
        return '%s - %s' % (self.name, self.category.name)


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
    price = models.FloatField(default=0.0, blank=True)

    def __str__(self):
        return self.name

    def likes_count(self):
        return self.liked.count()


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

    def name(self):
        return self.criterion.name


class Feedback(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='feedbacks', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feedbacks')
    advantage = models.CharField(max_length=255, blank=True)
    disadvantage = models.CharField(max_length=255, blank=True)
    message = models.TextField(blank=True)
    mark = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)], default=10)

    def __str__(self):
        return '%s - %s' % (self.owner.username, self.product.name)


class Order(models.Model):
    STATUS = (
        ('NEW', 'Created'),
        ('PAY', 'Payed'),
        ('RUN', 'Confirmed'),
        ('DEL', 'Canceled'),
        ('OK', 'Delivered'),
    )

    date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(UserModel)
    status = models.CharField(max_length=255, choices=STATUS, default='NEW')
    typeof_delivery = models.CharField(max_length=100, null=True)  # TODO: Add choices
    typeof_payment = models.CharField(max_length=100, null=True)  # TODO: Add choices
    name = models.CharField(max_length=100, null=True)
    surname = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True)
    delivery_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s' % (self.customer.username, str(self.date))

    def total_cost(self):
        cost = 0
        for i in self.products.all():
            cost += i.product.price
        return cost


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, related_name='orders', blank=True)
    count = models.IntegerField(validators=[MaxValueValidator(10000), MinValueValidator(1)])

    def __str__(self):
        return "%s - %s * %s" % (self.order.date, self.product.name, int(self.count))

    def get_characteristic(self, name):
        c = Characteristic.objects.filter(product=self.product, criterion__name=name)
        if c.exists():
            return c[0].value.split(' ')[0]


class Message(models.Model):
    owner = models.ForeignKey(get_user_model(), related_name='messages')
    title = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField()

    def __str__(self):
        return '%s - %s' % (self.owner.username, self.title)


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='liked')
    users = models.ManyToManyField(UserModel, related_name='likes')

    def __str__(self):
        return "%s - %s like" % (self.product.name, str(self.users.count()))

    def likes_count(self):
        return self.users.count()


class Check(models.Model):
    order = models.ForeignKey(Order, related_name='order_check')
    date = models.DateTimeField(default=timezone.now)
    products = models.TextField()
    customer = models.ForeignKey(UserModel)
    file = models.FileField(null=True, blank=True, upload_to='Checks')

    def get_pdf(self):
        list_products = OrderProduct.objects.filter(order__pk=self.order.pk)
        generate_pdf.generate(self.order.id, self.order.name, self.order.surname,
                              self.order.phone, self.order.address, list_products)

    def __str__(self):
        return self.order.__str__()


class BlackList(models.Model):
    FIELDS = (
        ('N', 'Choose field'),
        ('E', 'Email'),
        ('P', 'Phone'),
        ('U', 'Username'),
        ('A', 'Address'),
    )
    field = models.CharField(max_length=255, choices=FIELDS, default='N')
    value = models.CharField(max_length=100)

    def __str__(self):
        return "%s - %s" % (self.field, self.value)
