from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.mail import send_mail

# Create your models here.
class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    items = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name


class Feature(models.Model):
    name = models.CharField(max_length=100)
    size = models.IntegerField(default=False)
    weight = models.IntegerField(default=False)
    color = models.CharField(max_length=50, default=False)
    material = models.CharField(max_length=50, default=False)

    def __str__(self):
        return self.name


class ProductFeature(models.Model):
    feature = models.ManyToManyField(Feature)
    value = models.IntegerField()


class Image(models.Model):
    image = models.ImageField(default=False, upload_to='images/')


class User(AbstractUser):
    email = models.EmailField(unique=False)

    def __str__(self):
        return self.email


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    title = models.CharField(max_length=200)
    slug = models.SlugField(default=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(default=False)
    description = models.TextField(max_length=200)
    price = models.IntegerField()
    feature = models.ManyToManyField(ProductFeature)
    category= models.ForeignKey(Category, default=None, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ForeignKey(Image, default=None,  on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.product