from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('update/', views.update_cart_item, name='update_cart_item'),
    path('remove/', views.remove_cart_item, name='remove_cart_item'),
    path('', views.cart_detail, name='cart_detail'),  # Добавляем отображение корзины
]