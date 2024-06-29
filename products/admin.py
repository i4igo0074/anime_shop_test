from django.contrib import admin
from .models import Category, Product, Country, ProductImage, ProductReview, Collection

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Country)
admin.site.register(ProductImage)
admin.site.register(ProductReview)
admin.site.register(Collection)