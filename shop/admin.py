from django.contrib import admin
from .models import Category, Product, Image, Comment, Feature, ProductFeature, Order
from shop.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Feature)
admin.site.register(ProductFeature)
admin.site.register(User)
admin.site.register(Order)
