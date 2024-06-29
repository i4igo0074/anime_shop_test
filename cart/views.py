from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Cart, CartItem
from products.models import Product
import json 
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.total_quantity += quantity
        cart_item.save()

        # Обновление корзины
        cart.save()

        return redirect('product_detail', product_id=product_id)
    return HttpResponseBadRequest('Invalid request method')

@login_required
def update_cart_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        action = data.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id)

        if action == 'increase':
            cart_item.total_quantity += 1
        elif action == 'decrease' and cart_item.total_quantity > 1:
            cart_item.total_quantity -= 1
        cart_item.save()

        # Обновление корзины
        cart_item.cart.save()

        return JsonResponse({
            'total_quantity': cart_item.total_quantity,
            'total_price': cart_item.total_price,
            'cart_total_quantity': cart_item.cart.final_quantity,
            'cart_total_price': cart_item.cart.final_price,
        })

@login_required
def remove_cart_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()

        # Обновление корзины
        cart_item.cart.save()

        return JsonResponse({
            'cart_total_quantity': cart_item.cart.final_quantity,
            'cart_total_price': cart_item.cart.final_price,
        })

@login_required
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.items.all() if cart else []
    cart_total_price = cart.final_price if cart else 0
    cart_count = cart.final_quantity if cart else 0

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'cart_total_price': cart_total_price,
        'cart_count': cart_count
    })