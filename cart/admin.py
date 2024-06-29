from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('user', 'final_quantity', 'final_price')
    list_filter = ('user',)
    search_fields = ('user__username',)
    readonly_fields = ('final_quantity', 'final_price')


