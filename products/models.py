from django.db import models
from decimal import Decimal
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    base_image = models.ImageField(upload_to='product_images')
    discount = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    


    @property
    def discounted_price(self):
        return round(self.price * Decimal(1 - self.discount / 100),2)

    def __str__(self):
        return self.name
    
    @property
    def rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            return round(total_rating / len(reviews), 1)
        return 0
        
    @property
    def count_reviews(self):
        return self.reviews.count()
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/%Y/%m/%d/')

    def __str__(self):
        return f'{self.product.name} Image'
    

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])


    def __str__(self):
        return f'Review for {self.product.name} by {self.author.username}'
    

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ('user', 'product')


class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='collections', blank=True)
    products = models.ManyToManyField(Product, related_name='collections', blank=True)
    is_system = models.BooleanField(default=False)
    image = models.ImageField(upload_to='collection_images', null=True, blank=True)

    def __str__(self):
        return self.name
