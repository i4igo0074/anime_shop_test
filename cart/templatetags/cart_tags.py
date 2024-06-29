#cart_tags.py

from django import template
from cart.models import Cart

register = template.Library()

@register.inclusion_tag('cart/cart.html', takes_context=True)
def show_cart(context):
    request = context['request']
    cart_count = request.session.get('cart_count', 0) 

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.final_quantity
        cart_items = cart.items.all()
        cart_total_price = cart.final_price
    else:
        cart_items = []
        cart_count = 0
        cart_total_price = 0
    return {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'cart_total_price': cart_total_price,
    }