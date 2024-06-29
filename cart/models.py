from django.db import models
from authorization.models import CustomerUser
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    final_quantity = models.IntegerField(default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        items = self.items.all()
        self.final_quantity = sum(item.total_quantity for item in items)
        self.final_price = sum(item.total_price for item in items)
        super().save(update_fields=['final_quantity', 'final_price'])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.product.name} - {self.cart.user.username}"

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.total_quantity
        super().save(*args, **kwargs)
        self.cart.save()