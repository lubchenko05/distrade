from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

"""
TODO:

    0. Modify models
       Add ImageField, where it's needed.

    1. modify user model, need to add:
        - Profile photo.
        - Address *.
        - Phone.

    2. Create views for clients.

    3. Create User role. something like shop manager.
       Create permission for this role.

    4. Create views for managing data.

"""


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=16)
    image = models.ImageField(upload_to='Images/Users', default='Images/None/NoUser.jpg')
    address = models.CharField(max_length=255)

    def __str__(self):
          return "%s's profile" % self.user


def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='Images/Categories', default='Images/None/NoCategory.jpg')

    def __str__(self):
        return self.name


class Criterion(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

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


class Provider(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)  # MAKE COUNTRY CHOICES
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='Images/Providers', default='Images/None/NoProvider.jpg')

    def __str__(self):
        return self.name


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
